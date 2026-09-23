import re, os, glob, zipfile

work_dir = r"C:\Users\LENOVO\Desktop\web_itech\temp_ludashi_ui"
ludashi_themes = r"C:\Program Files (x86)\LuDaShi\Themes\Default"

# Extended translations - ALL remaining Chinese strings
translations = {
    # === ComputerZMonitor MenuWnd ===
    "保持在其他窗口前面": "Mantener por encima de otras ventanas",
    "在硬件加速球中显示": "Mostrar en la bola de aceleración",
    "设置": "Configuración",
    "本次关闭": "Cerrar esta vez",
    "靠近屏幕边缘时贴边": "Ajustar al borde de pantalla",
    "返回": "Volver",
    "问题反馈": "Reportar problema",
    "在加速球上显示活动": "Mostrar actividad en la bola",
    "永久关闭硬件加速球": "Cerrar permanentemente la bola de aceleración",
    "透明度设置": "Configuración de transparencia",
    "自动自动": "Automático",
    "致您的一封信": "Una carta para usted",
    "这里是广告文字，蚊子蚊子蚊子蚊子蚊子蚊子蚊子蚊子蚊子": "Texto publicitario de ejemplo",
    "速度已优化，开个网页试试速度": "Velocidad optimizada, abra una web para probarla",
    "正在加载，请稍候": "Cargando, espere por favor",
    "网络无法连接": "No se puede conectar a la red",
    "重试": "Reintentar",
    
    # === ComputerZTray ===
    "游戏、视频自动隐藏": "Ocultar automáticamente en juegos/videos",
    "进入超节能离开模式": "Entrar en modo súper ahorro de energía",
    "鲁大师": "LuDaShi",
    "即将进入离开模式": "A punto de entrar en modo ausente",
    "进入离开模式后电脑将自动关闭显示器，以此来延长": "Al entrar en modo ausente, el monitor se apagará automáticamente para prolongar",
    "显示器的使用寿命及减少电量消耗。": "la vida útil del monitor y reducir el consumo de energía.",
    "您可以按键盘上的任意键，来唤醒显示器。": "Puede presionar cualquier tecla para activar el monitor.",
    "以后不再提醒": "No volver a recordar",
    "进入离开模式": "Entrar en modo ausente",
    "硬件实时防护未开启": "Protección de hardware en tiempo real no activada",
    "开启Protección de hardware，延长硬件寿命": "Activar Protección de hardware para prolongar la vida útil",
    "开启硬件防护，延长硬件寿命": "Activar Protección de hardware para prolongar la vida útil",
    "开启": "Activar",
    "硬件参数": "Parámetros de hardware",
    "驱动检测": "Detección de controladores",
    "显示硬件加速球": "Mostrar bola de aceleración de hardware",
    "显示Sitios frecuentes": "Mostrar Sitios frecuentes",
    "显示常用网址": "Mostrar Sitios frecuentes",
    "大师敲敲乐": "Juego de golpeo",
    "一键优化内存": "Optimizar memoria con un clic",
    "退出": "Salir",
    
    # === DownMgr ===
    "我的下载": "Mis descargas",
    "阿里旺旺": "AliWangWang",
    "安装失败，请手动安装": "Instalación fallida, instale manualmente",
    "下载目录": "Directorio de descarga",
    "当前下载": "Descarga actual",
    "更改软件下载目录": "Cambiar directorio de descarga",
    
    # === ExaminUI ===
    "5秒后开始性能检测": "La prueba de rendimiento iniciará en 5 segundos",
    "为避免评测中断，请尽量减少不必要操作（切换屏幕、运行其他程序）显卡评测时会出现短暂黑屏，此为正常现象。": "Para evitar interrupciones, minimice acciones innecesarias. Durante la prueba de GPU puede haber una pantalla negra momentánea, esto es normal.",
    "读取中...": "Cargando...",
    "检测硬件性能，提升运行速度": "Detectar rendimiento del hardware, mejorar la velocidad",
    "您已经7天未进行硬件体检，检测到您硬件可能有异常情况，电脑硬": "No ha realizado una revisión de hardware en 7 días, se detectaron posibles anomalías",
    "磁盘检测": "Detección de disco",
    "蓝月传奇1.44游戏游戏": "Blue Moon Legend 1.44 juego",
    "正在检测": "Detectando",
    "已检测到56项，目前5项问题，建议扫描后一键修复": "Se detectaron 56 elementos, 5 problemas, se recomienda reparar con un clic",
    "继续修复": "Continuar reparación",
    "硬件信息": "Información de hardware",
    "一键修复": "Reparar con un clic",
    "操作系统": "Sistema operativo",
    "描述": "Descripción",
    "最近三天": "Últimos 3 días",
    "查看全部": "Ver todo",
    "CPU温度达到88℃，受到高温威胁": "La temperatura del CPU alcanzó 88°C, amenaza de sobrecalentamiento",
    "查看": "Ver",
    "得分": "Puntuación",
    "清理": "Limpiar",
    "忽略": "Ignorar",
    "已忽略": "Ignorado",
    "已还原，下次生效": "Restaurado, se aplicará la próxima vez",
    "名称": "Nombre",
    "安装": "Instalar",
    "重新体检查看结果": "Volver a analizar para ver resultados",
    "鲁大师-高温日志": "LuDaShi - Registro de alta temperatura",
    "查看硬件高温历史，进一步了解您的电脑": "Ver historial de alta temperatura del hardware",
    "时间": "Tiempo",
    "全部": "Todos",
    "类型": "Tipo",
    "报警温度": "Temperatura de alarma",
    "预警阈值": "Umbral de alerta",
    "暂时未发现高温历史，请继续保持。": "No se encontró historial de alta temperatura, siga así.",
    "硬盘": "Disco duro",
    "数据统计时间截止到：2017-11-12 12:00:00": "Estadísticas hasta: 2017-11-12 12:00:00",
    "清空所有": "Limpiar todo",
    
    # === GamePage ===
    "努力加载中...": "Cargando...",
    "网络无法连接，请检查网络是否正常": "No se puede conectar, verifique su red",
    "正在扫描游戏补丁": "Escaneando parches de juegos",
    "正在检测是否安装DirectX...": "Detectando si DirectX está instalado...",
    "运行库检测": "Detección de librerías",
    "硬件性能": "Rendimiento de hardware",
    "CPU性能": "Rendimiento de CPU",
    "显卡性能": "Rendimiento de GPU",
    "游戏性能：": "Rendimiento de juegos:",
    "内存性能": "Rendimiento de memoria",
    "您的电脑还没有进行游戏环境检测，建议立即检测": "Aún no se ha detectado el entorno de juegos, se recomienda detectar ahora",
    "检测运行库可以帮您解决游戏无法正确运行的问题": "Detectar librerías puede resolver problemas de ejecución de juegos",
    
    # === LdsLite ===
    "小鲁温度监控": "Monitor de temperatura LuDaShi",
    "电脑温度过高会导致运行不畅，影响硬件的使用寿命，甚至导致高温烧毁": "La temperatura excesiva causa lentitud, reduce la vida útil del hardware y puede causar daños",
    "已启用Ahorro de energía模式": "Modo de Ahorro de energía activado",
    "已启用节能降温模式": "Modo de Ahorro de energía activado",
    "已关闭多余的进程": "Se cerraron procesos innecesarios",
    "360极速浏览器": "Navegador 360",
    "已开启温度保护": "Protección de temperatura activada",
    "当CPU温度超过": "Cuando la temperatura del CPU supere",
    "当硬件温度超过特定值时自动报警": "Alarma automática al superar la temperatura límite",
    "℃时自动报警": "°C alarma automática",
    "当显卡温度超过": "Cuando la temperatura de la GPU supere",
    "当硬盘温度超过": "Cuando la temperatura del disco supere",
    "当主板温度超过": "Cuando la temperatura de la placa base supere",
    "当电池温度超过": "Cuando la temperatura de la batería supere",
    "网卡负载": "Carga de red",
    
    # === Fix partial translations (mixed Chinese+Spanish) ===
    "浏览器Protección de página de inicio，保护您的主页，防止被恶意篡改": "Proteger la página de inicio del navegador contra modificaciones maliciosas",
    "关闭Protección de página de inicio功能": "Desactivar Protección de página de inicio",
    "自动优化内存后，告知我Optimización de memoria结果": "Después de optimizar, informarme del resultado",
    "帮你快速打开Sitios frecuentes": "Acceso rápido a tus sitios frecuentes",
    
    # === CleanPage / BenchmarkPage / main_wnd (in default_theme) ===
    "全面体检": "Análisis completo",
    "性能跑分": "Prueba de rendimiento",
    "垃圾清理": "Limpieza de basura",
    "优化加速": "Optimizar y acelerar",
    "温度管理": "Gestión de temperatura",
    "游戏助手": "Asistente de juegos",
    "硬件检测": "Detección de hardware",
    "驱动管理": "Gestión de controladores",
    "我的鲁大师": "Mi LuDaShi",
    "关于": "Acerca de",
    "检查更新": "Buscar actualizaciones",
    "意见反馈": "Comentarios",
    "进入官网": "Ir al sitio web",
    "登录": "Iniciar sesión",
    
    # === Previous translations (to also apply to newly extracted files) ===
    "常规：": "General:",
    "常规": "General",
    "显示内存释放器（悬浮的加速球）": "Mostrar liberador de memoria (bola flotante)",
    "显示任务栏标尺": "Mostrar indicador en barra de tareas",
    "开机时自动启用硬件实时防护（核心功能，建议开启）": "Activar protección de hardware en tiempo real al iniciar (función principal, recomendado)",
    "显示电脑健康监控面板": "Mostrar panel de monitoreo de salud del PC",
    "当硬件温度高于以下阈值时自动报警（报警阈值可手动修改）": "Alarma automática cuando la temperatura del hardware supere el umbral (modificable manualmente)",
    "硬件防护：": "Protección de hardware:",
    "硬件防护": "Protección de hardware",
    "全屏模式下即使硬件温度过高也不报警": "No alertar por alta temperatura en modo pantalla completa",
    "高温报警时，自动播放以下声音提示": "Al alertar por alta temperatura, reproducir el siguiente sonido",
    "处理器": "Procesador",
    "开启硬盘温度监控,每": "Activar monitoreo de temperatura del disco duro, cada",
    "秒检测一次(1-99s)": "segundos verificar una vez (1-99s)",
    "报警音效": "Sonido de alarma",
    "主页防护：": "Protección de página de inicio:",
    "主页防护": "Protección de página de inicio",
    "浏览器主页防护，保护您的主页，防止被恶意篡改": "Proteger la página de inicio del navegador contra modificaciones maliciosas",
    "启用360安全上网导航（hao.360.cn）": "Activar navegación segura 360 (hao.360.cn)",
    "自定义锁定：": "Bloqueo personalizado:",
    "关闭主页防护功能": "Desactivar protección de página de inicio",
    "手动优化内存时，自动清空剪切板": "Al optimizar memoria manualmente, vaciar portapapeles automáticamente",
    "内存优化：": "Optimización de memoria:",
    "内存优化": "Optimización de memoria",
    "当物理内存负载超过百分之": "Cuando la carga de memoria física exceda el",
    "自动优化内存后，告知我内存优化结果": "Después de optimizar, informarme del resultado",
    "时自动优化内存": "% optimizar memoria automáticamente",
    "仅在系统空闲时，才执行内存自动优化功能": "Optimizar memoria automáticamente solo cuando el sistema esté inactivo",
    "每次自动优化内存的间隔时间：": "Intervalo entre optimizaciones automáticas:",
    "关闭回收站右键菜单入口": "Desactivar entrada del menú contextual de la papelera",
    "电脑空闲时提醒我清理垃圾": "Recordarme limpiar cuando el PC esté inactivo",
    "垃圾清理：": "Limpieza de basura:",
    "智能降温模式下即使温度过高也不报警": "No alertar por alta temperatura en modo de enfriamiento inteligente",
    "节能降温：": "Ahorro de energía:",
    "节能降温": "Ahorro de energía",
    "根据显示器类型自动选用节能壁纸": "Seleccionar automáticamente fondo de ahorro de energía según el monitor",
    "关闭屏幕保护程序": "Desactivar protector de pantalla",
    "自动调低显示器亮度": "Reducir automáticamente el brillo del monitor",
    "自定义电脑的待机时间：": "Personalizar tiempo de espera del PC:",
    "自定义显示器关闭时间：": "Personalizar tiempo de apagado del monitor:",
    "开启病毒防护功能": "Activar protección antivirus",
    "病毒查杀：": "Análisis de virus:",
    "病毒查杀": "Análisis de virus",
    "增值业务：": "Servicios adicionales:",
    "增值业务": "Servicios adicionales",
    "鲁大师是一款免费的软件，有您的支持我们将走的更远": "LuDaShi es un software gratuito, con su apoyo llegaremos más lejos",
    "停止接收推广信息（鲁大师新功能等官方通知除外）": "Dejar de recibir promociones (excepto notificaciones oficiales)",
    "其它设置：": "Otros ajustes:",
    "其它设置": "Otros ajustes",
    "安卓手机连接时，不安装手机助手组件": "No instalar componentes del asistente al conectar un celular Android",
    "安卓手机连接时，不再显示手机助手悬浮窗": "No mostrar ventana flotante del asistente al conectar un celular Android",
    "当有可用的新版本时提醒我": "Avisarme cuando haya una nueva versión disponible",
    "屏蔽广告弹窗": "Bloquear ventanas emergentes de publicidad",
    "恢复默认": "Restaurar predeterminado",
    "常用网址": "Sitios frecuentes",
    "帮你快速打开常用网址": "Acceso rápido a tus sitios frecuentes",
    "新功能推荐（通过主界面推送等方式提示）": "Recomendación de nuevas funciones (notificaciones en la interfaz)",
    "开启后可不定期收到产品优化、内测试用等提醒": "Al activar, recibirás recordatorios de optimización y pruebas del producto",
    "正在进行清理优化,您确定要退出吗?": "Se está realizando una optimización. ¿Desea salir?",
    "硬件：英特尔 Core i7-6700": "Hardware: Intel Core i7-6700",
    "阈值：": "Umbral:",
    "摄氏度": "°C (Celsius)",
    "设置无效，请重试": "Configuración inválida, intente de nuevo",
}

