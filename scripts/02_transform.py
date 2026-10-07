from pathlib import Path

import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[1]
(PROJECT_ROOT / "data" / "clean").mkdir(parents=True, exist_ok=True)

# index vira coluna trip_id que indentifica duas etapas de uma viagem
df = pd.read_csv(PROJECT_ROOT / "data" / "clean" / "clean.csv")
df = df.rename(columns={"Unnamed: 0": "trip_id"})

# tabela 1 linha por viagem -> tabela 1 linha por etapa de viagem
long_df = pd.wide_to_long(
    df, stubnames=["Ônibus", "Sentada", "Lotação"], i="trip_id", j="leg", sep=" "
)

# passo anterior gera linhas com segunda etapa vazia mesmo para viagens de apenas
# 1 ônibus, corrigido limpando coluna com valores vazios na coluna ônibus
long_df.dropna(subset=["Ônibus"], inplace=True)

# transforma o index múltiplo trip_id e leg em colunas da tabela,
# coluna 'rota' é removida devido redundância
long_df = long_df.reset_index()

long_df = long_df.drop(labels="Rota", axis=1)

long_df.to_csv(PROJECT_ROOT / "data" / "clean" / "transformed.csv")
