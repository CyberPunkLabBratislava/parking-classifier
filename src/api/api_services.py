from src.classes.classifier import classifier
from PIL import Image
from io import BytesIO
import io
import logging
logger = logging.getLogger('root')

class api_services:
    def __init__(self, config):
        # Initialize classifier
        self.classifier = classifier(config["path"])

    def welcome(self):
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
    
    def crop_and_classify(self, img):
        try:
            result = self.classifier.crop_image(Image.open(io.BytesIO(img))
)
            logger.debug("Parking image classified")
            return(result)
        except Exception as err:
            logger.exception(err)
            return("Problem receiving image")

    def detect(self, img):
        logger.debug("Object detection with parking image")
        return("Under construction")


            

