import numpy as np
import cv2
import time
from PIL import Image
import os
import logging
logger = logging.getLogger('root')

class detector:
    def __init__(self, path):
        self.path = path
        self.yolo_path = path + "/model"
        self.confthres = 0.5 # Default 0.3
        self.nmsthres = 0.5 # Default 0.1
        self.labelsPath = "/coco.names"
        self.configPath = "/yolov3.cfg"
        self.weightsPath = "/yolov3.weights"
        self.Labels = self.get_labels()
        self.config = os.path.sep.join([self.yolo_path, self.configPath])
        self.Weights = os.path.sep.join([self.yolo_path, self.weightsPath])
        self.net = self.load_model(self.config, self.Weights)
        self.Colors= self.get_colors(self.Labels)
        
    def get_labels(self):
        # load the COCO class labels our YOLO model was trained on
        #labelsPath = os.path.sep.join([yolo_path, "yolo_v3/coco.names"])
        lpath=os.path.sep.join([self.yolo_path, self.labelsPath])
        LABELS = open(lpath).read().strip().split("\n")
        return LABELS

    def get_colors(self, LABELS):
        # initialize a list of colors to represent each possible class label
        np.random.seed(42)
        COLORS = np.random.randint(0, 255, size=(len(LABELS), 3),dtype="uint8")
        return COLORS

    def load_model(self, configpath, weightsPath):
        # load our YOLO object detector trained on COCO dataset (80 classes)
        logger.info("[INFO] loading YOLO from disk...")
        net = cv2.dnn.readNetFromDarknet(configpath, weightsPath)
        return net

    def get_predection(self, img, output_type):
        npimg=np.array(img)
        image=npimg.copy()
        image=cv2.cvtColor(image,cv2.COLOR_BGR2RGB)
        (H, W) = image.shape[:2]

        # determine only the *output* layer names that we need from YOLO
        ln = self.net.getLayerNames()
        ln = [ln[i[0] - 1] for i in self.net.getUnconnectedOutLayers()]

        # construct a blob from the input image and then perform a forward
        # pass of the YOLO object detector, giving us our bounding boxes and
        # associated probabilities
        blob = cv2.dnn.blobFromImage(image, 1 / 255.0, (416, 416),
                                    swapRB=True, crop=False)
        self.net.setInput(blob)
        start = time.time()
        layerOutputs = self.net.forward(ln)
        # print(layerOutputs)
        end = time.time()

        # show timing information on YOLO
        logger.info("[INFO] YOLO took {:.6f} seconds".format(end - start))

        # initialize our lists of detected bounding boxes, confidences, and
        # class IDs, respectively
        boxes = []
        confidences = []
        classIDs = []

        # loop over each of the layer outputs
        for output in layerOutputs:
            # loop over each of the detections
            for detection in output:
                # extract the class ID and confidence (i.e., probability) of
                # the current object detection
                scores = detection[5:]
                # print(scores)
                classID = np.argmax(scores)
                # print(classID)
                confidence = scores[classID]

                # filter out weak predictions by ensuring the detected
                # probability is greater than the minimum probability
                if confidence > self.confthres:
                    # scale the bounding box coordinates back relative to the
                    # size of the image, keeping in mind that YOLO actually
                    # returns the center (x, y)-coordinates of the bounding
                    # box followed by the boxes' width and height
                    box = detection[0:4] * np.array([W, H, W, H])
                    (centerX, centerY, width, height) = box.astype("int")

                    # use the center (x, y)-coordinates to derive the top and
                    # and left corner of the bounding box
                    x = int(centerX - (width / 2))
                    y = int(centerY - (height / 2))

                    # update our list of bounding box coordinates, confidences,
                    # and class IDs
                    boxes.append([x, y, int(width), int(height)])
                    confidences.append(float(confidence))
                    classIDs.append(classID)

        # apply non-maxima suppression to suppress weak, overlapping bounding
        # boxes
        idxs = cv2.dnn.NMSBoxes(boxes, confidences, self.confthres,
                                self.nmsthres)

        # ensure at least one detection exists
        if len(idxs) > 0:
            # loop over the indexes we are keeping
            for i in idxs.flatten():
                # extract the bounding box coordinates
                (x, y) = (boxes[i][0], boxes[i][1])
                (w, h) = (boxes[i][2], boxes[i][3])

                # draw a bounding box rectangle and label on the image
                color = [int(c) for c in self.Colors[classIDs[i]]]
                cv2.rectangle(image, (x, y), (x + w, y + h), color, 2)
                text = "{}: {:.4f}".format(self.Labels[classIDs[i]], confidences[i])
                cv2.putText(image, text, (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX,0.5, color, 2)

        logger.info(boxes)
        logger.info(confidences)
        logger.info(classIDs)
        if output_type == 'image':
            image=cv2.cvtColor(image,cv2.COLOR_BGR2RGB)
            image=Image.fromarray(image)
            return image
        else:
            result = {"count": len(classIDs)}
            return(result)