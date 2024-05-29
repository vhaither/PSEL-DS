SELECT
  AVG(tolls_amount) AS mediaPedagio
FROM
  `psel-interno.tlcYellowStrips.tabelaSemSchema`
WHERE
  tolls_amount > 0 and passenger_count <= 3