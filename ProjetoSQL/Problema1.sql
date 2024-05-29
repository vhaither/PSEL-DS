SELECT
  CASE
    WHEN payment_type = 1 THEN 'Credit card'
    WHEN payment_type = 2 THEN 'Cash'
    WHEN payment_type = 3 THEN 'No charge'
    WHEN payment_type = 4 THEN 'Dispute'
    WHEN payment_type = 5 THEN 'Unknown'
    WHEN payment_type = 6 THEN 'Voided trip'
  END AS tipoDePagamentoMapeado,
  COUNT(*) AS quantidadeCorridas,
  SUM(total_amount) AS receitaTotal,
  AVG(total_amount) AS receitaMedia
FROM
  `psel-interno.tlcYellowStrips.tabelaSemSchema`
WHERE
  DATE(pickup_datetime) = '2018-03-15'
GROUP BY
  tipoDePagamentoMapeado