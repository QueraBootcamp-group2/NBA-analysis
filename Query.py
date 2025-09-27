from sqlalchemy import create_engine
import pandas as pd
import pymysql

username = "admin"
password = "Admin@2025"
host = "127.0.0.1"   
port = 3306             
database = "NBA"

engine = create_engine(f"mysql+pymysql://{username}:{password}@{host}:{port}/{database}", connect_args={"connect_timeout": 60})

with engine.connect() as conn:
    result = conn.execute("SELECT VERSION();")
    print(result.fetchone())

df1_1 = pd.read_sql("SELECT player_name, height From mvp", engine)
df1_1.to_csv("test.csv", index=False)

print(" Query results saved to complex_query_results.csv")