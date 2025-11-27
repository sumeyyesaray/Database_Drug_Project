-- Query1: Average side effects per therapeutic class
SELECT 
    tc.class_name AS therapeutic_class,
    AVG(se_count.side_effect_total) AS avg_side_effects
FROM TherapeuticClass tc
JOIN (
    SELECT 
        m.medicine_id,
        COUNT(mse.side_effect_id) AS side_effect_total
    FROM Medicine m
    LEFT JOIN Medicine_has_Side_Effect mse 
           ON m.medicine_id = mse.medicine_id
    GROUP BY m.medicine_id
) AS se_count 
ON se_count.medicine_id = se_count.medicine_id
GROUP BY tc.class_name;

-- Query2: Top medicines with the highest number of usages
SELECT 
    m.medicine_name,
    COUNT(mu.usage_id) AS usage_count
FROM Medicine m
LEFT JOIN Medicine_has_Usage mu
       ON m.medicine_id = mu.medicine_id
GROUP BY m.medicine_id
ORDER BY usage_count DESC
LIMIT 3;

    
-- Query3: Total number of substitutes per habit-forming category
SELECT 
    hf.habit_label AS habit_category,
    SUM(sub_counts.substitute_total) AS total_substitutes
FROM habit_forming hf
JOIN (
    SELECT 
        m.medicine_id,
        COUNT(ms.substitute_id) AS substitute_total
    FROM Medicine m
    LEFT JOIN Medicine_has_Substitutes ms 
           ON m.medicine_id = ms.medicine_id
    GROUP BY m.medicine_id
) AS sub_counts
ON sub_counts.medicine_id = sub_counts.medicine_id
GROUP BY hf.habit_label;

    
-- Query4: Medicines with the minimum number of side effects
WITH se_count AS (
    SELECT 
        m.medicine_id,
        m.medicine_name,
        COUNT(mse.side_effect_id) AS side_effect_total
    FROM Medicine m
    LEFT JOIN Medicine_has_Side_Effect mse 
           ON m.medicine_id = mse.medicine_id
    GROUP BY m.medicine_id
)
SELECT 
    medicine_name,
    side_effect_total
FROM se_count
WHERE side_effect_total = (SELECT MIN(side_effect_total) FROM se_count);


-- Query5: Maximum side effect count per chemical class
SELECT 
    cc.class_name AS chemical_class,
    MAX(se_count.side_effect_total) AS max_side_effects
FROM chemicalclasses cc
JOIN (
    SELECT 
        m.medicine_id,
        m.chemical_class_id,
        COUNT(mse.side_effect_id) AS side_effect_total
    FROM Medicine m
    LEFT JOIN Medicine_has_Side_Effect mse 
           ON m.medicine_id = mse.medicine_id
    GROUP BY m.medicine_id
) AS se_count
ON cc.chemical_class_id = se_count.chemical_class_id
GROUP BY cc.class_name;


