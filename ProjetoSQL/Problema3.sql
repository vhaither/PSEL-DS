SELECT 
    EXTRACT(HOUR FROM pickup_datetime) AS hora,
    COUNT(*) AS quantidadeCorridas
FROM 
  `psel-interno.tlcYellowStrips.tabelaSemSchema`
GROUP BY 
    hora
ORDER BY 
    quantidadeCorridas DESC