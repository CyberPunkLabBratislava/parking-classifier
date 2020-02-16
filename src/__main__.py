# Importing 3rd party classes
from flask import Flask, request, Response, jsonify
# Importing custom functions
import src.utils.log as log
import src.utils.parser as parser
# Importing custom class
from src.api.api_services import api_services

# Initialize logger
logger = log.setup_custom_logger('root')

# Welcome
logger.debug('Welcome to the classifier app')

# Parse arguments
config = parser.arg_parser()
# config = {"path": "."}

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
    try:
        result = api.crop_and_classify(request.files["image"].read(), "image")
        return Response(response=result, status=200, mimetype="image/jpeg")
    except Exception as err:
        logger.exception(err)
        return('Evaluation error')
    
@app.route('/detect', methods=['POST'])
def fun_4():
    result = api.detect(request.files["image"].read(), "image")
    return Response(response=result, status=200, mimetype="image/jpeg")

@app.route('/classify/data', methods=['POST'])
def fun_5():
    try:
        result = api.crop_and_classify(request.files["image"].read(), "data")
        return jsonify(result)
    except Exception as err:
        logger.exception(err)
        return('Evaluation error')
    
@app.route('/detect/data', methods=['POST'])
def fun_6():
    result = api.detect(request.files["image"].read(), "data")
    return jsonify(result)

# Entrypoint
if __name__ == '__main__':
    # Start app
    # app.debug = True
    app.run(port=config.port, host=config.host)