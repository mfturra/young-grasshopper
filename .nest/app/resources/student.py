import uuid
from flask import render_template, request
from flask.views import MethodView
from flask_smorest import Blueprint, abort 

from prelim_db import students

blp = Blueprint("Students", __name__, description="Operations on students")


@blp.route('/index')
class StudentLogin(MethodView):
    def get(self):
       try:
          return render_template('user_login.html')
       except KeyError:
           abort(404, message="Login page wasn't found.")

@blp.route("/<string:inst_id>")
class Student(MethodView):
    def get(self, student):


    def post(self, student):

        try:
            user_data = request.form.to_dict()

            # if user_data['email'] == user_db['email']:
            #     return 403, {'message': 'This email pertains to another user. Please create your account with another email.'}

            user_data = {
                'first_name': user_data['first_name'],
                'last_name': user_data['last_name'],
                'email': user_data['email'],
                'user_id': uuid.uuid4().hex
            }

            return redirect(url_for('home'))