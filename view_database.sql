USE medicine_news;

CREATE VIEW v_medicine_overview AS
SELECT
    m.medicine_id,
    m.medicine_name,
    cc.class_name AS chemical_class,
    tc.class_name AS therapeutic_class,
    ac.class_name AS action_class,
    hf.habit_label AS habit_forming
FROM medicine m
LEFT JOIN chemicalclasses  cc ON m.chemical_class_id    = cc.chemical_class_id
LEFT JOIN therapeuticclass tc ON m.therapeutic_class_id = tc.therapeutic_class_id
LEFT JOIN actionclass      ac ON m.action_class_id      = ac.action_class_id
LEFT JOIN habit_forming    hf ON m.habit_forming_id     = hf.habit_forming_id;
