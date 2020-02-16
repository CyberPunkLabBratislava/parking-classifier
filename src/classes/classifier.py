from tensorflow.keras.preprocessing import image
from tensorflow.keras.models import load_model 
import numpy as np
import pandas as pd
from PIL import Image, ImageDraw
# import cv2
# import io as StringIO
# import time
import logging
logger = logging.getLogger('root')

class classifier:
    def __init__(self, path):
        self.path = path
        # self.net = cv2.dnn.readNetFromCaffe(path + "/model/deploy.prototxt", path + "/model/parking.caffemodel")
        self.classifier = load_model(self.path + '/model/cnnparking.h5')
        logger.info("Model loaded and classifier module ready")

    def evaluate(self, img):
        try:
            size = 64, 64
            test_image = img.resize(size) # Adapt to size of model
            test_image = test_image.convert('RGB') # Ensure image is RGB, RGBA does not work well
            # test_image.save(self.path + '/' + str(n) + '.jpg')
            test_image = image.img_to_array(test_image)
            test_image = np.expand_dims(test_image, axis=0)
            result = self.classifier.predict(test_image)
            if result[0][0] == 1:
                prediction = 'free'
            else:
                prediction = 'busy'
            # print(prediction)
            return(prediction)

            # Old CAFFE model classifier
            # img = cv2.resize(img, (224, 224))
            # # blob = cv2.dnn.blobFromImage(img, 1, (224, 224), (104, 117, 123))
            # blob = cv2.dnn.blobFromImage(img, 1, (224, 224), (104, 117, 123))
            # self.net.setInput(blob)
            # start = time.time()
            # preds.append(self.net.forward())
            # end = time.time()
            # logger.info("Classification took {:.5} seconds".format(end - start))
            # # return(self.build_obj(preds))

        except Exception as err:
            logger.exception(err)
            return('Evaluation error')
    
    def crop_image(self, img, output_type):
      
        data = pd.read_csv(self.path + '/parkingspots.csv',index_col=0)
        df = pd.DataFrame(data)
        listx1 = tuple(df['x1'])
        listy1 = tuple(df['y1'])
        listx2 = tuple(df['x2'])
        listy2 = tuple(df['y2'])

        npimg=np.array(img)
        parsed_image=npimg.copy()

        images = []
        for i in range(0,len(df)):
            start_point = int(listx1[i]), int(listy1[i])
            end_point = int(listx2[i]), int(listy2[i])
            cropped_area = parsed_image[start_point[1]:end_point[1], start_point[0]:end_point[0]]
            images.append(Image.fromarray(cropped_area))
        
        try:
            results = []
            n = 0
            for i in images:
                n += 1
                results.append({ "id": n, "value": self.evaluate(i)})

            logger.info(results)
            if output_type == 'image':
                final_image = self.print_rectangles(img, results, listx1, listx2, listy1, listy2)
                return(final_image)
            else:
                return(results)
            
        except Exception as err:
            logger.exception(err)
            return('Cropping error')


    def print_rectangles(self, img, results, x1, x2, y1, y2):
        draw = ImageDraw.Draw(img)
        try:
            n=0
            for i in results:
                if i["value"] == "free":
                    color = 'green'
                else:
                    color = 'red'
                draw.rectangle(((int(x1[n]), int(y1[n])), (int(x2[n]), int(y2[n]))), outline=color, width=2)
                n+=1
            draw.text((20, 20), "PARKING CLASSIFIER")
            return img
        except Exception as err:
            logger.exception(err)
            return('Painting rectangles error')


    # def build_obj(self, x):
    #     results = []
    #     try:
    #         for item in x:
    #             aux = item.tolist()
    #             results.append(aux[0])
    #             print(aux[0])
    #         return({'results': results})
    #     except Exception as err:
    #         logger.exception(err)
    #         return('Error parsing predictions')

            

