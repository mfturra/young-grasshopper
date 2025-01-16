from flask import Flask
from flask_smorest import Api

from resources.institution import blp as InstitutionBlueprint
from resources.degree import blp as DegreeBlueprint

# initialize app
app = Flask(__name__) 
# flask --app app-v2 run

app.config["PROPAGATE_EXCEPTIONS"] = True
app.config["API_TITLE"] = "Young Grasshopper REST API"
app.config["API_VERSION"] = "v1"
app.config["OPENAPI_VERSION"] = "3.0.3"
app.config["OPENAPI_URL_PREFIX"] = "/docs"
app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"

api = Api(app)

api.register_blueprint(DegreeBlueprint)
api.register_blueprint(InstitutionBlueprint)