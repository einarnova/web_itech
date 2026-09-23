import re, os, glob

base = r"C:\Users\LENOVO\Desktop\web_itech\temp_ludashi_ui\SettingCenter"
for xml_file in glob.glob(os.path.join(base, "*.xml")):
    with open(xml_file, "r", encoding="utf-16") as f:
        txt = f.read()
    titles = re.findall(r'title="([^"]+)"', txt)
    tips = re.findall(r'tip="([^"]+)"', txt)
    chinese = [t for t in titles + tips if any(ord(c) > 127 for c in t)]
    if chinese:
        print(f"\n=== {os.path.basename(xml_file)} ===")
        for t in chinese:
            print(f"  {t}")
