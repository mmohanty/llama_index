import logging
import sys
import os
import openai

#openai.api_key = os.environ["OPENAI_API_KEY"]

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

#llm = OpenAI(temperature=0.5, model="gpt-3.5-turbo-16k")
#service_context = ServiceContext.from_defaults(llm=llm)

# query_engine = NLSQLTableQueryEngine(sql_database, service_context=service_context) with OpenAI llm

query_engine = NLSQLTableQueryEngine(sql_database) # default llm

format_hint: str = "Please answer with a short summary. Dont explain the query and make it compatible with DuckDB"

def get_answer(query):
    final_query = query + "\n" + format_hint
    return query_engine.query(final_query)


result = get_answer("What is total contract value in year 2024?")

print(result)

print(result.metadata)
