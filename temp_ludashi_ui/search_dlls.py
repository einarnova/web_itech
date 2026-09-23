import os, re

# Buscar en las DLL principales los textos de la interfaz
files_to_check = [
    r"C:\Program Files (x86)\LuDaShi\ComputerMonZ.dll",
    r"C:\Program Files (x86)\LuDaShi\ComputerZ7.dll",
    r"C:\Program Files (x86)\LuDaShi\ComputerZ_CN.dll",
    r"C:\Program Files (x86)\LuDaShi\ComputerZ_CN.exe",
    r"C:\Program Files (x86)\LuDaShi\ComputerZTray.exe",
    r"C:\Program Files (x86)\LuDaShi\MiniUI.dll",
    r"C:\Program Files (x86)\LuDaShi\Setting.dll",
    r"C:\Program Files (x86)\LuDaShi\sites.dll",
    r"C:\Program Files (x86)\LuDaShi\SiteUIHelper.dll",
]

targets = [
    "硬件体检", "硬件参数", "硬件评测", "电脑优化", 
    "清理优化", "驱动检测", "主机监控", "开始体检",
    "建议立即体检", "了解电脑健康状态", "经常体检有助",
    "温度管理", "游戏助手", "性能跑分"
]

for filepath in files_to_check:
    if not os.path.exists(filepath):
        continue
    try:
        with open(filepath, "rb") as f:
            data = f.read()
    except Exception as e:
        print(f"No se pudo leer: {os.path.basename(filepath)} - {e}")
        continue
    
    # Try UTF-16-LE (Windows default for DLLs)
    text_u16 = data.decode("utf-16-le", errors="ignore")
    # Try UTF-8
    text_u8 = data.decode("utf-8", errors="ignore")
    
    found_any = False
    for t in targets:
        positions = []
        # Check UTF-16-LE
        idx = text_u16.find(t)
        if idx >= 0:
            positions.append(("UTF-16-LE", idx))
        # Check UTF-8
        idx8 = text_u8.find(t)
        if idx8 >= 0:
            positions.append(("UTF-8", idx8))
        
        if positions:
            if not found_any:
                print(f"\n=== {os.path.basename(filepath)} ({len(data):,} bytes) ===")
                found_any = True
            for enc, pos in positions:
                # Get byte offset
                if enc == "UTF-16-LE":
                    byte_offset = pos * 2
                    context_text = text_u16
                else:
                    byte_offset = pos
                    context_text = text_u8
                
                start = max(0, pos - 20)
                end = min(len(context_text), pos + 40)
                ctx = context_text[start:end].replace("\x00", "")
                print(f"  '{t}' [{enc}] byte_offset={byte_offset}: {repr(ctx[:80])}")

print("\nBúsqueda completada.")
