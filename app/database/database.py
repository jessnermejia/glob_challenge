"""
TODO 
Database module to manage connection and methods for read and write
"""
import os
from dotenv import load_dotenv
import pymysql
import sqlalchemy
from google.cloud.sql.connector import Connector, IPTypes
from app.common.utils import get_credentials, read_sql_file, clean_data
from app.common.variables import TEMPLATES_SQL_PATH
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
        df_cleaned, df_nulls = clean_data(df_data)
        print(f"inserting data in {table}")
        try:
            db_pool = self.connect_database()
            df_cleaned.write_database(table_name=table,
                                connection=db_pool,
                                if_table_exists= "append",
                                engine="sqlalchemy")
        except Exception as e:
            print(e)
        finally:
            print(f"Data with nulls was excluded, more details here: {df_nulls}")
            self.close_conn()
    
    def insert_rows(self, table, columns, values, rows, template_name):
        path_insert = os.path.join(TEMPLATES_SQL_PATH, template_name)
        total_rows = 0
        try:
            db_engine = self.connect_database()
            db_conn = db_engine.connect()

            for row in rows:
                params_query = {
                    "db_name": "glob_challenge",
                    "table_name": table,
                    "columns_names": columns,
                    "columns_values": values
                }
                query_insert = sqlalchemy.text(read_sql_file(path=path_insert, params = params_query))
                try:
                    db_conn.execute(query_insert, parameters=row)
                    db_conn.commit()
                except Exception as e:
                    print(e)
                    db_conn.rollback()
                total_rows += 1
        except Exception as e: 
            print(e)       
        finally:
            db_conn.close()
        
        return total_rows     