def translate_xml(file_path, translations):
    """Replace Chinese strings in a UTF-16 XML file."""
    for enc in ["utf-16", "utf-8"]:
        try:
            with open(file_path, "r", encoding=enc) as f:
                content = f.read()
            break
        except:
            continue
    else:
        return False
    
    modified = False
    for chinese, spanish in translations.items():
        if chinese in content:
            content = content.replace(chinese, spanish)
            modified = True
    
    if modified:
        with open(file_path, "w", encoding=enc) as f:
            f.write(content)
        print(f"  [TRANSLATED] {os.path.basename(file_path)}")
    return modified

# Re-extract all .ui files fresh
print("PASO 1: Re-extrayendo archivos .ui...")
ui_dirs = {}

for root, dirs, files in os.walk(ludashi_themes):
    for f in files:
        if f.endswith(".ui"):
            src = os.path.join(root, f)
            rel = os.path.relpath(root, ludashi_themes)
            extract_to = os.path.join(work_dir, "final_extracted", rel, f.replace(".ui", ""))
            os.makedirs(extract_to, exist_ok=True)
            try:
                with zipfile.ZipFile(src, "r") as zf:
                    zf.extractall(extract_to)
                ui_dirs[src] = extract_to
                print(f"  Extracted: {os.path.relpath(src, ludashi_themes)}")
            except Exception as e:
                print(f"  SKIP: {f} - {e}")

