import logging
import sys

logging.basicConfig(stream=sys.stdout, level=logging.INFO)
logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout))

from llama_index.indices.struct_store import (
    NLSQLTableQueryEngine
)

from sqlalchemy import (
    create_engine,
    MetaData,
    Table,
    Column,
    String,
    Integer,
    select,
    column,
)

engine = create_engine("duckdb:///data/duckdb/contracts.db")
metadata_obj = MetaData()
table_name = "contract_stats"

metadata_obj.create_all(engine)

# print tables
metadata_obj.tables.keys()

with engine.connect() as connection:
    cursor = connection.exec_driver_sql("SELECT * FROM contract_stats")
    print(cursor.fetchall())

from llama_index import SQLDatabase

sql_database = SQLDatabase(engine, include_tables=["contract_stats"])

query_engine = NLSQLTableQueryEngine(sql_database)


def get_answer(query):
    return query_engine.query(query)


result = get_answer("What is total contract value in year 2024?")

print(result)
