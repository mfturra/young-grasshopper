import os
import config
import psycopg2
from dotenv import load_dotenv
from configparser import ConfigParser
from flask import Flask, render_template, request

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

# sample university data
island_locals = [
    {
        "local": "bank"
    }
]

# route to main page
@app.get('/')
def home():
    return render_template('islandIndex.html')

@app.get('/home')
def get_locals():
    return { "island_locals": island_locals }

# route to private university workflow
@app.get('/public-university')
def public_university():
    return render_template('universityMain/publicUniversity.html')

@app.post('/public-university')
def create_public_university():
    request_data = request.get_json()
    new_local = { "local": request_data['local'], "students": []}
    island_locals.append(new_local)
    return new_local, 201

# route to public university workflow
@app.get('/private-university')
def private_university():
    return render_template('universityMain/privateUniversity.html')

@app.post('/private-university')
def create_private_university():
    request_data = request.get_json()
    new_local = { "local": request_data['local'], "students": []}
    island_locals.append(new_local)
    return new_local, 201

# create new user for any university
@app.post('/<string:university>/student-enrollment')
def new_student_enrollment(university):
    request_data = request.get_json()

    for local in island_locals:
        # check if university exists
        if local['local'] == university: 
            new_student = { "name": request_data["name"], "email": request_data["email"]}
            
            # store new student in the respective university
            local["students"].append(new_student)

            return new_student, 201
    return {"message": "University not found"}, 404

@app.get('/<string:university>/student-enrollment')
def get_all_students(university):
    # iterate through index and find matching local
    for local in island_locals:
        if local['local'] == university:
            # once located, output results stored in data
            return { "local": local["local"], "students": local["students"]}, 200 #, "students": students["pedro"]}
    return {"message": "University not found"}, 404