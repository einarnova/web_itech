import os, struct

src = r"C:\Program Files (x86)\LuDaShi\ComputerZ.dat"
dst = r"C:\Users\LENOVO\Desktop\web_itech\temp_ludashi_ui\ComputerZ_copy.dat"

# Read with shared access
with open(src, "rb") as f:
    data = f.read()

with open(dst, "wb") as out:
    out.write(data)

print(f"Copiado: {len(data)} bytes")
header = " ".join(f"{b:02X}" for b in data[:16])
print(f"Header: {header}")

# Check if ZIP
if data[:2] == b"PK":
    print("Formato: ZIP")
elif data[:4] == b"SQLi":
    print("Formato: SQLite")
else:
    print(f"Formato: Desconocido (magic: {data[:4]})")

# Search for Chinese text in both UTF-16-LE and UTF-8
for encoding in ["utf-16-le", "utf-8"]:
    text = data.decode(encoding, errors="ignore")
    targets = ["硬件体检", "硬件参数", "电脑优化", "开始体检", "清理优化", "驱动检测", "建议立即体检"]
    found = False
    for t in targets:
        idx = text.find(t)
        if idx >= 0:
            if not found:
                print(f"\n=== Encoding: {encoding} ===")
                found = True
            start = max(0, idx - 30)
            end = min(len(text), idx + 60)
            ctx = repr(text[start:end])
            print(f"  '{t}' at pos {idx}: {ctx}")
