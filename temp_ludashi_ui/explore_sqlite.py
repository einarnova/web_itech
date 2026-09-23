import sqlite3, os

db_path = r"C:\Users\LENOVO\Desktop\web_itech\temp_ludashi_ui\ComputerZ_copy.dat"

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# List all tables
cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
tables = cursor.fetchall()
print("=== TABLAS ===")
for t in tables:
    print(f"  {t[0]}")
    # Show schema
    cursor.execute(f"PRAGMA table_info({t[0]})")
    cols = cursor.fetchall()
    for col in cols:
        print(f"    {col[1]} ({col[2]})")
    # Count rows
    try:
        cursor.execute(f"SELECT COUNT(*) FROM {t[0]}")
        count = cursor.fetchone()[0]
        print(f"    -> {count} rows")
    except:
        pass

# Search for Chinese text in all text columns
print("\n=== BUSCANDO TEXTO CHINO ===")
targets = ["硬件体检", "硬件参数", "电脑优化", "开始体检", "清理优化", "驱动检测", "建议立即体检"]

for table in tables:
    tname = table[0]
    cursor.execute(f"PRAGMA table_info({tname})")
    cols = cursor.fetchall()
    text_cols = [c[1] for c in cols if c[2] in ("TEXT", "VARCHAR", "CHAR", "")]
    
    for col in text_cols:
        try:
            cursor.execute(f"SELECT {col} FROM {tname} WHERE {col} IS NOT NULL LIMIT 500")
            rows = cursor.fetchall()
            for row in rows:
                val = str(row[0])
                for t in targets:
                    if t in val:
                        print(f"\n  Tabla: {tname}, Columna: {col}")
                        print(f"  Valor: {val[:200]}")
        except Exception as e:
            pass

# Also show sample data from each table
print("\n=== DATOS DE EJEMPLO ===")
for table in tables:
    tname = table[0]
    try:
        cursor.execute(f"SELECT * FROM {tname} LIMIT 3")
        rows = cursor.fetchall()
        if rows:
            print(f"\n  {tname}:")
            for row in rows:
                print(f"    {str(row)[:300]}")
    except:
        pass

conn.close()
