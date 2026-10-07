CREATE DATABASE bus_commute;
USE bus_commute;

CREATE TABLE locais (
	local_id int UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
    nome varchar(255) UNIQUE
);

CREATE TABLE onibus (
	bus_id int UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
    linha int NOT NULL UNIQUE,
    bus_tipo varchar(255)
);

CREATE TABLE commute_legs (
	c_legs_id int UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
    dia date,
    trip_id int UNSIGNED NOT NULL,
    bus_id int UNSIGNED NOT NULL,
    CONSTRAINT fk_commute_legs_bus_id
    FOREIGN KEY (bus_id)
    REFERENCES onibus(bus_id),
    leg_order int,
    partida int UNSIGNED NOT NULL,
    CONSTRAINT fk_commute_legs_partida
    FOREIGN KEY (partida)
    REFERENCES locais(local_id),
    destino int UNSIGNED NOT NULL,
    CONSTRAINT fk_commute_legs_destino
    FOREIGN KEY (destino)
    REFERENCES locais(local_id),
	inicio time,
    fim time,
    sentada bool,
    lotacao enum('Alta', 'Média', 'Baixa')
);

-- atualização para prevenir duplicidade de linhas na tabela
-- após reprocessamento de dados
ALTER TABLE commute_legs
ADD CONSTRAINT uq_dia_inicio  UNIQUE (dia, inicio);