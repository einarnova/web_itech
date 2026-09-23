import os, zipfile, glob, re

# Check if the Themes\UI\*.dat files are ZIP or some other format
ui_dir = r"C:\Program Files (x86)\LuDaShi\Themes\UI"
work = r"C:\Users\LENOVO\Desktop\web_itech\temp_ludashi_ui\ui_dat_check"
os.makedirs(work, exist_ok=True)

dat_files = [
    "ludashi.dat", "examine.dat", "bench.dat", "Clean.dat",
    "monitor.dat", "HardwareParams.dat", "ranking.dat",
    "setting.dat", "SuperApp.dat", "context_menu.dat",
    "browser_guard.dat", "general_setup.dat", "feedback.dat",
    "GamePage_Theme.dat"  # wait, no this isn't here
]

for dat_name in os.listdir(ui_dir):
    if not dat_name.endswith('.dat'):
        continue
    dat_path = os.path.join(ui_dir, dat_name)
    
    with open(dat_path, 'rb') as f:
        header = f.read(16)
    
    hex_header = ' '.join(f'{b:02X}' for b in header[:4])
    is_zip = header[:2] == b'PK'
    is_sqlite = header[:6] == b'SQLite'
    
    print(f"\n{dat_name} ({os.path.getsize(dat_path):,} bytes)")
    print(f"  Header: {hex_header}")
    
    if is_zip:
        print(f"  Formato: ZIP!")
        extract_to = os.path.join(work, dat_name.replace('.dat', ''))
        os.makedirs(extract_to, exist_ok=True)
        try:
            with zipfile.ZipFile(dat_path, 'r') as zf:
                zf.extractall(extract_to)
            # List XML files
            xmls = glob.glob(os.path.join(extract_to, '**', '*.xml'), recursive=True)
            print(f"  XMLs encontrados: {len(xmls)}")
            # Search for Chinese
            for xml_file in xmls:
                for enc in ['utf-16', 'utf-8']:
                    try:
                        with open(xml_file, 'r', encoding=enc) as xf:
                            txt = xf.read()
                        break
                    except:
                        continue
                else:
                    continue
                titles = re.findall(r'title="([^"]+)"', txt)
                chinese = [t for t in titles if any('\u4e00' <= c <= '\u9fff' for c in t)]
                if chinese:
                    print(f"  -> {os.path.relpath(xml_file, extract_to)}:")
                    for c in chinese[:5]:
                        print(f"     {c}")
                    if len(chinese) > 5:
                        print(f"     ... y {len(chinese)-5} más")
        except Exception as e:
            print(f"  Error extrayendo: {e}")
    else:
        # Check if contains Chinese text in raw form
        with open(dat_path, 'rb') as f:
            data = f.read()
        text = data.decode('utf-16-le', errors='ignore')
        targets = ['硬件体检', '硬件参数', '电脑优化', '开始体检']
        for t in targets:
            if t in text:
                idx = text.find(t)
                print(f"  Contains: '{t}' at pos {idx}")
        print(f"  Formato: {'SQLite' if is_sqlite else 'Binario/Otro'}")
