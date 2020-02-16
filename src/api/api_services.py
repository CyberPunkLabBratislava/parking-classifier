from src.classes.classifier import classifier
from src.classes.detector import detector
from PIL import Image
from io import BytesIO
import io
import logging
logger = logging.getLogger('root')

class api_services:
    def __init__(self, config):
        # Initialize classifier
        self.classifier = classifier(config["path"])
        self.detector = detector(config["path"])

    def welcome(self):
        logger.debug("Welcome to cyberlab app")
        return "Welcome to parking classifier!"    
    
    def classify_one(self, img):
        try:
            result = self.classifier.evaluate(Image.open(io.BytesIO(img))
)
            logger.debug("Image tested as " + result)
            return(result)
        except Exception as err:
            logger.exception(err)
            return("Problem receiving image")
    
    def crop_and_classify(self, img, output_type):
        try:
            result = self.classifier.crop_image(Image.open(io.BytesIO(img)), output_type)
            logger.debug("Parking image classified")
            if output_type == 'image':
                imgByteArr = io.BytesIO()
                result.save(imgByteArr, format='PNG')
                return(imgByteArr.getvalue())
            else:
                return(result)
        except Exception as err:
            logger.exception(err)
            return("Problem receiving image")

    def detect(self, img, output_type):
        try:
            result = self.detector.get_predection(Image.open(io.BytesIO(img)), output_type)
            logger.debug("Object detection with parking image")
            if output_type == 'image':
                imgByteArr = io.BytesIO()
                result.save(imgByteArr, format='PNG')
                return(imgByteArr.getvalue())
            else:
                return(result)
        except Exception as err:
            logger.exception(err)
            return("Problem receiving image")


            

