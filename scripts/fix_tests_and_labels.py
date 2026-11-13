from pathlib import Path

ROOT = Path(r"C:\Users\Lapto\PycharmProjects\Space_Segment_building")

p = ROOT / "tests" / "unit" / "test_catalog_and_datasheets.py"
t = p.read_text(encoding="utf-8").replace("\r\n", "\n")
old = '''    assert len(plat_suppliers) == 5
    for sup in plat_suppliers:
        items = db.items_by_supplier(sup.id, "platform")
        assert len(items) >= 3, f"Supplier {sup.id} should have at least 3 platforms"
'''
new = '''    assert len(plat_suppliers) >= 10
    major_suppliers = 0
    for sup in plat_suppliers:
        items = db.items_by_supplier(sup.id, "platform")
        assert len(items) >= 1, f"Supplier {sup.id} should have at least 1 platform"
        if len(items) >= 3:
            major_suppliers += 1
    assert major_suppliers >= 5
    assert len(db.platforms) >= 26
'''
assert old in t
t = t.replace(old, new)
t = t.replace(
    "assert win.browser_platforms.list_suppliers.count() == 6",
    "assert win.browser_platforms.list_suppliers.count() >= 11",
)
p.write_text(t, encoding="utf-8")

m = ROOT / "src" / "ssb" / "student_app" / "main_window.py"
s = m.read_text(encoding="utf-8")
for a, b in [
    ("CubeSats (6U à 16U)", "CubeSats & Nanosats (3U à 27U)"),
    ("Microsatellites & SmallSats (50 à 500 kg)", "Microsatellites & SmallSats (45 à 500 kg)"),
    ("Plateformes moyennes (700 à 1500 kg)", "Plateformes moyennes (600 à 1500 kg)"),
    ("SmallGEO compactes (500 à 900 kg)", "SmallGEO compactes (500 à 1400 kg)"),
]:
    s = s.replace(a, b)
m.write_text(s, encoding="utf-8")
print("ok")
