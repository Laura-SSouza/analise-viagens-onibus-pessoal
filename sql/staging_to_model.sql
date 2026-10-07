USE bus_commute;

INSERT IGNORE INTO locais (nome)
SELECT partida FROM staging_trips
UNION
SELECT destino FROM staging_trips;

INSERT IGNORE INTO onibus (linha)
	SELECT SUBSTRING_INDEX(`Ônibus`,"+",1) FROM staging_trips
		WHERE `Ônibus` IS NOT NULL
	UNION 
	SELECT SUBSTRING_INDEX(`Ônibus`,"+",-1) FROM staging_trips
		WHERE `Ônibus` IS NOT NULL;

UPDATE onibus
SET bus_tipo = 
	CASE
		WHEN LEFT(linha, 1) = 7 AND LENGTH(linha) = 3
		THEN 'Topic'
		ELSE 'Onibus'
	END
WHERE bus_id > 0;

INSERT IGNORE INTO commute_legs (
			dia,
            trip_id,
            bus_id,
            leg_order,
            partida,
            destino,
            inicio,
            fim,
            sentada,
            lotacao
)
WITH staging_trips_count AS (
	SELECT trip_id, leg, `Data`, Sentada, `Lotação`, `Ônibus`, Partida, Destino, CASE
		WHEN leg = 1
			THEN `Início`
		WHEN leg = 2
			THEN `Integração`
	END AS inicio,
	CASE
 		WHEN COUNT(*) OVER (PARTITION BY trip_id) = 1
 			THEN `Fim`
        WHEN leg = 1
			THEN `Integração`
		WHEN leg = 2
			THEN `Fim`
	END AS fim
FROM staging_trips)
SELECT `Data`,
		trip_id,
        onibus.bus_id,
        leg,
        partida.local_id,
        destino.local_id,
        inicio,
        fim,
        Sentada,
        `Lotação`
FROM staging_trips_count
JOIN onibus
	ON staging_trips_count.`Ônibus` = onibus.linha
JOIN locais AS partida
	ON staging_trips_count.Partida = partida.nome
JOIN locais AS destino
	ON staging_trips_count.Destino = destino.nome;