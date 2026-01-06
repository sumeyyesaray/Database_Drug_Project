CREATE VIEW view_medicine_full_details AS
SELECT 
    m.medicine_name,
    d.dosage_amount,
    m.form_id, -- Tablet, Şurup vb.
    m.therapeutic_class_id
FROM medicine m
LEFT JOIN dosage d ON m.dosage_id = d.dosage_id;

SELECT * FROM view_medicine_full_details;



CREATE VIEW view_medicine_substitutes AS
SELECT DISTINCT 
    m.medicine_name AS ana_ilac,
    s.substitute_name AS muadil_ilac
FROM medicine m
JOIN medicine_has_substitutes mhs ON m.medicine_id = mhs.medicine_id
JOIN substitutes s ON mhs.substitute_id = s.substitute_id;
SELECT * FROM view_medicine_substitutes;