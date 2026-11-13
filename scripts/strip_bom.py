from pathlib import Path

p = Path(r"C:\Users\Lapto\PycharmProjects\Space_Segment_building\data\catalogs\platforms.json")
t = p.read_text(encoding="utf-8-sig")
p.write_bytes(t.replace("\r\n", "\n").encode("utf-8"))
print("BOM removed")
