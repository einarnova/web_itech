import os, re, json, shutil, zipfile

ludashi_dir = r"C:\Program Files (x86)\LuDaShi"
work_dir = r"C:\Users\LENOVO\Desktop\web_itech\temp_ludashi_ui"

# ============================================================
# MASSIVE TRANSLATION SCRIPT - Everything modifiable
# ============================================================

# DLL Binary Patches - SAME CHARACTER COUNT or shorter (padded with nulls)
# In UTF-16-LE: 1 Chinese char = 2 bytes = 1 Latin char = 2 bytes
# So replacement must have ≤ same NUMBER of characters
dll_translations = {
    # 4 chars -> 4 chars max
    "硬件体检": "Test HW ",  # 4 -> 8 chars... no, 4 Chinese = 4 chars
    # Actually in UTF-16, each char (Chinese or Latin) = 2 bytes
    # 硬件体检 = 4 chars = 8 bytes
    # So replacement can be up to 4 chars = 8 bytes
    # But that's too short for Spanish...
    # Let me use mixed approach: replace where possible
}

# Actually, the key issue: for DLLs, Chinese chars and Latin chars both take 2 bytes in UTF-16.
# 硬件体检 = 4 chars * 2 bytes = 8 bytes max -> "Test" (4 chars) works!
# But "Test" doesn't mean much in Spanish context.

# Let's focus on what CAN be modified:

# ============================================================  
# PART A: Translate ALL SuperApp JSON files
# ============================================================
print("=" * 60)
print("PARTE A: Traduciendo archivos JSON de SuperApp")
print("=" * 60)

json_translations = {
    # App names and descriptions
    "智能降温": "Enfriamiento",
    "系统清理": "Limpieza",
    "磁盘碎片整理": "Desfragmentar",
    "桌面快捷方式": "Acceso directo",
    "修复DLL": "Reparar DLL",
    "重复文件清理": "Limpiar duplicados",
    "护眼模式": "Modo lectura",
    "显卡优化": "Optimizar GPU",
    "拦截弹窗": "Bloquear popups",
    "内存优化专家": "Optimizar RAM",
    "多开微信": "Multi WeChat",
    "万能压缩": "Compresor",
    "电脑优化": "Optimizar PC",
    "隐私清理": "Limpiar privacidad",
    "隐身模式": "Modo incógnito",
    "隐私保护": "Proteger privacidad",
    "进程优化": "Optimizar procesos",
    "软件管家": "Gestor de software",
    "开始菜单增强": "Mejora menú inicio",
    "系统加速": "Acelerar sistema",
    "系统清理助手": "Asist. limpieza",
    "Win助手": "Asist. Windows",
    "屏蔽广告": "Bloquear anuncios",
    "垃圾清理": "Limpieza basura",
    "微信清理": "Limpiar WeChat",
    "蓝屏修复": "Reparar BSOD",
    "一键智能降温，延长硬件使用寿命": "Enfriamiento inteligente para prolongar vida del hardware",
    "快速清理系统中的垃圾文件": "Limpiar archivos basura del sistema",
    "整理磁盘碎片，提升磁盘读写速度": "Desfragmentar disco para mejor velocidad",
    "快捷管理桌面快捷方式": "Gestión rápida de accesos directos",
    "修复系统DLL缺失问题": "Reparar DLL faltantes del sistema",
    "清理电脑中的重复文件": "Limpiar archivos duplicados",
    "过滤有害蓝光，保护视力": "Filtrar luz azul dañina, proteger vista",
    "智能优化电脑显卡配置": "Optimizar configuración de GPU",
    "实时拦截系统弹窗广告": "Bloquear publicidad emergente en tiempo real",
    "释放不必要的内存占用": "Liberar memoria RAM innecesaria",
    "微信多开不串号": "Abrir múltiples instancias de WeChat",
    "万能压缩文件管理": "Compresor universal de archivos",
    "优化电脑运行速度": "Optimizar velocidad del PC",
    "清理浏览器和使用痕迹": "Limpiar historial del navegador",
    "隐身上网不留痕迹": "Navegar sin dejar rastro",
    "保护个人隐私数据安全": "Proteger datos personales",
    "优化系统进程提升性能": "Optimizar procesos para mejor rendimiento",
    "一站式管理电脑软件": "Gestión integral de software",
    "增强开始菜单功能": "Mejorar funciones del menú inicio",
    "加速系统启动速度": "Acelerar inicio del sistema",
    "清理系统垃圾文件": "Limpiar archivos basura",
    "智能优化助手": "Asistente inteligente",
    "清理微信缓存释放空间": "Limpiar caché de WeChat",
    "分析修复蓝屏问题": "Analizar y reparar pantallazos azules",
    # Common JSON field values
    "鲁大师": "LuDaShi",
    "立即使用": "Usar ahora",
    "开启": "Activar",
    "关闭": "Cerrar",
    "设置": "Config.",
    "更新": "Actualizar",
    "下载": "Descargar",
    "安装": "Instalar",
    "卸载": "Desinstalar",
    "正在检测": "Detectando",
    "检测完成": "Completado",
    "优化完成": "Optimizado",
    "清理完成": "Limpieza hecha",
}

