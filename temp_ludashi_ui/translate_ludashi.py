import re, os, glob, shutil, zipfile

# Directorio de trabajo
work_dir = r"C:\Users\LENOVO\Desktop\web_itech\temp_ludashi_ui"
ludashi_themes = r"C:\Program Files (x86)\LuDaShi\Themes\Default"
ludashi_drvmgr = r"C:\Program Files (x86)\LuDaShi\DrvMgr\config\defaultskin"

# Mapeo de traducciones Chino -> Español
translations = {
    # === setting_content_general.xml ===
    "常规：": "General:",
    "常规": "General",
    "显示内存释放器（悬浮的加速球）": "Mostrar liberador de memoria (bola flotante)",
    "显示任务栏标尺": "Mostrar indicador en barra de tareas",
    "开机时自动启用硬件实时防护（核心功能，建议开启）": "Activar protección de hardware en tiempo real al iniciar (función principal, recomendado)",
    "显示电脑健康监控面板": "Mostrar panel de monitoreo de salud del PC",
    
    # === setting_content_hardware.xml ===
    "当硬件温度高于以下阈值时自动报警（报警阈值可手动修改）": "Alarma automática cuando la temperatura del hardware supere el umbral (modificable manualmente)",
    "硬件防护：": "Protección de hardware:",
    "硬件防护": "Protección de hardware",
    "全屏模式下即使硬件温度过高也不报警": "No alertar por alta temperatura en modo pantalla completa",
    "高温报警时，自动播放以下声音提示": "Al alertar por alta temperatura, reproducir el siguiente sonido",
    "处理器": "Procesador",
    "开启硬盘温度监控,每": "Activar monitoreo de temperatura del disco duro, cada",
    "秒检测一次(1-99s)": "segundos verificar una vez (1-99s)",
    "报警音效": "Sonido de alarma",
    
    # === setting_content_homepage.xml ===
    "主页防护：": "Protección de página de inicio:",
    "主页防护": "Protección de página de inicio",
    "浏览器主页防护，保护您的主页，防止被恶意篡改": "Proteger la página de inicio del navegador contra modificaciones maliciosas",
    "启用360安全上网导航（hao.360.cn）": "Activar navegación segura 360 (hao.360.cn)",
    "自定义锁定：": "Bloqueo personalizado:",
    "关闭主页防护功能": "Desactivar protección de página de inicio",
    
    # === setting_content_memopt.xml ===
    "手动优化内存时，自动清空剪切板": "Al optimizar memoria manualmente, vaciar portapapeles automáticamente",
    "内存优化：": "Optimización de memoria:",
    "内存优化": "Optimización de memoria",
    "当物理内存负载超过百分之": "Cuando la carga de memoria física exceda el",
    "自动优化内存后，告知我内存优化结果": "Después de optimizar, informarme del resultado",
    "时自动优化内存": "% optimizar memoria automáticamente",
    "仅在系统空闲时，才执行内存自动优化功能": "Optimizar memoria automáticamente solo cuando el sistema esté inactivo",
    "每次自动优化内存的间隔时间：": "Intervalo entre optimizaciones automáticas:",
    
    # === setting_content_clean.xml ===
    "关闭回收站右键菜单入口": "Desactivar entrada del menú contextual de la papelera",
    "电脑空闲时提醒我清理垃圾": "Recordarme limpiar cuando el PC esté inactivo",
    "垃圾清理：": "Limpieza de basura:",
    "垃圾清理": "Limpieza de basura",
    
    # === setting_content_savepower.xml ===
    "智能降温模式下即使温度过高也不报警": "No alertar por alta temperatura en modo de enfriamiento inteligente",
    "节能降温：": "Ahorro de energía:",
    "节能降温": "Ahorro de energía",
    "根据显示器类型自动选用节能壁纸": "Seleccionar automáticamente fondo de ahorro de energía según el monitor",
    "关闭屏幕保护程序": "Desactivar protector de pantalla",
    "自动调低显示器亮度": "Reducir automáticamente el brillo del monitor",
    '以下设置仅开启"全面节能"时有效': 'Los siguientes ajustes solo aplican con "Ahorro total" activado',
    '以下设置仅开启\u201c全面节能\u201d时有效': 'Los siguientes ajustes solo aplican con "Ahorro total" activado',
    "自定义电脑的待机时间：": "Personalizar tiempo de espera del PC:",
    "自定义显示器关闭时间：": "Personalizar tiempo de apagado del monitor:",
    
    # === setting_content_security.xml ===
    "开启病毒防护功能": "Activar protección antivirus",
    "病毒查杀：": "Análisis de virus:",
    "病毒查杀": "Análisis de virus",
    
    # === setting_content_advance.xml ===
    "增值业务：": "Servicios adicionales:",
    "增值业务": "Servicios adicionales",
    "鲁大师是一款免费的软件，有您的支持我们将走的更远": "LuDaShi es un software gratuito, con su apoyo llegaremos más lejos",
    "停止接收推广信息（鲁大师新功能等官方通知除外）": "Dejar de recibir promociones (excepto notificaciones oficiales)",
    
    # === setting_content_more.xml ===
    "其它设置：": "Otros ajustes:",
    "其它设置": "Otros ajustes",
    "安卓手机连接时，不安装手机助手组件": "No instalar componentes del asistente al conectar un celular Android",
    "安卓手机连接时，不再显示手机助手悬浮窗": "No mostrar ventana flotante del asistente al conectar un celular Android",
    "当有可用的新版本时提醒我": "Avisarme cuando haya una nueva versión disponible",
    "屏蔽广告弹窗": "Bloquear ventanas emergentes de publicidad",
    
    # === setting_mainwnd.xml ===
    "恢复默认": "Restaurar predeterminado",
    
    # === setting_mainwnd_functional.xml ===
    "常用网址": "Sitios frecuentes",
    "帮你快速打开常用网址": "Acceso rápido a tus sitios frecuentes",
    
    # === setting_mainwnd_informational.xml ===
    "新功能推荐（通过主界面推送等方式提示）": "Recomendación de nuevas funciones (notificaciones en la interfaz)",
    "开启后可不定期收到产品优化、内测试用等提醒": "Al activar, recibirás recordatorios de optimización y pruebas del producto",
    
    # === setting_msgbox.xml ===
    "正在进行清理优化,您确定要退出吗?": "Se está realizando una optimización. ¿Desea salir?",
    
    # === setting_msgbox_temperature.xml ===
    "硬件：英特尔 Core i7-6700": "Hardware: Intel Core i7-6700",
    "阈值：": "Umbral:",
    "摄氏度": "°C (Celsius)",
    "设置无效，请重试": "Configuración inválida, intente de nuevo",
}

