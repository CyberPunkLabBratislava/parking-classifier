from flask import Flask, request, Response
from src.classes.classifier import classifier
import src.utils.log as log
app = Flask(__name__)
logger = log.setup_custom_logger('root')

# Welcome
logger.debug('Welcome to the classifier app')

# Initialize classifier
classifier = classifier()

# TODO
# LOAD CONFIG FILE PATH AS ARGS AND THEN PARSE IT
# IF DOES NOT EXIST, FALL BACK TO DEFAULTS

# API
@app.route('/', methods=['GET', 'POST'])
def server():
    if request.method == 'GET':
        return "Welcome to parking classifier!"
    else:
        try:
            data = request.get_json()
            result = classifier.evaluate(data['path'])
            return(result)
        except Exception as err:
            logger.error('Problem receiving path')
            return("Problem receiving path")

if __name__ == '__main__':
    app.debug = True
    app.run(port=5000)