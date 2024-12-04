from flask import Flask, render_template

# initialize app
app = Flask(__name__)

# route to main page
@app.route('/')
def home():
    return render_template('islandIndex.html')

# route to private university workflow
@app.route('/public-university')
def publicUniversity():
    return render_template('universityMain/publicUniversity.html')

# route to public university workflow
@app.route('/private-university')
def privateUniversity():
    return render_template('universityMain/privateUniversity.html')