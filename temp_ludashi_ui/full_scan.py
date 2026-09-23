import os, re, glob, json, zipfile, shutil, struct

work_dir = r"C:\Users\LENOVO\Desktop\web_itech\temp_ludashi_ui"
ludashi_dir = r"C:\Program Files (x86)\LuDaShi"

# ============================================================
# PARTE 1: Buscar TODOS los textos chinos en TODOS los archivos legibles
# ============================================================
print("=" * 70)
print("PARTE 1: BARRIDO COMPLETO DE TEXTOS CHINOS")
print("=" * 70)

all_chinese_found = {}

# 1A: Search all DLLs and EXEs for Chinese text
print("\n--- Buscando en DLLs y EXEs ---")
for root, dirs, files in os.walk(ludashi_dir):
    for fname in files:
        if not fname.lower().endswith(('.dll', '.exe')):
            continue
        fpath = os.path.join(root, fname)
        try:
            with open(fpath, 'rb') as f:
                data = f.read()
        except:
            continue
        
        text = data.decode('utf-16-le', errors='ignore')
        # Find all Chinese sequences
        chinese_seqs = re.findall(r'[\u4e00-\u9fff\u3000-\u303f\uff00-\uffef]{2,}', text)
        if chinese_seqs:
            unique = set(chinese_seqs)
            # Filter to meaningful strings (length >= 2)
            meaningful = [s for s in unique if len(s) >= 2]
            if meaningful:
                rel = os.path.relpath(fpath, ludashi_dir)
                all_chinese_found[rel] = meaningful
                print(f"  {rel}: {len(meaningful)} cadenas")

# 1B: Search all JSON files
print("\n--- Buscando en archivos JSON ---")
for root, dirs, files in os.walk(ludashi_dir):
    for fname in files:
        if not fname.lower().endswith('.json'):
            continue
        fpath = os.path.join(root, fname)
        try:
            with open(fpath, 'r', encoding='utf-8') as f:
                content = f.read()
        except:
            continue
        
        chinese = re.findall(r'[\u4e00-\u9fff]{2,}', content)
        if chinese:
            rel = os.path.relpath(fpath, ludashi_dir)
            print(f"  {rel}: {list(set(chinese))[:5]}")
            all_chinese_found[rel] = list(set(chinese))

# 1C: Search all XML files  
print("\n--- Buscando en archivos XML ---")
for root, dirs, files in os.walk(ludashi_dir):
    for fname in files:
        if not fname.lower().endswith('.xml'):
            continue
        fpath = os.path.join(root, fname)
        for enc in ['utf-16', 'utf-8', 'gbk']:
            try:
                with open(fpath, 'r', encoding=enc) as f:
                    content = f.read()
                break
            except:
                continue
        else:
            continue
        
        chinese = re.findall(r'[\u4e00-\u9fff]{2,}', content)
        if chinese:
            rel = os.path.relpath(fpath, ludashi_dir)
            print(f"  {rel}: {list(set(chinese))[:5]}")

# 1D: Search SuperApp JSON files specifically
print("\n--- SuperApp JSON files ---")
superapp_dir = os.path.join(ludashi_dir, "SuperApp")
if os.path.exists(superapp_dir):
    for root, dirs, files in os.walk(superapp_dir):
        for fname in files:
            if not fname.endswith('.json'):
                continue
            fpath = os.path.join(root, fname)
            try:
                with open(fpath, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                content = json.dumps(data, ensure_ascii=False)
                chinese = re.findall(r'[\u4e00-\u9fff]{2,}', content)
                if chinese:
                    rel = os.path.relpath(fpath, ludashi_dir)
                    print(f"  {rel}:")
                    for c in list(set(chinese))[:8]:
                        print(f"    {c}")
            except Exception as e:
                pass

# ============================================================
# PARTE 2: Contar total
# ============================================================
total_strings = sum(len(v) for v in all_chinese_found.values())
print(f"\n\nTotal archivos con texto chino: {len(all_chinese_found)}")
print(f"Total cadenas chinas únicas: {total_strings}")