# Also DrvMgr
drvmgr_src = r"C:\Program Files (x86)\LuDaShi\DrvMgr\config\defaultskin\defaultskin.ui"
drvmgr_fb = r"C:\Program Files (x86)\LuDaShi\DrvMgr\feedback\LuDaShiFeedback.ui"
for src in [drvmgr_src, drvmgr_fb]:
    if os.path.exists(src):
        extract_to = os.path.join(work_dir, "final_extracted", "DrvMgr", os.path.basename(src).replace(".ui", ""))
        os.makedirs(extract_to, exist_ok=True)
        try:
            with zipfile.ZipFile(src, "r") as zf:
                zf.extractall(extract_to)
            ui_dirs[src] = extract_to
            print(f"  Extracted: DrvMgr/{os.path.basename(src)}")
        except Exception as e:
            print(f"  SKIP: {os.path.basename(src)} - {e}")

# Step 2: Apply translations to ALL xml files
print("\nPASO 2: Aplicando traducciones completas...")
total = 0
for src, extract_dir in ui_dirs.items():
    for xml_file in glob.glob(os.path.join(extract_dir, "**", "*.xml"), recursive=True):
        if translate_xml(xml_file, translations):
            total += 1

print(f"\n  Total archivos traducidos: {total}")

# Step 3: Repackage
print("\nPASO 3: Reempaquetando...")
repack_dir = os.path.join(work_dir, "final_repacked")
os.makedirs(repack_dir, exist_ok=True)

