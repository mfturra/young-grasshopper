import os
import uuid
import config
import psycopg2
from dotenv import load_dotenv
from prelim_db import institutions, curriculums, students
from configparser import ConfigParser
from flask import Flask, render_template, request, redirect, url_for
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

@app.get('/index')
def user_main():
    return render_template('user_login.html')

@app.post('/login')
def user_login():
    user_data = request.form.to_dict()

    if user_data['email'] == user_db['email']:
        return 403, {'message': 'This email pertains to another user. Please create your account with another email.'}

    user_data = {
        'first_name': user_data['first_name'],
        'last_name': user_data['last_name'],
        'email': user_data['email'],
        'user_id': uuid.uuid4().hex
    }

    return redirect(url_for('home'))
    # return 

# route to main page
@app.get('/home')
def home():
    return render_template('islandIndex.html')

# get info on all institutions
# future iteration: change route to '/'
@app.get('/')
def get_all_institutions():
    # future iteration: route user to islandIndex.html
    return {"institutions": list(institutions.values())}

# get info on institution
@app.get('/<string:inst_id>')
def get_institution(inst_id):
    try:
        # future iteration: route user to webpage of welcome banner of institution
        return institutions[inst_id]
    except KeyError:
        return { "message":"Institution not found."}, 404

## setup institution
@app.post('/')
def create_institution():
    inst_data = request.get_json()

    # check if payload includes an inst_name
    if "inst_name" not in inst_data:
        abort(404, message="Ensure that 'inst_name' is included in JSON payload.")
    
    # check if institution already exists
    for institution in institutions.values():
        if inst_data["inst_name"] == institution["inst_name"]:
            return { "message":"Institution already exists."}, 403 #abort(400, message="Bad request. The institution that you requested already exists.")

    # create institution
    inst_id = uuid.uuid4().hex

    new_inst = {**inst_data, "inst_id": inst_id, "name": "inst_name"}
    institutions[inst_id] = new_inst

    # future iteration: route admin to webpage of new institution created
    return new_inst, 201

# delete specific institution
@app.delete('/<string:inst_id>')
def delete_institution(inst_id):
    try:
        del institutions[inst_id]
        return {"message": "Institution successfully deleted."}
    except KeyError:
        return {"message": "Institution not found."}

# get list of all curriculums to prospective students
@app.get('/curriculum')
def get_all_curriculums():

    # future iteration: route user to webpage of all curriculums
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


# route to user to public university main page
@app.get('/public-university')
def public_university():
    return render_template('universityMain/publicUniversity.html')

# route user to private university main page
@app.get('/private-university')
def private_university():
    return render_template('universityMain/privateUniversity.html')


