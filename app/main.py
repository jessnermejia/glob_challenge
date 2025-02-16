import os
from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
import polars as pl
from app.database.database import MySQLConn
from app.common.variables import ALLOWED_EXTENSIONS, DP_SCHEMA, JOBS_SCHEMA, HIRED_SCHEMA

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
def prediction():
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

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 8080)), debug=True)