"""
TODO 
Database module to manage connection and methods for read and write
"""
import os
from dotenv import load_dotenv
import pymysql
import sqlalchemy
from google.cloud.sql.connector import Connector, IPTypes
from app.common.utils import get_credentials
import polars as pl

class MySQLConn:

    def __init__(self):
        load_dotenv()
        self.instance_connection_name = os.getenv("INSTANCE_CONNECTION_NAME")
        self.db_user = os.getenv("DB_USER")
        self.db_pass = os.getenv("DB_PASS")
        self.db_name = os.getenv("DB_NAME")
        self.connector = Connector(refresh_strategy="LAZY", credentials=get_credentials())

    def getconn(self,) -> pymysql.connections.Connection:
        conn: pymysql.connections.Connection = self.connector.connect(
            self.instance_connection_name,
            "pymysql",
            user=self.db_user,
            password=self.db_pass,
            db=self.db_name,
        )
        return conn
    
    def close_conn(self,):
        return self.connector.close()

    def connect_database(self,) -> sqlalchemy.engine.base.Engine:
        pool = sqlalchemy.create_engine(
            "mysql+pymysql://",
            creator=self.getconn
        )
        return pool

    def upload_file_table(self, file, schema_df, table: str):
        df_data = pl.read_csv(file, has_header=False, schema=schema_df)
        print(f"inserting data in {table}")
        try:
            db_pool = self.connect_database()
            df_data.write_database(table_name=table,
                                connection=db_pool,
                                if_table_exists= "append",
                                engine="sqlalchemy")
        except Exception as e:
            print(e)
        finally:
            self.close_conn()