superapp_dir = os.path.join(ludashi_dir, "SuperApp")
json_count = 0
if os.path.exists(superapp_dir):
    for root, dirs, files in os.walk(superapp_dir):
        for fname in files:
            if not fname.endswith('.json'):
                continue
            fpath = os.path.join(root, fname)
            try:
                with open(fpath, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                modified = False
                for ch, es in json_translations.items():
                    if ch in content:
                        content = content.replace(ch, es)
                        modified = True
                
                if modified:
                    # Save to work dir first
                    rel = os.path.relpath(fpath, ludashi_dir)
                    out_path = os.path.join(work_dir, "json_translated", rel)
                    os.makedirs(os.path.dirname(out_path), exist_ok=True)
                    with open(out_path, 'w', encoding='utf-8') as f:
                        f.write(content)
                    json_count += 1
                    print(f"  [OK] {os.path.relpath(fpath, superapp_dir)}")
            except Exception as e:
                pass

print(f"  Total JSON traducidos: {json_count}")

# ============================================================
# PART B: Translate DrvMgr XML files  
# ============================================================
print("\n" + "=" * 60)
print("PARTE B: Traduciendo archivos XML del DrvMgr")
print("=" * 60)

xml_translations = {
    # DrvMgr feedback
    "反馈问题类型": "Tipo de problema",
    "问题描述": "Descripción del problema",
    "联系方式": "Información de contacto",
    "截图": "Captura de pantalla",
    "提交": "Enviar",
    "取消": "Cancelar",
    "确定": "Aceptar",
    "关闭": "Cerrar",
    "驱动管理": "Gestión de controladores",
    "驱动安装": "Instalar controlador",
    "驱动更新": "Actualizar controlador",
    "驱动备份": "Respaldar controlador",
    "驱动还原": "Restaurar controlador",
    "正在检测": "Detectando",
    "检测完成": "Completado",
    "设备名称": "Nombre del dispositivo",
    "当前版本": "Versión actual",
    "最新版本": "Última versión",
    "操作": "Acción",
    "状态": "Estado",
    "已安装": "Instalado",
    "需要更新": "Necesita actualizar",
    "全部": "Todos",
    "正常": "Normal",
    "异常": "Anormal",
}

drvmgr_xml_dir = os.path.join(ludashi_dir, "DrvMgr")
xml_count = 0
for root, dirs, files in os.walk(drvmgr_xml_dir):
    for fname in files:
        if not fname.endswith('.xml'):
            continue
        fpath = os.path.join(root, fname)
        for enc in ['utf-16', 'utf-8']:
            try:
                with open(fpath, 'r', encoding=enc) as f:
                    content = f.read()
                break
            except:
                continue
        else:
            continue
        
        modified = False
        for ch, es in xml_translations.items():
            if ch in content:
                content = content.replace(ch, es)
                modified = True
        
        if modified:
            rel = os.path.relpath(fpath, ludashi_dir)
            out_path = os.path.join(work_dir, "xml_translated", rel)
            os.makedirs(os.path.dirname(out_path), exist_ok=True)
            with open(out_path, 'w', encoding=enc) as f:
                f.write(content)
            xml_count += 1
            print(f"  [OK] {rel}")

print(f"  Total XML traducidos: {xml_count}")

# ============================================================
# PART C: Patch DLL strings with SAME-LENGTH replacements
# ============================================================
print("\n" + "=" * 60)
print("PARTE C: Parcheando cadenas en DLLs (mismo largo)")
print("=" * 60)

# In UTF-16-LE: each char = 2 bytes, Chinese or Latin
# So 4 Chinese chars can be replaced by 4 Latin chars max
dll_replacements = {
    # Format: "chinese": "replacement" (MUST be same char count or less)
    # 2 chars (4 bytes)
    "详情": "Info",  # 2->4 NO, 2 chars -> 2 chars max
    "返回": "←←",
    "退出": "Exit",  # Actually need 2 chars... "退出" -> but Exit is 4
    
    # Let me be smarter - use exact same length
    # 2 char Chinese = 2 char replacement
    "详情": ">>",
    "返回": "<<",
    "退出": "XX",
    "清理": "Lp",
    "下载": "DL",
    "安装": "Ok",
    "查看": ">>",
    "忽略": "No",
    "得分": "Pt",
    "设置": "⚙️",  # emoji might not work, use "Cf" 
    
    # 3 chars = 3 char replacement
    "处理器": "CPU",
    "硬件防护": "Prot",  # 4 chars
    
    # 4 chars = 4 char replacement  
    "硬件体检": "Test",
    "硬件参数": "Info",
    "硬件评测": "Eval",
    "电脑优化": "Opti",
    "清理优化": "Limp",
    "驱动检测": "Driv",
    "温度管理": "Temp",
    "游戏助手": "Game",
    "性能跑分": "Bnch",
    "开始体检": "Test",
    "优化内存": "OptM",
    "隐藏标尺": "Ocul",
    "离开模式": "Away",
    
    # 5+ chars
    "主机监控": "Monit",  # 4 chars OK
    "内存性能": "mRAM",
    "显卡性能": "mGPU",
    "硬件信息": "HWin",
    "操作系统": "SysO",
    "磁盘检测": "Disc",
    
    # Longer strings
    "了解电脑健康状态": "Ver estado PC ",  # 8 chars -> need 8
    "建议立即体检": "Analice su PC",  # 6 chars -> 6... wait no
    "经常体检有助于提高电脑运行效率": "Analizar ayuda a mejorar el PC ",
}

# Actually let me do this properly
# Count chars and only replace what fits
dll_safe_replacements = {}
for ch, es in dll_replacements.items():
    if len(es) <= len(ch):
        dll_safe_replacements[ch] = es
    else:
        # Try to truncate
        dll_safe_replacements[ch] = es[:len(ch)]

print(f"  Reemplazos seguros: {len(dll_safe_replacements)}")

# Files to patch
dll_files = [
    os.path.join(ludashi_dir, "ComputerMonZ.dll"),
    os.path.join(ludashi_dir, "ComputerZ7.dll"),
    os.path.join(ludashi_dir, "ComputerZ7_x64.dll"),
    os.path.join(ludashi_dir, "ComputerZ_CN.dll"),
    os.path.join(ludashi_dir, "ComputerZ_CN.exe"),
    os.path.join(ludashi_dir, "ComputerZTray.exe"),
    os.path.join(ludashi_dir, "ComputerZMonHelper.exe"),
    os.path.join(ludashi_dir, "SettingCenter.exe"),
    os.path.join(ludashi_dir, "MiniUI.dll"),
    os.path.join(ludashi_dir, "Setting.dll"),
    os.path.join(ludashi_dir, "Perfmon.dll"),
    os.path.join(ludashi_dir, "TemperatureHistory.dll"),
    os.path.join(ludashi_dir, "PowerCalculator.exe"),
    os.path.join(ludashi_dir, "sites.dll"),
    os.path.join(ludashi_dir, "SiteUIHelper.dll"),
    os.path.join(ludashi_dir, "Safelive.dll"),
]

patched_dir = os.path.join(work_dir, "patched_dlls")
backup_dir = os.path.join(work_dir, "backup_dlls")
os.makedirs(patched_dir, exist_ok=True)
os.makedirs(backup_dir, exist_ok=True)

total_dll_patches = 0
for dll_path in dll_files:
    if not os.path.exists(dll_path):
        continue
    
    basename = os.path.basename(dll_path)
    try:
        with open(dll_path, 'rb') as f:
            data = bytearray(f.read())
    except Exception as e:
        print(f"  No se pudo leer: {basename} - {e}")
        continue
    
    # Backup
    backup_path = os.path.join(backup_dir, basename)
    if not os.path.exists(backup_path):
        with open(backup_path, 'wb') as f:
            f.write(data)
    
    patches_this_file = 0
    for chinese, spanish in dll_safe_replacements.items():
        chinese_bytes = chinese.encode('utf-16-le')
        spanish_bytes = spanish.encode('utf-16-le')
        
        # Pad with null bytes to match original length
        padded = spanish_bytes + b'\x00' * (len(chinese_bytes) - len(spanish_bytes))
        
        idx = 0
        while True:
            idx = data.find(chinese_bytes, idx)
            if idx == -1:
                break
            data[idx:idx + len(chinese_bytes)] = padded
            patches_this_file += 1
            total_dll_patches += 1
            idx += len(padded)
    
    if patches_this_file > 0:
        out_path = os.path.join(patched_dir, basename)
        with open(out_path, 'wb') as f:
            f.write(data)
        print(f"  [PATCHED] {basename}: {patches_this_file} parches")

print(f"  Total parches DLL: {total_dll_patches}")

# ============================================================
# PART D: Create install script
# ============================================================
print("\n" + "=" * 60)
print("PARTE D: Creando script de instalación completo")
print("=" * 60)

# Write a BAT that copies everything
install_bat = os.path.join(work_dir, "INSTALAR_TODO_ESPAÑOL.bat")
with open(install_bat, 'w', encoding='utf-8') as f:
    f.write('@echo off\n')
    f.write('chcp 65001 >nul\n')
    f.write('echo ================================================\n')
    f.write('echo   INSTALADOR COMPLETO LUDASHI EN ESPAÑOL\n')
    f.write('echo ================================================\n')
    f.write('echo.\n')
    f.write('net session >nul 2>&1\n')
    f.write('if %errorlevel% neq 0 (\n')
    f.write('    echo [ERROR] Ejecutar como ADMINISTRADOR\n')
    f.write('    pause\n')
    f.write('    exit /b 1\n')
    f.write(')\n')
    f.write('echo Cerrando LuDaShi...\n')
    f.write('taskkill /F /IM ComputerZTray.exe 2>nul\n')
    f.write('taskkill /F /IM ComputerZMonHelper.exe 2>nul')
    f.write('\ntaskkill /F /IM ComputerZService.exe 2>nul\n')
    f.write('taskkill /F /IM ComputerZ_CN.exe 2>nul\n')
    f.write('taskkill /F /IM computercenter.exe 2>nul\n')
    f.write('taskkill /F /IM SettingCenter.exe 2>nul\n')
    f.write('timeout /t 3 >nul\n')
    f.write('echo.\n')
    
    # Copy Themes UI files
    f.write('echo [1/4] Instalando temas traducidos...\n')
    f.write(f'robocopy "{work_dir}\\final_repacked\\Themes" "C:\\Program Files (x86)\\LuDaShi\\Themes\\Default" /E /IS /IT /R:3 /W:1 >nul\n')
    
    # Copy DrvMgr files
    f.write('echo [2/4] Instalando DrvMgr traducido...\n')
    f.write(f'copy /Y "{work_dir}\\final_repacked\\DrvMgr\\defaultskin.ui" "C:\\Program Files (x86)\\LuDaShi\\DrvMgr\\config\\defaultskin\\defaultskin.ui" >nul\n')
    f.write(f'copy /Y "{work_dir}\\final_repacked\\DrvMgr\\LuDaShiFeedback.ui" "C:\\Program Files (x86)\\LuDaShi\\DrvMgr\\feedback\\LuDaShiFeedback.ui" >nul\n')
    
    # Copy patched DLLs
    f.write('echo [3/4] Instalando DLLs parcheadas...\n')
    for dll_name in os.listdir(patched_dir):
        src = os.path.join(patched_dir, dll_name)
        dst = os.path.join(ludashi_dir, dll_name)
        f.write(f'copy /Y "{src}" "{dst}" >nul 2>nul\n')
        f.write(f'if %errorlevel%==0 echo   OK: {dll_name}\n')
    
    # Copy JSON files
    f.write('echo [4/4] Instalando JSON traducidos...\n')
    json_dir = os.path.join(work_dir, "json_translated", "SuperApp")
    if os.path.exists(json_dir):
        f.write(f'robocopy "{os.path.join(work_dir, "json_translated", "SuperApp")}" "C:\\Program Files (x86)\\LuDaShi\\SuperApp" /E /IS /IT /R:3 /W:1 >nul\n')
    
    # Copy XML files
    xml_dir = os.path.join(work_dir, "xml_translated")
    if os.path.exists(xml_dir):
        f.write(f'robocopy "{xml_dir}" "C:\\Program Files (x86)\\LuDaShi" /E /IS /IT /R:3 /W:1 >nul\n')
    
    f.write('echo.\n')
    f.write('echo ================================================\n')
    f.write('echo   INSTALACION COMPLETA!\n')
    f.write('echo   Reinicia LuDaShi para ver los cambios.\n')
    f.write('echo ================================================\n')
    f.write('pause\n')

print(f"  Instalador creado: {install_bat}")

print("\n" + "=" * 60)
print("RESUMEN")
print("=" * 60)
print(f"  JSON traducidos: {json_count}")
print(f"  XML traducidos:  {xml_count}")
print(f"  DLL parcheadas:  {total_dll_patches} parches")
print(f"  Temas UI:        15 archivos (del paso anterior)")
print(f"\n  Ejecuta: INSTALAR_TODO_ESPAÑOL.bat como Administrador")
