import csv
import mysql.connector
import sys

# MySQL bağlantı bilgilerini ayarla
config = {
    'user': 'root',           # Kullanıcı adınız
    'password': 'Sumeyye.03',   # Şifreniz
    'host': 'localhost',
    'database': 'medicine_database',
    'charset': 'utf8'
}

def clean_int(value, is_required=False):
    """
    Integer değeri temizle
    is_required=True ise boş olamaz (örn: medicine_id)
    is_required=False ise boşsa 0 döner (örn: foreign key'ler)
    """
    if value is None or value == '' or str(value).strip() == '':
        return 0 if not is_required else None
    
    value = str(value).strip()
    
    # Tırnak işaretlerini temizle
    if value.startswith('"') and value.endswith('"'):
        value = value[1:-1]
    
    try:
        return int(value)
    except:
        return 0 if not is_required else None

def clean_str(value):
    """String değeri temizle"""
    if value is None:
        return ''
    value = str(value).strip()
    if value.startswith('"') and value.endswith('"'):
        value = value[1:-1]
    return value

try:
    # MySQL'e bağlan
    connection = mysql.connector.connect(**config)
    cursor = connection.cursor()
    
    print("MySQL'e bağlandı...")
    
    # Önce tabloyu temizlemek ister misiniz?
    clear_table = input("Tabloyu temizlemek istiyor musunuz? (e/h): ").lower()
    if clear_table == 'e':
        cursor.execute("DELETE FROM medicine")
        connection.commit()
        print("Mevcut veriler temizlendi...")
    
    # CSV dosyasını oku - Noktalı virgül ile ayır
    csv_file = 'c://Users//Sümeyye//Desktop//data_csv//Medicine.csv'
    inserted_count = 0
    error_count = 0
    batch_size = 1000  # Toplu işlem boyutu
    
    with open(csv_file, 'r', encoding='utf-8') as file:
        # Noktalı virgül ile CSV reader oluştur
        csv_reader = csv.reader(file, delimiter=';')
        
        # Başlık satırını oku
        headers = next(csv_reader)
        print(f"CSV Başlıkları: {headers}")
        
        # Toplu ekleme için liste
        batch_values = []
        
        # Her satırı işle
        for row_num, row in enumerate(csv_reader, start=2):
            try:
                # Satırda yeterli sütun var mı kontrol et
                if len(row) != 8:
                    print(f"Uyarı: Satır {row_num} - {len(row)} sütun (beklenen: 8)")
                    # Eksik sütunları tamamla
                    while len(row) < 8:
                        row.append('')
                
                # İlk 3 satırı debug için göster
                if row_num <= 4:
                    print(f"DEBUG Satır {row_num}: {row}")
                
                # Değerleri temizle ve eşleştir
                # NOT NULL olanlar: medicine_id (zorunlu)
                # NULL olabilip 0 yapılacaklar: foreign key'ler
                
                medicine_id = clean_int(row[0], is_required=True)
                if medicine_id is None:
                    print(f"Hata: Satır {row_num} - medicine_id boş!")
                    error_count += 1
                    continue
                
                medicine_name = clean_str(row[1])
                if not medicine_name:
                    print(f"Uyarı: Satır {row_num} - medicine_name boş, id: {medicine_id}")
                
                # Foreign key'ler - boşsa 0
                dosage_id = clean_int(row[2], is_required=False)  # boşsa 0
                unit_id = clean_int(row[3], is_required=False)    # boşsa 0  
                form_id = clean_int(row[4], is_required=False)    # boşsa 0
                chemical_class_id = clean_int(row[5], is_required=False)  # boşsa 0
                therapeutic_class_id = clean_int(row[6], is_required=False)  # boşsa 0
                habit_forming_id = clean_int(row[7], is_required=False)  # boşsa 0
                
                # Tablonuzdaki sütun isimlerine göre SQL
                # Eğer tablonuzda habit_forming_id yoksa, action_class_id'ye ata
                sql = """
                INSERT INTO medicine 
                (medicine_id, medicine_name, dosage_id, unit_id, form_id, 
                 chemical_class_id, therapeutic_class_id, action_class_id)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                """
                
                # Parametreler
                params = (
                    medicine_id, medicine_name, dosage_id, unit_id, 
                    form_id, chemical_class_id, therapeutic_class_id, habit_forming_id
                )
                
                # Toplu işlem için ekle
                batch_values.append(params)
                
                # Batch dolunca execute et
                if len(batch_values) >= batch_size:
                    cursor.executemany(sql, batch_values)
                    inserted_count += len(batch_values)
                    batch_values = []
                    
                    # İlerlemeyi göster
                    print(f"{inserted_count} kayıt eklendi...")
                    
            except Exception as e:
                error_count += 1
                print(f"Satır {row_num} hata: {str(e)[:100]}")
                if row_num <= 10:  # İlk 10 hatayı detaylı göster
                    import traceback
                    traceback.print_exc()
                continue
        
        # Kalan batch'i kaydet
        if batch_values:
            cursor.executemany(sql, batch_values)
            inserted_count += len(batch_values)
        
        # Tüm değişiklikleri kaydet
        connection.commit()
        
        print(f"\n" + "="*50)
        print(f"İŞLEM TAMAMLANDI!")
        print(f"Başarılı: {inserted_count} kayıt")
        print(f"Hatalı: {error_count} satır")
        print(f"Toplam işlenen: {inserted_count + error_count} satır")
        
        # Toplam kayıt sayısını göster
        cursor.execute("SELECT COUNT(*) FROM medicine")
        total = cursor.fetchone()[0]
        print(f"Tablonun yeni toplam kayıt sayısı: {total}")
        
        # Örnek verileri göster
        cursor.execute("SELECT * FROM medicine LIMIT 5")
        sample = cursor.fetchall()
        print(f"\nİlk 5 kayıt örneği:")
        for record in sample:
            print(f"  ID: {record[0]}, İsim: {record[1][:20]}, Dosage: {record[2]}, Unit: {record[3]}")
        
except mysql.connector.Error as err:
    print(f"MySQL hatası: {err}")
    sys.exit(1)
    
except FileNotFoundError:
    print(f"CSV dosyası bulunamadı: {csv_file}")
    sys.exit(1)
    
except Exception as e:
    print(f"Beklenmeyen hata: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
    
finally:
    # Bağlantıyı kapat
    if 'connection' in locals() and connection.is_connected():
        cursor.close()
        connection.close()
        print("\nMySQL bağlantısı kapatıldı.")