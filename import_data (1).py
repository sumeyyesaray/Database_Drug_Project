import pandas as pd
from sqlalchemy import create_engine, text
import os

# ==========================================
# 1. VERİTABANI BAĞLANTISI
# ==========================================
DB_USER = 'root'
DB_PASS = '123456'  # <-- BURAYA KENDİ ŞİFRENİ YAZ
DB_HOST = 'localhost'
DB_NAME = 'medicine_final1'

# Bağlantı motoru
engine = create_engine(f"mysql+pymysql://{DB_USER}:{DB_PASS}@{DB_HOST}/{DB_NAME}?charset=utf8mb4")

# ==========================================
# 2. AYARLAR
# ==========================================
DEFAULT_FK_ID = 0

# Boşsa 0 ile doldurulacak Foreign Key sütunları
# NOT: Artık doğru yazım olan 'therapeutic' kullanılıyor.
fk_columns_to_fill = [
    'chemical_class_id',
    'therapeutic_class_id',
    'habit_forming_id',
    'form_id',
    'dosage_id',
    'unit_id',
    'action_class_id',
    'subtype_id'
]

# Dosya -> Tablo Eşleşmesi
file_table_mapping = {
    'ChemicalClasses': 'ChemicalClasses',
    'TherapeuticClass': 'TherapeuticClass',
    'MedicineForms': 'MedicineForms',
    'DosageUnits': 'DosageUnits',
    'Dosage': 'Dosage',
    'Habit_Forming': 'Habit_Forming',
    'SideEffects': 'SideEffect',
    'ActionClass': 'ActionClasses',
    'Uses': 'Uses',
    'ActionSubtype': 'ActionSubtype',
    'Substitutes': 'Substitutes',
    'Medicine': 'Medicine',
    'Medicine_has_SideEffects': 'Medicine_has_SideEffect',
    'Medicine_has_Uses': 'Medicine_has_Uses',
    'Medicine_has_ActionClass': 'Medicine_has_ActionClass',
    'Medicine_has_Substitutes': 'Medicine_has_Substitutes'
}

# Yükleme Sırası (Foreign Key kurallarına uygun)
import_order = [
    'ChemicalClasses', 'TherapeuticClass', 'MedicineForms', 'DosageUnits',
    'Dosage', 'Habit_Forming', 'SideEffects', 'ActionClass', 'Uses',
    'ActionSubtype', 'Substitutes', 'Medicine',
    'Medicine_has_SideEffects', 'Medicine_has_Uses',
    'Medicine_has_ActionClass', 'Medicine_has_Substitutes'
]


def import_clean_data():
    folder_path = '.'
    print(f"--- Veri Aktarımı Başlıyor (Varsayılan ID: {DEFAULT_FK_ID}) ---\n")

    # SQL Strict Mode'u devre dışı bırak (0 ID'si ve diğer kısıtlamalar için)
    with engine.connect() as conn:
        conn.execute(text("SET SQL_MODE = 'NO_AUTO_VALUE_ON_ZERO'"))

    for file_name in import_order:
        table_name = file_table_mapping[file_name]

        # Dosya yollarını kontrol et
        csv_path = os.path.join(folder_path, f"{file_name}.csv")
        xlsx_path = os.path.join(folder_path, f"{file_name}.xlsx")

        file_path = csv_path if os.path.exists(csv_path) else (xlsx_path if os.path.exists(xlsx_path) else None)

        if file_path:
            try:
                # 1. DOSYAYI OKU (Noktalı Virgül Düzeltmesi)
                if file_path.endswith('.csv'):
                    # sep=';' -> CSV'lerin noktalı virgül ile ayrıldığını belirtir.
                    df = pd.read_csv(file_path, sep=';', encoding='utf-8-sig', on_bad_lines='skip')
                else:
                    df = pd.read_excel(file_path)

                # 2. SÜTUN İSİMLERİNİ TEMİZLE
                # " id " gibi boşluklu gelen sütun adlarını "id" yapar.
                df.columns = df.columns.str.strip()

                # 3. BOŞ FOREIGN KEY DEĞERLERİNİ 0 YAP
                for col in df.columns:
                    if col in fk_columns_to_fill:
                        # Sütun tamamen boşsa veya eksik veri varsa
                        if df[col].isna().sum() > 0:
                            df[col] = df[col].fillna(DEFAULT_FK_ID)

                            # Sayısal olmayan karakterleri temizle ve integer yap
                            # 'coerce' hatalı veriyi NaN yapar, sonra tekrar 0 doldururuz
                            df[col] = pd.to_numeric(df[col], errors='coerce').fillna(DEFAULT_FK_ID).astype(int)

                            print(f"   ℹ️ {file_name} -> '{col}' sütunundaki boşluklar {DEFAULT_FK_ID} ile dolduruldu.")

                # 4. VERİTABANINA AKTAR
                # if_exists='append': Var olan tablonun altına ekle
                df.to_sql(table_name, con=engine, if_exists='append', index=False)

                print(f"✅ BAŞARILI: {file_name} -> {table_name} ({len(df)} kayıt)")

            except Exception as e:
                print(f"❌ HATA: {file_name} yüklenirken sorun oluştu.")
                print(f"   Detay: {e}")
        else:
            print(f"⚠️ Dosya Bulunamadı: {file_name}")

    print("\n--- İşlem Tamamlandı ---")


if __name__ == "__main__":
    import_clean_data()