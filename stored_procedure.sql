DELIMITER $$
CREATE PROCEDURE sp_medicine_stats (
    IN    p_medicine_name     VARCHAR(500),
    INOUT p_medicine_id       INT,
    OUT   p_substitute_count  INT,
    OUT   p_side_effect_count INT
    )
BEGIN
    -- ID verilmemişse isimden bul
    IF p_medicine_id IS NULL OR p_medicine_id = 0 THEN
        SELECT m.medicine_id
        INTO p_medicine_id
        FROM medicine m
        WHERE m.medicine_name = p_medicine_name
        LIMIT 1;
    END IF;
    -- Eğer ilaç bulunamazsa sonuçları sıfırla
    IF p_medicine_id IS NULL THEN
        SET p_substitute_count  = 0;
        SET p_side_effect_count = 0;
    ELSE
        -- Muadil sayısı
        SELECT COUNT(DISTINCT ms.substitute_id)
        INTO p_substitute_count
        FROM medicine_has_substitutes ms
        WHERE ms.medicine_id = p_medicine_id;
        -- Yan etki sayısı
        SELECT COUNT(DISTINCT se.side_effect_id)
        INTO p_side_effect_count
        FROM medicine_has_side_effect se
        WHERE se.medicine_id = p_medicine_id;
    END IF;
END$$
DELIMITER ;