for src, extract_dir in ui_dirs.items():
    if "DrvMgr" in src:
        out_path = os.path.join(repack_dir, "DrvMgr", os.path.basename(src))
    else:
        rel = os.path.relpath(src, ludashi_themes)
        out_path = os.path.join(repack_dir, "Themes", rel)
    
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    
    with zipfile.ZipFile(out_path, "w", zipfile.ZIP_STORED) as zf:
        for root, dirs, files in os.walk(extract_dir):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, extract_dir)
                zf.write(file_path, arcname)
    
    print(f"  {os.path.relpath(out_path, repack_dir)}")

# Count remaining Chinese
print("\nPASO 4: Verificando cadenas restantes...")
remaining = 0
for src, extract_dir in ui_dirs.items():
    for xml_file in glob.glob(os.path.join(extract_dir, "**", "*.xml"), recursive=True):
        for enc in ["utf-16", "utf-8"]:
            try:
                with open(xml_file, "r", encoding=enc) as f:
                    txt = f.read()
                break
            except:
                continue
        else:
            continue
        for match in re.findall(r'title="([^"]+)"', txt) + re.findall(r'tip="([^"]+)"', txt):
            if any("\u4e00" <= c <= "\u9fff" for c in match):
                remaining += 1

print(f"  Cadenas chinas restantes en títulos: {remaining}")
print(f"\nArchivos finales en: {repack_dir}")
