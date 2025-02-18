import os
from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
import tempfile
from app.database.database import MySQLConn
from app.filesystem.gcs_glob import GCSConnection
from app.database.bigquery_glob import BigqueryConn
from app.common.variables import (ALLOWED_EXTENSIONS, DP_SCHEMA, FILE_PATH, 
                                  JOBS_SCHEMA, HIRED_SCHEMA, 
                                  DP_COLUMNS, DP_VALUES, JOB_COLUMNS,
                                  JOB_VALUES, HIRED_COLUMNS, HIRED_VALUES)

app = Flask(__name__) 

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def get_file_name(filename:str) -> str:
    return filename.rsplit('.', 1)[0].lower()

@app.route('/', methods=['GET'])
def root():
    return jsonify({"status":"app ok"})

@app.route('/upload', methods=['POST'])
def upload():
    if request.method == 'POST':
        if request.files:
            departments = request.files.get('departments', None)
            jobs = request.files.get('jobs', None)
            hired = request.files.get('hired', None)

            if departments and allowed_file(departments.filename):
                filename = secure_filename(departments.filename)
                final_name = get_file_name(filename)
                sql_object = MySQLConn()
                sql_object.upload_file_table(file=departments,
                                            schema_df=DP_SCHEMA,
                                            table="tbl_department")
                
                return jsonify({'status': 'SUCCESS', 'description': f'{final_name} was uploaded'})
        
            elif jobs and allowed_file(jobs.filename):
                jobs_file = secure_filename(jobs.filename)
                final_name = get_file_name(jobs_file)
                sql_object = MySQLConn()
                sql_object.upload_file_table(file=jobs,
                                            schema_df=JOBS_SCHEMA,
                                            table="tbl_job")
                return jsonify({'status': 'SUCCESS', 'description': f'{final_name} was uploaded'})

            elif hired and allowed_file(hired.filename):
                hired_file = secure_filename(hired.filename)
                final_name = get_file_name(hired_file)
                sql_object = MySQLConn()
                sql_object.upload_file_table(file=hired,
                                            schema_df=HIRED_SCHEMA,
                                            table="tbl_hired_employee")
                return jsonify({'status': 'SUCCESS', 'description': f'{final_name} was uploaded'})
        
            else:
                return jsonify({'status': 'FAIL', 'description': 'No selected file'})

@app.route('/bulk', methods=['POST'])
def bulk_data():
    if request.method == "POST":
        data = request.get_json()
        data_pushed = data.get('data')
        
        if len(data_pushed) <= 1000:
            sql_object = MySQLConn()
            table_name=data.get('table')

            if table_name == "tbl_department" :
                table_columns = DP_COLUMNS
                table_values = DP_VALUES
            elif table_name == "tbl_job":
                table_columns = JOB_COLUMNS
                table_values = JOB_VALUES
            elif table_name == "tbl_hired_employee":
                table_columns = HIRED_COLUMNS
                table_values = HIRED_VALUES
            else:
                raise("Need a valid table name")
            
            rows_inserted = sql_object.insert_rows(table=table_name,
                                    columns=table_columns,
                                    values=table_values,
                                    rows=data_pushed,
                                    template_name="insert_table.sql")
            
            return jsonify({'status': 'SUCCESS', 'description': f'{rows_inserted} rows was inserted'})
        else:
            return jsonify({'status': 'FAIL', 'description': 'Up to 1000 rows can be inserted'})

@app.route('/backup', methods=['POST'])
def backup_data():
    if request.method == "POST":
        data = request.get_json()
        obj_gcs = GCSConnection()
        table_name = data.get("table")
        params = {
            "db_name": "glob_challenge",
            "table_name": table_name
        }
        sql_object = MySQLConn()
        response_df = sql_object.query_to_df(query_name="select_all.sql", params_query=params)

        with tempfile.NamedTemporaryFile(prefix=table_name, dir=FILE_PATH) as file:
            response_df.write_avro(file.name)
            response = obj_gcs.upload_file(source_file=file.name, destination=f"backup/{table_name}.avro")
            if response:
                status = "SUCCESS"
            else:
                status = "FAIL"
            file.close()
        return jsonify({"status":status, "details":"tabla backed"})

@app.route('/restore', methods=['POST'])
def restore_table():
    if request.method == "POST":
        data_request = request.get_json()
        table_name = data_request.get("table")
        gcs_object = GCSConnection()
        sql_object = MySQLConn()
        with tempfile.NamedTemporaryFile(prefix=table_name, dir=FILE_PATH) as lc_file:
            gcs_object.download_file(source_file=f"backup/{table_name}.avro",
                                     destination_path=lc_file.name)
            status = sql_object.upload_backed_file(file=lc_file.name, table=table_name)
            lc_file.close()
        return jsonify({"status":status, "details":f"{table_name} backed up"})

@app.route('/hires_q', methods=['GET'])
def get_hires_by_q():
    if request.method == "GET":
        data_request = request.get_json()
        year = data_request.get("year")
        sql_object = MySQLConn()
        bq_object = BigqueryConn()
        try:
            data = sql_object.query_to_df(query_name="hires_by_q.sql", params_query={"year": year})
            pivoted_df = data.pivot("q", index=["department","job"], values="employee", aggregate_function="len")
            print(pivoted_df)
            status = bq_object.load_df_to_table(df=pivoted_df, table="hires_by_q")
        except Exception as e:
            print(e)
            status = "FAIL"
        return jsonify({"status": status, "details": "table hires_by_q was updated"})

@app.route('/hires_depa', methods=['GET'])
def get_hires_by_department():
    if request.method == "GET":
        data_request = request.get_json()
        year = data_request.get("year")
        sql_object = MySQLConn()
        bq_object = BigqueryConn()
        try:
            data = sql_object.query_to_df(query_name="hires_by_dpt.sql", params_query={"year": year})
            print(data)
            status = bq_object.load_df_to_table(df=data, table="hires_by_dpt")
        except Exception as e:
            print(e)
            status = "FAIL"
        return jsonify({"status": status, "details": "table hires_by_dpt was updated"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 8080)), debug=True)