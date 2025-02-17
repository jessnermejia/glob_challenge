import io
import polars as pl
from dotenv import load_dotenv
from google.cloud import bigquery
from app.common.utils import get_credentials
from app.common.variables import PROJECT_ID


class BigqueryConn:

    def __init__(self):
        load_dotenv()
        self._creds = get_credentials()
        self.client = bigquery.Client(project=PROJECT_ID, credentials=self._creds)
    
    def load_df_to_table(self, df: pl.DataFrame, table: str, dataset:str = "glob_challenge"):
        # Write DataFrame to stream as parquet file; does not hit disk
        try:
            with io.BytesIO() as stream:
                
                df.write_parquet(stream)
                stream.seek(0)
                
                parquet_options = bigquery.ParquetOptions()
                parquet_options.enable_list_inference = True
                bq_config = bigquery.LoadJobConfig(parquet_options=parquet_options,
                                                   source_format=bigquery.SourceFormat.PARQUET,
                                                   write_disposition="WRITE_TRUNCATE")
                job = self.client.load_table_from_file(
                    stream,
                    destination=f"{dataset}.{table}",
                    project=PROJECT_ID,
                    job_config=bq_config,
                )
            job.result()  # Waits for the job to complete
            job_status = "SUCCESS"
        except Exception as e:
            print(e)
            job_status = "FAIL"
        
        return job_status
