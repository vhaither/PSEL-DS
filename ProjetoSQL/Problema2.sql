SELECT 
    passenger_count,
    COUNT(*) AS quantidadeCorridas,
    AVG(total_amount) AS receitaMediaCorrida,
    AVG(total_amount/passenger_count) AS receitaMediaPorPassageiro
FROM 
  `psel-interno.tlcYellowStrips.tabelaSemSchema`
WHERE 
    passenger_count BETWEEN 1 AND 5
GROUP BY 
    passenger_count
ORDER BY passenger_count asc
