import polars as pl

PROJECT_ID = "interno-lumen-analitica"
SECRET_ID = "glob_challenge_secret"
PATH_CRED = "/Users/jessner/Profesional/Desarrollos/glob_challenge/.creds/glob_challenge.txt"
ALLOWED_EXTENSIONS = {'csv'}
FILE_PATH = '/Users/jessner/Profesional/Desarrollos/glob_challenge/files'
DP_SCHEMA = pl.Schema({"idtbl_department": pl.Int16() ,"department": pl.String()})
JOBS_SCHEMA = pl.Schema({"idtbl_job": pl.Int16(), "name_job":pl.String()})
HIRED_SCHEMA = pl.Schema({"idtbl_hired_employee": pl.Int16,
                          "name": pl.String(),
                          "hire_datetime": pl.Datetime(),
                          "tbl_department_idtbl_department": pl.Int16,
                          "tbl_job_idtbl_job":pl.Int16})