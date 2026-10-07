import os
from pathlib import Path

import pandas as pd
import sqlalchemy as sa
from dotenv import load_dotenv

load_dotenv()

PROJECT_ROOT = Path(__file__).resolve().parents[1]

url_obj = sa.URL.create(
    drivername="mysql+mysqlconnector",
    host=os.getenv("DB_HOST"),
    username=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    database=os.getenv("DB_NAME"),
)

engine = sa.create_engine(url_obj)

df = pd.read_csv(PROJECT_ROOT / "data" / "clean" / "transformed.csv")

df.to_sql("staging_trips", engine, if_exists="replace", index=False)
