import numpy as np
import cv2
import time
import logging
logger = logging.getLogger('root')

class classifier:
    def __init__(self):
        pt = "/Users/jorgealmela/Documents/projects/personal/python/parking_classifier"
        self.net = cv2.dnn.readNetFromCaffe(pt + "/deploy.prototxt", pt + "/parking.caffemodel")
        logger.info("Model loaded and classifier module ready")

    def evaluate(self, path):
        try:
            # logger.info("Evaluating...")
            image = cv2.imread(path)
            blob = cv2.dnn.blobFromImage(image, 1, (224, 224), (104, 117, 123))
            self.net.setInput(blob)
            start = time.time()
            preds = self.net.forward()
            end = time.time()
            logger.info("Classification took {:.5} seconds".format(end - start))
            return(self.build_obj(preds))
        except Exception as err:
            logger.error('Evaluation error')
            return('Evaluation error')

    def build_obj(self, x):
        try:
            aux = x.tolist()
            return({'result': aux[0]})
        except Exception as err:
            logger.error('Error parsing predictions')
            return('Error parsing predictions')

            

