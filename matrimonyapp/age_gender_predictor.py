import cv2
import numpy as np
from django.conf import settings
import os

GENDER_MODEL = os.path.join(settings.BASE_DIR, 'models/gender_net.caffemodel')
GENDER_PROTO = os.path.join(settings.BASE_DIR, 'models/gender_deploy.prototxt')
FACE_PROTO = os.path.join(settings.BASE_DIR, 'models/opencv_face_detector.pbtxt')
FACE_MODEL = os.path.join(settings.BASE_DIR, 'models/opencv_face_detector_uint8.pb')

GENDER_LIST = ['Male', 'Female']

class AgeGenderPredictor:
    def __init__(self):
        self.face_net = cv2.dnn.readNet(FACE_MODEL, FACE_PROTO)
        self.gender_net = cv2.dnn.readNet(GENDER_MODEL, GENDER_PROTO)

    def get_faces(self, frame):
        blob = cv2.dnn.blobFromImage(frame, 1.0, (300, 300), [
                                     104, 117, 123], swapRB=False)
        self.face_net.setInput(blob)
        detections = self.face_net.forward()
        h, w = frame.shape[:2]
        faces = []
        for i in range(detections.shape[2]):
            confidence = detections[0, 0, i, 2]
            if confidence > 0.6:
                box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
                (x1, y1, x2, y2) = box.astype("int")
                faces.append((x1, y1, x2 - x1, y2 - y1))
        return faces

    def predict(self, frame):
        results = []
        faces = self.get_faces(frame)
        for (x, y, w, h) in faces:
            face_img = frame[y:y+h, x:x+w].copy()
            blob = cv2.dnn.blobFromImage(
                face_img, 1.0, (227, 227), (78.4263377603,
                                           87.7689143744, 114.895847746), swapRB=False
            )
            self.gender_net.setInput(blob)
            gender_preds = self.gender_net.forward()
            gender = GENDER_LIST[gender_preds[0].argmax()]

            results.append({
                'gender': gender,
                'box': (x, y, w, h)
            })
        return results