def translate_xml(file_path, translations):
    """Replace Chinese strings in a UTF-16 XML file."""
    with open(file_path, 'r', encoding='utf-16') as f:
        content = f.read()
    
    modified = False
    for chinese, spanish in translations.items():
        if chinese in content:
            content = content.replace(chinese, spanish)
            modified = True
    
    if modified:
        with open(file_path, 'w', encoding='utf-16') as f:
            f.write(content)
        print(f"  [TRANSLATED] {os.path.basename(file_path)}")
    else:
        print(f"  [NO CHANGES] {os.path.basename(file_path)}")
    return modified

# Step 1: Extract all .ui files from Themes/Default
print("=" * 60)
print("PASO 1: Extrayendo archivos .ui del directorio de temas...")
print("=" * 60)

ui_dirs = {}  # map: original_path -> extracted_dir
for root, dirs, files in os.walk(ludashi_themes):
    for f in files:
        if f.endswith('.ui'):
            src = os.path.join(root, f)
            rel = os.path.relpath(root, ludashi_themes)
            extract_to = os.path.join(work_dir, "themes_extracted", rel, f.replace('.ui', ''))
            os.makedirs(extract_to, exist_ok=True)
            try:
                with zipfile.ZipFile(src, 'r') as zf:
                    zf.extractall(extract_to)
                ui_dirs[src] = extract_to
                print(f"  Extracted: {os.path.relpath(src, ludashi_themes)}")
            except Exception as e:
                print(f"  SKIP (not a zip): {os.path.relpath(src, ludashi_themes)} - {e}")

# Also extract DrvMgr defaultskin.ui
for f in ['defaultskin.ui']:
    src = os.path.join(ludashi_drvmgr, f)
    if os.path.exists(src):
        extract_to = os.path.join(work_dir, "drvmgr_extracted", f.replace('.ui', ''))
        os.makedirs(extract_to, exist_ok=True)
        try:
            with zipfile.ZipFile(src, 'r') as zf:
                zf.extractall(extract_to)
            ui_dirs[src] = extract_to
            print(f"  Extracted: DrvMgr/{f}")
        except Exception as e:
            print(f"  SKIP: DrvMgr/{f} - {e}")

# Step 2: Find and list all Chinese text
print("\n" + "=" * 60)
print("PASO 2: Buscando texto chino en todos los archivos XML...")
print("=" * 60)

all_chinese = {}
for src, extract_dir in ui_dirs.items():
    for xml_file in glob.glob(os.path.join(extract_dir, "**", "*.xml"), recursive=True):
        try:
            with open(xml_file, 'r', encoding='utf-16') as f:
                txt = f.read()
        except:
            try:
                with open(xml_file, 'r', encoding='utf-8') as f:
                    txt = f.read()
            except:
                continue
        
        titles = re.findall(r'title="([^"]+)"', txt)
        tips = re.findall(r'tip="([^"]+)"', txt)
        all_strings = titles + tips
        chinese = [t for t in all_strings if any('\u4e00' <= c <= '\u9fff' for c in t)]
        
        if chinese:
            rel = os.path.relpath(xml_file, work_dir)
            all_chinese[xml_file] = chinese
            print(f"\n  {rel}:")
            for t in chinese:
                status = "✓" if t in translations else "✗ (sin traducción)"
                print(f"    {status} {t}")

# Step 3: Translate
print("\n" + "=" * 60)
print("PASO 3: Aplicando traducciones...")
print("=" * 60)

translated_files = 0
for xml_file in all_chinese:
    if translate_xml(xml_file, translations):
        translated_files += 1

print(f"\n  Total archivos traducidos: {translated_files}")

# Step 4: Repackage .ui files
print("\n" + "=" * 60)
print("PASO 4: Reempaquetando archivos .ui...")
print("=" * 60)

repack_dir = os.path.join(work_dir, "repacked")
os.makedirs(repack_dir, exist_ok=True)

for src, extract_dir in ui_dirs.items():
    # Determine output path
    if "DrvMgr" in src:
        out_path = os.path.join(repack_dir, "DrvMgr", os.path.basename(src))
    else:
        rel = os.path.relpath(src, ludashi_themes)
        out_path = os.path.join(repack_dir, "Themes", rel)
    
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    
    with zipfile.ZipFile(out_path, 'w', zipfile.ZIP_STORED) as zf:
        for root, dirs, files in os.walk(extract_dir):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, extract_dir)
                zf.write(file_path, arcname)
    
    print(f"  Repackaged: {os.path.relpath(out_path, repack_dir)}")

print("\n" + "=" * 60)
print("COMPLETADO!")
print(f"Los archivos .ui traducidos están en: {repack_dir}")
print("=" * 60)
