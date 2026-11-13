"""Cross-platform build, smoke-test, and packaging script for Space Segment Builder.

Usage:
    python scripts/build_dist.py
    python scripts/build_dist.py --targets student teacher --archive
    python scripts/build_dist.py --skip-test --archive
"""

from __future__ import annotations

import argparse
import os
import platform
import shutil
import subprocess
import sys
import time
import zipfile
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DIST_DIR = PROJECT_ROOT / "dist"
BUILD_DIR = PROJECT_ROOT / "build"
ARCHIVES_DIR = DIST_DIR / "archives"

TARGETS: dict[str, tuple[str, str]] = {
    "student": ("build/student.spec", "SpaceSegmentBuilder-Student"),
    "teacher": ("build/teacher.spec", "SpaceSegmentBuilder-Teacher"),
    "student_lite": ("build/student_lite.spec", "SpaceSegmentBuilder-Student-Lite"),
    "teacher_lite": ("build/teacher_lite.spec", "SpaceSegmentBuilder-Teacher-Lite"),
}


def platform_tag() -> str:
    machine = platform.machine().lower()
    arch_map = {
        "amd64": "x86_64",
        "x86_64": "x86_64",
        "arm64": "arm64",
        "aarch64": "arm64",
    }
    arch = arch_map.get(machine, machine or "unknown")
    if sys.platform == "win32":
        return f"windows-{arch}"
    if sys.platform == "darwin":
        return f"macos-{arch}"
    if sys.platform.startswith("linux"):
        return f"linux-{arch}"
    return f"{sys.platform}-{arch}"


def run_cmd(cmd: list[str], env: dict[str, str] | None = None, retry_win_4551: bool = False) -> None:
    print(f">>> {' '.join(cmd)}", flush=True)
    attempts = 4 if (retry_win_4551 and sys.platform == "win32") else 1
    for attempt in range(1, attempts + 1):
        try:
            subprocess.run(cmd, cwd=PROJECT_ROOT, env=env, check=True)
            return
        except OSError as exc:
            if getattr(exc, "winerror", None) == 4551 and attempt < attempts:
                print(
                    f"Windows Application Control blocked execution (attempt {attempt}/{attempts}); "
                    "waiting 3s for AV/policy scan...",
                    flush=True,
                )
                time.sleep(3)
                continue
            raise


def binary_path_for(app_name: str) -> Path:
    if sys.platform == "win32":
        return DIST_DIR / app_name / f"{app_name}.exe"
    if sys.platform == "darwin":
        app_bundle = DIST_DIR / f"{app_name}.app"
        if app_bundle.exists():
            return app_bundle / "Contents" / "MacOS" / app_name
        return DIST_DIR / app_name / app_name
    return DIST_DIR / app_name / app_name


def build_target(key: str) -> Path:
    spec_rel, app_name = TARGETS[key]
    spec_path = PROJECT_ROOT / spec_rel
    work_path = BUILD_DIR / f"work_{key}"

    run_cmd([
        sys.executable,
        "-m",
        "PyInstaller",
        "--noconfirm",
        "--clean",
        "--distpath",
        str(DIST_DIR),
        "--workpath",
        str(work_path),
        str(spec_path),
    ])

    if sys.platform == "darwin":
        app_bundle = DIST_DIR / f"{app_name}.app"
        if app_bundle.exists() and shutil.which("codesign"):
            run_cmd(["codesign", "--force", "--deep", "--sign", "-", str(app_bundle)])

    exe = binary_path_for(app_name)
    if not exe.exists():
        raise FileNotFoundError(f"Expected built executable not found: {exe}")
    return exe


def smoke_test(exe: Path) -> None:
    env = os.environ.copy()
    if sys.platform.startswith("linux") and not env.get("DISPLAY") and not env.get("WAYLAND_DISPLAY"):
        env["QT_QPA_PLATFORM"] = "offscreen"

    run_cmd([str(exe), "--version"], env=env, retry_win_4551=True)
    run_cmd([str(exe), "--test-launch"], env=env, retry_win_4551=True)


def archive_target(app_name: str, tag: str) -> Path:
    ARCHIVES_DIR.mkdir(parents=True, exist_ok=True)

    if sys.platform == "darwin":
        app_bundle = DIST_DIR / f"{app_name}.app"
        out_zip = ARCHIVES_DIR / f"{app_name}-{tag}.zip"
        if out_zip.exists():
            out_zip.unlink()
        if app_bundle.exists() and shutil.which("ditto"):
            run_cmd([
                "ditto",
                "-c",
                "-k",
                "--sequesterRsrc",
                "--keepParent",
                str(app_bundle),
                str(out_zip),
            ])
            return out_zip
        # Fallback using zip -y to preserve symlinks
        run_cmd(["zip", "-r", "-y", str(out_zip), f"{app_name}.app" if app_bundle.exists() else app_name])
        return out_zip

    if sys.platform.startswith("linux"):
        out_tar = ARCHIVES_DIR / f"{app_name}-{tag}.tar.gz"
        if out_tar.exists():
            out_tar.unlink()
        run_cmd(["tar", "-C", str(DIST_DIR), "-czf", str(out_tar), app_name])
        return out_tar

    # Windows zip
    src_dir = DIST_DIR / app_name
    out_zip = ARCHIVES_DIR / f"{app_name}-{tag}.zip"
    if out_zip.exists():
        out_zip.unlink()
    with zipfile.ZipFile(out_zip, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=6) as zf:
        for file_path in sorted(src_dir.rglob("*")):
            if file_path.is_file():
                zf.write(file_path, file_path.relative_to(DIST_DIR))
    return out_zip


def main() -> int:
    parser = argparse.ArgumentParser(description="Build Space Segment Builder standalone distributions.")
    parser.add_argument(
        "--targets",
        nargs="+",
        choices=[*TARGETS.keys(), "all"],
        default=["all"],
        help="Targets to compile (default: all).",
    )
    parser.add_argument("--skip-test", action="store_true", help="Skip --version and --test-launch smoke tests.")
    parser.add_argument("--archive", action="store_true", help="Package built outputs into dist/archives/.")
    args = parser.parse_args()

    selected = list(TARGETS.keys()) if "all" in args.targets else list(dict.fromkeys(args.targets))
    tag = platform_tag()
    print(f"Building targets {selected} for platform '{tag}'...", flush=True)

    built_archives: list[Path] = []
    for key in selected:
        _, app_name = TARGETS[key]
        exe = build_target(key)
        print(f"Built: {exe}", flush=True)
        if not args.skip_test:
            smoke_test(exe)
            print(f"Smoke test passed: {app_name}", flush=True)
        if args.archive:
            arc = archive_target(app_name, tag)
            built_archives.append(arc)
            print(f"Packaged: {arc}", flush=True)

    if built_archives:
        print("\nGenerated archives:", flush=True)
        for arc in built_archives:
            size_mb = arc.stat().st_size / (1024 * 1024)
            print(f"  - {arc} ({size_mb:.1f} MB)", flush=True)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
