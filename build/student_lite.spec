# -*- mode: python ; coding: utf-8 -*-
import os
import sys

block_cipher = None

project_root = os.path.abspath(os.path.join(SPECPATH, '..'))
use_upx = sys.platform == 'win32'

added_files = [
    (os.path.join(project_root, 'data', 'catalogs', '*'), 'data/catalogs'),
    (os.path.join(project_root, 'data', 'images', '*'), 'data/images'),
    (os.path.join(project_root, 'data', 'missions', 'exam_optical_earth_observation.mission.json'), 'data/missions'),
]

a = Analysis(
    [os.path.join(project_root, 'src', 'ssb', 'student_app', 'main.py')],
    pathex=[os.path.join(project_root, 'src')],
    binaries=[],
    datas=added_files,
    hiddenimports=[
        'ssb.catalog.database',
        'ssb.catalog.datasheet',
        'ssb.core.calibration',
        'ssb.core.catalog_meta',
        'ssb.core.paths',
        'ssb.core.constants',
        'ssb.core.mission',
        'ssb.core.orbit',
        'ssb.core.payload',
        'ssb.core.platform',
        'ssb.core.project',
        'ssb.orbit.propagator',
        'ssb.orbit.station_access',
        'ssb.payload.optical_model',
        'ssb.payload.sar_model',
        'ssb.payload.spectrometer_model',
        'ssb.payload.comm_model',
        'ssb.payload.qkd_model',
        'ssb.system.checks',
        'ssb.system.configurator',
        'ssb.system.evaluator',
        'ssb.system.payload_evaluator',
        'ssb.conops.simulator',
        'ssb.report.generator',
        'ssb.ui_common.schematic',
        'ssb.ui_common.catalog_browser',
        'ssb.ui_common.global_architecture_view',
        'ssb.ui_common.platform_slots_widget',
        'ssb.ui_common.mission_sheet_view',
        'scipy.integrate',
        'scipy.spatial.transform',
        'docx',
        'matplotlib',
        'unittest',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=['tkinter'],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='SpaceSegmentBuilder-Student-Lite',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=use_upx,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=use_upx,
    upx_exclude=[],
    name='SpaceSegmentBuilder-Student-Lite',
)

if sys.platform == 'darwin':
    app = BUNDLE(
        coll,
        name='SpaceSegmentBuilder-Student-Lite.app',
        icon=None,
        bundle_identifier='edu.spacesegment.student.lite',
        info_plist={
            'CFBundleDisplayName': 'Space Segment Builder (Student Lite)',
            'CFBundleShortVersionString': '0.1.0',
            'NSHighResolutionCapable': True,
        },
    )
