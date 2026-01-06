DELIMITER //

CREATE PROCEDURE sp_GetMedicineForm(
    IN p_med_name VARCHAR(250),  -- Dışarıdan gelen veri
    OUT p_form_name VARCHAR(50)  -- Dışarıya gönderilen sonuç
)
BEGIN
    -- İlaç ismine göre Medicine tablosunu ve MedicineForms tablosunu bağlayıp formu buluyoruz
    SELECT mf.form_name INTO p_form_name
    FROM Medicine m
    JOIN MedicineForms mf ON m.form_id = mf.form_id
    WHERE m.medicine_name = p_med_name;
END //

DELIMITER ;

DELIMITER //

CREATE PROCEDURE sp_UpdateStockValue(
    INOUT p_quantity INT  -- Hem girdi hem çıktı
)
BEGIN
    -- Elimizdeki sayıya (örneğin sevkiyat geldiğinde) 10 adet ekleyelim
    SET p_quantity = p_quantity + 10;
END //

DELIMITER ;

-- 1. Prosedür Testi (IN/OUT)
CALL sp_GetMedicineForm('Aspirin', @sonuc_form);
SELECT @sonuc_form; -- Ekranda 'Tablet' yazar.

-- 2. Prosedür Testi (INOUT)
SET @stok_miktari = 50;
CALL sp_UpdateStockValue(@stok_miktari);
SELECT @stok_miktari; -- Ekranda '60' yazar.