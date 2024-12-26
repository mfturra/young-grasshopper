import os
import uuid
import config
import psycopg2
from dotenv import load_dotenv
from prelim_db import institutions, curriculums, students
from configparser import ConfigParser
from flask import Flask, render_template, request
from flask_smorest import abort

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

# initialize app
app = Flask(__name__)

# route to main page
@app.get('/')
def home():
    return render_template('islandIndex.html')

# get info on all institutions
# future iteration: change route to '/'
@app.get('/home')
def get_all_institutions():
    # future iteration: route user to islandIndex.html
    return { "institutions": list(institutions.values()) }

# get info on institution
# future iteration: change route to '/'
@app.get('/home/<string:institution_id>')
def get_institution(institution_id):
    try:
        # future iteration: route user to webpage of welcome banner of institution
        return institutions[institution_id]
    except KeyError:
        abort(404, message="Institution not found")

## setup institution
@app.post('/home')
def create_institution():
    inst_data = request.get_json()

    # check if payload includes an institution_name
    if "inst_name" not in inst_data:
        abort(404, message="Ensure that 'instutition_name' is included in payload")
    
    # check if institution exists
    for institution in institutions.values():
        if inst_data["inst_name"] == institution["inst_name"]:
            abort(400, message="Bad request. The institution that you requested already exists")
        else:
            # create institution
            inst_id = uuid.uuid4().hex

            new_inst = {**inst_data, "id": inst_id, "name": "inst_name"}
            institutions[inst_id] = new_inst

            # future iteration: route admin to webpage of new institution created
            return new_inst, 201

# create new curriculum at institution
@app.post('/curriculum')
def create_curriculum():
    curriculum_data = request.get_json()
    # check if all elements exist in JSON payload
    if (
        "curriculum_id" not in curriculum_data
        or "curriculum_name" not in curriculum_data
        or "semester_cost" not in curriculum_data
        or "inst_id" not in curriculum_data
    ):
        abort(
            400,
            message = "Bad request. Ensure that the 'curriculum_id', 'inst_id', 'curriculum_name', 'semester_cost' is included in the JSON payload."
        )
    # iterature through curriculums and check for similar curriculum
    for curriculum in curriculum.values():
        if(
            curriculum_data["curriculum_name"] == curriculum["curriculum_name"]
            and curriculum_data["inst_id"] == curriculum["inst_id"]
        ):
            abort(404, message="Curriculum already exists")

    else:
        curriculum_id = uuid.uuid4().hex
        curriculum = { **curriculum_data, "id": curriculum_id}
        curriculums[curriculum_id] = curriculum

        # future iteration: route admin to webpage of new curriculum added
        return curriculum, 201
    
# get list of all curriculums to prospective students
@app.get('/curriculum')
def get_all_curriculums():

    # future iteration: route user to webpage of all curriculums
    return {curriculums: list(curriculums.items())}

@app.get('/curriculum/<string:curriculum_id>')
def get_curriculum_info(curriculum_id):
    try:
        return curriculums[curriculum_id]
    except KeyError: 
        abort(404, message="Curriculum not found")

# route to user to public university main page
@app.get('/public-university')
def public_university():
    return render_template('universityMain/publicUniversity.html')

# route user to private university main page
@app.get('/private-university')
def private_university():
    return render_template('universityMain/privateUniversity.html')


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