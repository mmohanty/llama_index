import logging
import sys

logging.basicConfig(stream=sys.stdout, level=logging.INFO)
logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout))


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

#engine = create_engine("duckdb:///:memory:")
engine = create_engine("duckdb:///data/duckdb/contracts.db")
# uncomment to make this work with MotherDuck
# engine = create_engine("duckdb:///md:llama-index")
metadata_obj = MetaData()
# create city SQL table
table_name = "contract_stats"

contract_stats_table = Table(
    table_name,
    metadata_obj,
    Column("contract_name", String(16), primary_key=True),
    Column("cost", Integer),
    Column("start_date", String(10), nullable=False),
    Column("end_date", String(10), nullable=False),
    Column("renewal_date", String(10), nullable=False),
)

metadata_obj.create_all(engine)


# print tables
metadata_obj.tables.keys()

from sqlalchemy import insert

rows = [
    {"contract_name": "Infosys", "cost": 1000, "start_date": "2022-10-10", "end_date": "2023-10-10", "renewal_date": "2023-10-11"},
    {"contract_name": "Wipro", "cost": 2000, "start_date": "2022-08-10", "end_date": "2023-08-10", "renewal_date": "2023-08-11"},
    {"contract_name": "TCS", "cost": 500, "start_date": "2022-11-10", "end_date": "2023-11-10", "renewal_date": "2023-11-11"},
    {"contract_name": "HCL", "cost": 1500, "start_date": "2023-08-10", "end_date": "2024-08-10", "renewal_date": "2024-08-11"},
]
for row in rows:
    stmt = insert(contract_stats_table).values(**row)
    with engine.connect() as connection:
        cursor = connection.execute(stmt)
        connection.commit()


with engine.connect() as connection:
    cursor = connection.exec_driver_sql("SELECT * FROM contract_stats")
    print(cursor.fetchall())


