from pathlib import Path

import numpy as np
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[1]
(PROJECT_ROOT / "data" / "clean").mkdir(parents=True, exist_ok=True)
(PROJECT_ROOT / "data" / "logs").mkdir(parents=True, exist_ok=True)

df = pd.read_csv(
    PROJECT_ROOT / "data" / "raw" / "raw.csv",
    low_memory=False,
)

# REMOVENDO COLUNAS E LINHAS VAZIAS
df = df.loc[:, ~df.columns.str.contains("^Unnamed")]
df = df[df["Tempo total"] != 0]

# CONVERSÃO DE DATATYPES
df["Ônibus 1"] = df["Ônibus 1"].astype(int).astype(str)

datetime_cols = ["Data"]
time_cols = ["Início", "Integração", "Fim"]
bool_cols = ["Sentada 1", "Sentada 2"]
category_cols = ["Lotação 1", "Lotação 2"]
text_cols = ["Partida", "Destino", "Dia da semana", "Rota"]


for col in datetime_cols:
    df[col] = pd.to_datetime(df[col], format="%d/%m/%Y", errors="coerce")

for col in time_cols:
    df[col] = pd.to_datetime(df[col], format="%H:%M:%S", errors="coerce").dt.time

bool_map = {"Sim": True, "Não": False}
for col in bool_cols:
    df[col] = df[col].map(bool_map).astype("boolean")

for col in category_cols:
    df[col] = df[col].astype("category")

for col in text_cols:
    df[col] = df[col].astype(str).str.strip()
    df[col] = df[col].replace("nan", np.nan)

# PADRONIZAÇÃO DE COLUNAS E CATALÓGO DE ENTRADAS INVÁLIDAS
# como os dados vem de um forms preenchido no momento de embarque,
# erros são esperados. há também um log pra catalogar exatamente qual foi o erro

log = []
numb_only = ["Ônibus 1", "Ônibus 2"]
letter_only = ["Partida", "Destino"]

for col in numb_only:
    log.append(df[df[col].str.contains("[^0-9+]", na=False)])
    df[col] = df[col].str.replace("[^0-9+]", "", regex=True)
    df[col] = df[col].replace("", np.nan)

valid_place_pattern = r"[^a-zA-ZáàãâéêíóôõúçÁÀÃÂÉÊÍÓÔÕÚÇ\s]"
for col in letter_only:
    log.append(df[df[col].str.contains(valid_place_pattern, na=False)])
    df[col] = df[col].str.replace(valid_place_pattern, "", regex=True)
    df[col] = df[col].replace("", np.nan)

# dessa forma, não vai haver log de dados inválidos sendo duplicados
# se uma linha tiver dados inválidos em mais de uma coluna
flag = pd.concat(log)
flag = flag[~flag.index.duplicated()]

# log de entradas inválidas
flag.to_csv(
    PROJECT_ROOT / "data" / "logs" / "flagged_rows.csv",
    header=False,
)

# exportando dados limpos
df.to_csv(
    PROJECT_ROOT / "data" / "clean" / "clean.csv",
)
