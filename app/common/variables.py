import os
import pathlib
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
TEMPLATES_SQL_PATH = os.path.join(pathlib.Path(__file__).parent.parent, "database/query")
DP_COLUMNS = "idtbl_department, department"
DP_VALUES = ":idtbl_department, :department"
JOB_COLUMNS = "idtbl_job, name_job"
JOB_VALUES = ":idtbl_job, :idtbl_job"
HIRED_COLUMNS = "idtbl_hired_employee, name, hire_datetime, tbl_department_idtbl_department, tbl_job_idtbl_job"
HIRED_VALUES = ":idtbl_hired_employee, :name, :hire_datetime, :tbl_department_idtbl_department, :tbl_job_idtbl_job"