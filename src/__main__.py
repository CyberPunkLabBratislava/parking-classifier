# Importing 3rd party classes
from flask import Flask, request, Response
# Importing custom functions
import src.utils.log as log
import src.utils.parser as parser
# Importing custom class
from src.api.api_services import api_services

# Initialize logger
logger = log.setup_custom_logger('root')

# Parse arguments
config = parser.arg_parser()

# Welcome
logger.debug('Welcome to the classifier app')

# Initialize Flask server
app = Flask(__name__)

# Initialize API
api = api_services(config)

# API
@app.route('/', methods=['GET'])
def fun_1():
    return api.welcome()

@app.route('/test', methods=['POST'])
def fun_2():
    return api.classify_one(request.files["image"].read())

@app.route('/classify', methods=['POST'])
def fun_3():
    result = api.crop_and_classify(request.files["image"].read())
    return Response(response=result, status=200, mimetype="image/jpeg")
    
@app.route('/detect', methods=['POST'])
def fun_4():
    result = api.detect(request.files["image"].read())
    return Response(response=result, status=200, mimetype="image/jpeg")

# Entrypoint
if __name__ == '__main__':
    # Start app
    app.debug = True
    app.run(port=5000)