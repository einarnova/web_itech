import os, shutil, struct

# Las cadenas están en las DLLs como UTF-16-LE
# Podemos hacer un "binary patch" reemplazando las cadenas chinas por españolas
# IMPORTANTE: La cadena de reemplazo debe tener el MISMO número de bytes (o menor con padding de nulls)

def utf16le_bytes(text):
    return text.encode('utf-16-le')

def pad_to_length(replacement_bytes, original_length):
    """Pad replacement with null bytes to match original length"""
    if len(replacement_bytes) > original_length:
        return None  # Cannot replace - too long
    return replacement_bytes + b'\x00' * (original_length - len(replacement_bytes))

# DLL files to patch
dll_patches = {
    r"C:\Program Files (x86)\LuDaShi\ComputerZ7.dll": {
        "硬件体检": "Diag. HW",
        "硬件防护": "Protección",  
        "离开模式": "Modo ausente",
        "隐藏标尺": "Ocultar",
        "优化内存": "Optim. RAM",
        "开启硬件防护": "Activar Prot.",
        "硬件防护已开启": "Protección activa",
    },
    r"C:\Program Files (x86)\LuDaShi\ComputerMonZ.dll": {
        "硬件体检": "Diag. HW",
        "垃圾超过": "Basura>",
        "从未进行硬件体检": "Sin diagnóstico HW",
    },
}

work_dir = r"C:\Users\LENOVO\Desktop\web_itech\temp_ludashi_ui"
backup_dll_dir = os.path.join(work_dir, "backup_dlls")
os.makedirs(backup_dll_dir, exist_ok=True)
patched_dll_dir = os.path.join(work_dir, "patched_dlls")
os.makedirs(patched_dll_dir, exist_ok=True)

for dll_path, patches in dll_patches.items():
    if not os.path.exists(dll_path):
        print(f"No encontrado: {dll_path}")
        continue
    
    basename = os.path.basename(dll_path)
    print(f"\n=== {basename} ===")
    
    # Read the DLL
    with open(dll_path, 'rb') as f:
        data = bytearray(f.read())
    
    # Backup
    backup_path = os.path.join(backup_dll_dir, basename)
    with open(backup_path, 'wb') as f:
        f.write(data)
    print(f"  Backup: {backup_path}")
    
    total_patches = 0
    for chinese, spanish in patches.items():
        chinese_bytes = utf16le_bytes(chinese)
        spanish_bytes = utf16le_bytes(spanish)
        
        # Find all occurrences
        idx = 0
        count = 0
        while True:
            idx = data.find(chinese_bytes, idx)
            if idx == -1:
                break
            
            # Replace with padded version
            padded = pad_to_length(spanish_bytes, len(chinese_bytes))
            if padded is None:
                print(f"  SKIP '{chinese}' -> '{spanish}' (español demasiado largo: {len(spanish_bytes)} > {len(chinese_bytes)} bytes)")
                idx += len(chinese_bytes)
                continue
            
            data[idx:idx + len(chinese_bytes)] = padded
            count += 1
            total_patches += 1
            idx += len(padded)
        
        if count > 0:
            print(f"  PATCH '{chinese}' -> '{spanish}' ({count} ocurrencias)")
        else:
            print(f"  NOT FOUND: '{chinese}'")
    
    # Save patched DLL
    patched_path = os.path.join(patched_dll_dir, basename)
    with open(patched_path, 'wb') as f:
        f.write(data)
    print(f"  Guardado: {patched_path} ({total_patches} parches)")

# Now also search for the MAIN SIDEBAR text in the main EXE
print("\n\n=== Buscando textos del sidebar principal ===")
main_files = [
    r"C:\Program Files (x86)\LuDaShi\ComputerZ_CN.exe",
    r"C:\Program Files (x86)\LuDaShi\ComputerZ_CN.dll",
    r"C:\Program Files (x86)\LuDaShi\ComputerZTray.exe",
    r"C:\Program Files (x86)\LuDaShi\MiniUI.dll",
    r"C:\Program Files (x86)\LuDaShi\sites.dll",
]

sidebar_texts = ["硬件体检", "硬件参数", "硬件评测", "电脑优化", "清理优化", 
                 "驱动检测", "温度管理", "游戏助手", "性能跑分",
                 "开始体检", "建议立即体检", "了解电脑健康状态",
                 "电脑简介", "处理器信息", "主板信息", "内存信息",
                 "显卡信息", "硬盘信息", "显示器信息"]

for filepath in main_files:
    if not os.path.exists(filepath):
        continue
    try:
        with open(filepath, 'rb') as f:
            data = f.read()
    except Exception as e:
        print(f"  No se pudo leer {os.path.basename(filepath)}: {e}")
        continue
    
    found_any = False
    for t in sidebar_texts:
        t_bytes = utf16le_bytes(t)
        if t_bytes in data:
            if not found_any:
                print(f"\n  {os.path.basename(filepath)} ({len(data):,} bytes):")
                found_any = True
            # Count occurrences
            count = 0
            idx = 0
            while True:
                idx = data.find(t_bytes, idx)
                if idx == -1:
                    break
                count += 1
                idx += len(t_bytes)
            print(f"    '{t}' - {count} ocurrencia(s)")

print("\nAnálisis completado.")
