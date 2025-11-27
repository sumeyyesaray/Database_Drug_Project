# 💊 DrugMatrix – Multi-Feature Medicine Analytics System
A relational database system designed to analyze large-scale pharmaceutical data, including medicines, usages, side effects, substitutes, chemical classes, therapeutic classes, action classes, and habit-forming information.

This project was developed as part of the **DBMS Project Phase I** requirements.

---

## 📌 Project Overview
DrugMatrix is a normalized relational database built using **MySQL 8.0** and **MySQL Workbench**.  
The system enables efficient querying of pharmaceutical properties, multi-valued attributes, and classification-based analyses.

The dataset used includes:
- **248,218 records**
- **58 columns**
- Rich multi-valued fields (side effects, usages, substitutes)

Dataset Link  
🔗 https://www.kaggle.com/datasets/shudhanshusingh/250k-medicines-usage-side-effects-and-substitutes

---

## 👥 Team Members
- **Sinan Kaçar – 220709053**  
- **Sümeyye Saray – 220709070**  
- **Hakan Belen – 220709029**

---

## 🗂 Database Contents
The project includes:
- ER Diagram
- SQL file containing:
  - Table creation scripts  
  - Sample data inserts  
  - 5 analytical queries using GROUP BY  
  - View definition  
  - Stored procedure with IN–OUT–INOUT parameters  

---

## 🧬 ER Diagram
The relational model is centered around the **Medicine** table and supported by the following entities:

- **ChemicalClasses**
- **TherapeuticClass**
- **ActionClass**
- **Habit_Forming**
- **Usages**
- **Side_Effect**
- **Substitutes**

Multi-valued attributes (side effects, usages, substitutes) are represented using associative junction tables:

- `Medicine_has_Usage`
- `Medicine_has_Side_Effect`
- `Medicine_has_Substitutes`

All relationships follow proper PK–FK constraints ensuring referential integrity.


``

---

## 🔬(Target Analytical Queries

DrugMatrix sistemi, ilaç verileri üzerinde anlamlı çıkarımlar yapmak üzere tasarlanmış 10 ana analitik soruyu yanıtlayabilir. [cite_start]Bu soruların tümü, `GROUP BY` yan cümlesi ile birlikte en az bir Aggregate Fonksiyonu (`COUNT`, `AVG`, `MIN`, `MAX`) kullanır[cite: 195].

1.  Her bir ilaç için kaydedilen toplam yan etki sayısı.
2.  Her bir ilaç için kaydedilen kullanım (endikasyon) sayısı.
3.  [cite_start]Her bir ilaç için mevcut olan muadil (substitute) sayısı[cite: 20].
4.  [cite_start]Her bir terapötik sınıfa ait olan ilaç sayısı[cite: 21].
5.  [cite_start]Her bir terapötik sınıf için ilaç başına ortalama, minimum ve maksimum yan etki sayısı[cite: 22].
6.  [cite_start]Her bir etki sınıfı (action class) için ilişkili ilaç sayısı ve toplamdaki farklı yan etki sayısı[cite: 23].
7.  [cite_start]Her bir alışkanlık yapıcı kategori ("Yes" / "No") için ilaç sayısı ve ilaç başına ortalama muadil sayısı[cite: 24].
8.  [cite_start]Her bir yan etki için bu yan etkiye sahip olan farklı ilaç sayısı[cite: 25].
9.  [cite_start]Her bir kullanım (endikasyon) için bu amaçla kullanılan ilaç sayısı[cite: 26].
10. [cite_start]Her bir kimyasal sınıfa ait ilaç sayısı ve bu ilaçlar arasındaki maksimum muadil sayısı[cite: 27].

---

## 🛠 Technologies Used

Bu projenin geliştirilmesi ve uygulanması için aşağıdaki teknolojiler ve ortamlar kullanılmıştır:

| Bileşen | Özellik / Sürüm |
| :--- | :--- |
| **İşletim Sistemi** | Windows 11 |
| **Veritabanı Motoru** | MySQL Community Server 8.0.43 |
| **Veritabanı Tasarımı** | MySQL Workbench |
| **İşlemci (CPU)** | Intel-based Multi-Core Processor |
| **Bellek (RAM)** | 16 GB |
| **Depolama** | Local SSD |
| **Veri Seti Kaynağı** | Kaggle – 250k Medicines Dataset |



## 📌 Key Features

* Tamamen **normalize edilmiş** ilişkisel şema tasarımı[cite: 9].
* Çok değerli öznitelikler (Yan Etkiler, Kullanımlar, Muadiller) için **Junction tabloları** kullanılması[cite: 90, 91, 92].
* Kompleks analizler için `GROUP BY` içeren **Analitik SQL sorguları**[cite: 203].
* Özelleştirilmiş veri perspektifi sunan **View** ve verimli veri işleme sağlayan **Stored Procedure** uygulamaları[cite: 208].
* **MySQL 8.0** ile tam uyumluluk.


## 📞 Contact

Proje ile ilgili sorularınız için iletişime geçebilirsiniz:

* **Sümeyye Saray**
* **E-posta:** sumeyyesaray@posta.mu.edu.tr
