import logging
import sys

logging.basicConfig(stream=sys.stdout, level=logging.INFO)
logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout))

from llama_index.indices.struct_store import (
    NLSQLTableQueryEngine,
    SQLContextContainerBuilder,
    SQLTableRetrieverQueryEngine,

)
from IPython.display import Markdown, display

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

connection_uri = r"sqlite:///data/sqlite/contracts.db"

engine = create_engine(connection_uri)
# uncomment to make this work with MotherDuck
# engine = create_engine("duckdb:///md:llama-index")
metadata_obj = MetaData()
table_name = "contract"

# contract_stats_table = Table(
#     table_name,
#     metadata_obj,
#     Column("contract_id", String, primary_key=True),
#     Column("vendor_name", String),
#     Column("contract_value", Integer),
#     Column("start_date", String, nullable=False),
#     Column("end_date", String, nullable=False),
#     Column("renewal_date", String, nullable=False),
# )

metadata_obj.create_all(engine)


# print tables
metadata_obj.tables.keys()



with engine.connect() as connection:
    cursor = connection.exec_driver_sql("SELECT * FROM contract")
    print(cursor.fetchall())


from llama_index import SQLDatabase, GPTSQLStructStoreIndex

sql_database = SQLDatabase(engine, include_tables=["contract"])


query_engine = NLSQLTableQueryEngine(sql_database)

#response = query_engine.query("What is total contract value of Wipro?")
#response = query_engine.query("How many contracts are going to be renewed next month?")
#response = query_engine.query("Which contracts are going to be renewed next month?")
response = query_engine.query("What is total contract value in year 2023?")

print(response)


#print(response.metadata)


