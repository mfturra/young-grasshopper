import os
import uuid
import config
import secrets
import psycopg2
from dotenv import load_dotenv
from prelim_db import institutions, degrees, curriculums
from configparser import ConfigParser
from flask import Flask, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from flask_smorest import abort

# initialize app
app = Flask(__name__)

# Load database.ini config
config = ConfigParser()
config.read('database.ini')

app.secret_key = config['flask']['secret_key']

# get info on all institutions
@app.get('/institutions')
def inst_home():
    return { "institutions": list(institutions.values())}

## setup institution
@app.post('/institutions')
def create_institution():
    inst_data = request.get_json()

    # check if all elements are included in json payload
    if (
        "inst_type" not in inst_data
        or "inst_name" not in inst_data
        or "inst_cost" not in inst_data
        or "welcome_text" not in inst_data
    ):
        abort(
            400,
            message="Bad request. Ensure that 'inst_type', 'inst_name', 'inst_cost', and 'welcome_text' are included in the payload."
        )
    for inst in institutions.values():
        if (
            inst_data["inst_type"] == inst["inst_type"]
            and inst_data["inst_name"] == inst["inst_name"]
            and inst_data["inst_cost"] == inst["inst_cost"]
        ):
            abort(
                404,
                message="Institution already exists.")

    inst_id = uuid.uuid4().hex
    inst = {**inst_data, "id": inst_id}
    institutions[inst_id] = inst
    return inst, 201

# delete specific institution
@app.delete('/institutions/<string:inst_id>')
def delete_institution(inst_id):
    try:
        del institutions[inst_id]
        return {"message": "Institution successfully deleted."}
    except KeyError:
        abort(404, message="Institution was not found.")

@app.put('/institutions')
def update_inst():
    try:
        pass
    except KeyError:
        abort(404, message="Institution was not found.")

# get info on single institution
@app.get('/institutions/<string:inst_id>')
def get_institution(inst_id):
    try:
        return institutions[inst_id]
    except KeyError:
        abort(404, message="Institution was not found.")

@app.get('/degrees')
def get_all_degrees():
    return { "degrees": list(degrees.items())}

@app.post('/degrees')
def create_degree():
    degree_data = request.get_json()

    # check payload for all required items
    if (
        "degree_track" not in degree_data
        or "degree_name" not in degree_data
        or "degree_description" not in degree_data
        or "inst_id" not in degree_data
        or "inst_cost" not in degree_data
    ):
        abort(
            400,
            message="Ensure that 'degree_track', 'degree_name', 'degree_description', 'inst_id', and 'inst_cost' is in your JSON payload."
        )
    
    # check for duplicate degree entries
    for degree in degrees.values():
        if (
            degree_data["degree_name"] == degree["degree_name"]
            and degree_data["degree_track"] == degree["degree_track"]
            and degree_data["inst_id"] == degree["inst_id"]
        ):
            abort(
                404,
                message="Degree has already been created."
                )
            
    degree_id = uuid.uuid4().hex
    degree = {**degree_data, "id": degree_id}
    degrees[degree_id] = degree
    return degree, 201

@app.delete('/degrees/<string:degree_id>')
def delete_degree(degree_id):
    try:
        del degrees[degree_id]
        return {"message": "Degree was successfully deleted."}
    except KeyError:
        abort(404, message='Degree was not found')
        
@app.get('/degrees/<string:degree_id>')
def get_one_degree(degree_id):
    try:
        return degrees[degree_id]
    except KeyError:
        abort(404, "Degree was not found")


# get list of all curriculums to prospective students
@app.get('/curriculum')
def get_all_curriculums():
    return {"curriculums": list(curriculums.items())}

# get list of only one curriculum
@app.get('/curriculum/<string:curriculum_id>')
def get_curriculum_info(curriculum_id):
    try:
        return curriculums[curriculum_id]
    except KeyError: 
        abort(404, message="Curriculum not found.")

# create new curriculum at institution
@app.post('/curriculum')
def create_curriculum():
    curriculum_data = request.get_json()
    
    # check if all elements exist in JSON payload
    if (
        "curriculum_name" not in curriculum_data
        or "semester_cost" not in curriculum_data
        or "inst_id" not in curriculum_data
    ):
        abort(
            400,
            message = "Bad request. Ensure that the 'curriculum_id', 'inst_id', 'curriculum_name', 'semester_cost' is included in the JSON payload."
        )

    if curriculum_data["inst_id"] not in institutions:
        abort(404, "Institution not found.")

    # iterature through curriculums and check for similar curriculum
    for curriculum in curriculums.values():
        if(
            curriculum_data["curriculum_name"] == curriculum["curriculum_name"]
            and curriculum_data["inst_id"] == curriculum["inst_id"]
        ):
            abort(404, message="Curriculum already exists.")

    curriculum_id = uuid.uuid4().hex
    curriculum = {**curriculum_data, "curriculum_id": curriculum_id}
    curriculums[curriculum_id] = curriculum

    # future iteration: route admin to webpage of new curriculum added
    return curriculum, 201

# delete curriculum
@app.delete('/curriculum/<string:curriculum_id>')
def delete_curriculum(curriculum_id):
    try:
        del curriculums[curriculum_id]
        return {"message": "Curriculum was deleted."}
    except KeyError:
        abort(404, message="Curriculum not found.")

@app.put('/curriculum/<string:curriculum_id>')
def update_curriculum(curriculum_id):
    curriculum_data = request.get_json()

    # check to see if "curriculum_name" and "semester_cost" was included in JSON payload
    if "curriculum_name" not in curriculum_data and "semester_cost" not in curriculum_data:
        return {"message": "Curriculum not included in data set."}
    try:
        curriculum = curriculums[curriculum_id]
        curriculum |= curriculum_data

        return curriculum
    except KeyError:
        return {"message":"Curriculum was not found."}

# enroll new student at the respective institution
@app.post('/<string:institution_id>/new-enrollment')
def new_enrollment(institution_id):
    for institution in institutions:
        # check if university exists
        if institution[institution_id] != institution_id: 
            abort(404, message="Institution not found")
        else:
            student_data = request.get_json()
            student_id = uuid.uuid4().hex
            new_student = { "id": student_id, "name": student_data["name"], "email": student_data["email"], "curriculum": student_data["curriculum"]}
            
            # store new student in the respective university
            students[student_id] = new_student

            return new_student, 201
    abort(404, message="Institution not found")

# identify all students that are enrolled at the respective university
@app.get('/<string:institution_id>/enrolled')
def get_all_students(institution_id):
    for institution in institutions:
        if institution['institution_id'] == institution_id:
            return { "local": institution["institution_id"], "students": institution["students"]}, 200 #, "students": students["pedro"]}
    abort(404, message="Institution not found")

@app.route('/logout')
def logout():
    session.clear()
    # flash('You have been logged out.')
    return redirect(url_for('home'))
    
# def config(filename='database.ini', section='postgresql'):
#     # create file parser
#     parser = ConfigParser()

#     # read config file
#     parser.read(filename)

#     # get section, default to postgresql
#     db_params = {}
#     if parser.has_section(section):
#         params = parser.items(section)
#         for param in params:
#             db_params[param[0]] = param[1]
#     else:
#         raise Exception('Section {0} not found in {1} file'.format(section, filename))
    
#     return db_params

# read config params
# db_params = config()

# # Use conn_string to connect to SQL DB
# conn_string = f"postgresql+psycopg2://{db_params['user']}:{db_params['password']}@{db_params['host']}:{db_params['port']}/{db_params['database']}"
# db_connection = psycopg2.connect(conn_string)