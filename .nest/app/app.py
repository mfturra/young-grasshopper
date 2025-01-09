import os
import uuid
import config
import secrets
import psycopg2
from dotenv import load_dotenv
from prelim_db import institutions, curriculums, students
from configparser import ConfigParser
from flask import Flask, render_template, request, redirect, url_for, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_smorest import abort

# initialize app
app = Flask(__name__)

# Load database.ini config
config = ConfigParser()
config.read('database.ini')

app.secret_key = config['flask']['secret_key']

# create students database
students_db = []

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        command = request.form.get('command').strip().lower()
        if command == 'create':
            return redirect(url_for('create_account'))
        elif command == 'login':
            return redirect(url_for('student_login'))
        else:
            flash('Invalid command. Please type "create" or "login" to proceed.')

    return render_template('home.html')


@app.route('/create', methods=['GET', 'POST'])
def create_account():
    # check new account inputs
    if request.method == 'POST':
        first_name =    request.form.get('first_name')
        last_name =     request.form.get('last_name')
        email =         request.form.get('email')
        password =      request.form.get('password')
        
        # password validation
        if len(password) < 7:
            flash('Password must be at least 7 characters long.')
            return redirect(url_for('create_account'))
        
        # check for duplicate email in db
        for student in students_db:
            if student['email'] == email:
                flash('An account with this email already exists.')
                return redirect(url_for(create_account))

        # hash password
        hashed_password = generate_password_hash(password)

        # store user info in db
        students_db.append({
            'user_id': uuid.uuid4().hex,
            'first_name': first_name,
            'last_name': last_name,
            'email': email,
            'password': hashed_password
        })

        flash('Account created successfully!')
        return redirect(url_for('student_login'))

    return render_template('create-account.html')

@app.post('/login')
def student_login():

    user_data = {
        'first_name': user_data['first_name'],
        'last_name': user_data['last_name'],
        'email': user_data['email'],
        'user_id': uuid.uuid4().hex
    }

    return redirect(url_for('home'))
    # return 

'''# route to main page
@app.get('/home/<user_id>')
def home():
    def get_all_institutions():

    return render_template('islandIndex.html')

# get info on all institutions
# future iteration: change route to '/'
@app.get('/')


# get info on institution
@app.get('/<string:inst_id>')
def get_institution(inst_id):
    

## setup institution
@app.post('/')
def create_institution():

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
    '''