USE bus_commute;

SELECT
	destino, locais.nome
FROM commute_legs
JOIN locais
	ON commute_legs.destino = locais.local_id
GROUP BY destino;


-- menor tempo por par origem/destino
WITH trip_time AS (
	SELECT MIN(inicio) AS start_time,
    MAX(fim) AS end_time,
    MIN(partida) AS start_dest,
	MAX(destino) AS final_dest,
--     bus_id
    trip_id
	FROM commute_legs
	GROUP BY trip_id
)
SELECT MIN(TIMEDIFF(end_time, start_time)) AS duration,
l2.nome AS origem,
l1.nome AS destino
-- o1.linha AS first_bus
FROM trip_time
JOIN locais AS l1
ON trip_time.final_dest = l1.local_id
JOIN locais AS l2
ON trip_time.start_dest = l2.local_id
-- JOIN onibus AS o1
-- ON trip_time.bus_id = o1.bus_id
GROUP BY start_dest, final_dest 