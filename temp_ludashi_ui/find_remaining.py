import re, os, glob

work_dir = r"C:\Users\LENOVO\Desktop\web_itech\temp_ludashi_ui\themes_extracted"
missing = {}
for xml_file in glob.glob(os.path.join(work_dir, "**", "*.xml"), recursive=True):
    try:
        with open(xml_file, "r", encoding="utf-16") as f:
            txt = f.read()
    except:
        try:
            with open(xml_file, "r", encoding="utf-8") as f:
                txt = f.read()
        except:
            continue
    titles = re.findall(r'title="([^"]+)"', txt)
    tips = re.findall(r'tip="([^"]+)"', txt)
    for t in titles + tips:
        if any("\u4e00" <= c <= "\u9fff" for c in t):
            if t not in missing:
                missing[t] = os.path.relpath(xml_file, work_dir)

for t, f in sorted(missing.items(), key=lambda x: x[1]):
    print(f"  {f}: {t}")

print(f"\nTotal cadenas chinas restantes: {len(missing)}")
