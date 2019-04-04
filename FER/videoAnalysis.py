from keras.preprocessing.image import img_to_array
import imutils
import cv2
from keras.models import load_model
import numpy as np

test_movie = "C:\\Users\\USER\\Desktop\\affective-movie-evaluator\\data\\1b025e32-2737-4b6c-8394-019f20d9ad34\\test.avi"
camera = cv2.VideoCapture(test_movie)

detection_model_path = 'haarcascade_files/haarcascade_frontalface_default.xml'
emotion_model_path = 'models/_mini_XCEPTION.102-0.66.hdf5'

face_detection = cv2.CascadeClassifier(detection_model_path)

preds = []
EMOTIONS = ["angry" ,"disgust","scared", "happy", "sad", "surprised",
 "neutral"]

while camera.isOpened():
    _, frame = camera.read()

    #face detection
    #frame2 = frame.clone()
    #frame2 = imutils.resize(frame,width=300)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_detection.detectMultiScale(gray,scaleFactor=1.1,minNeighbors=5,minSize=(30,30),flags=cv2.CASCADE_SCALE_IMAGE)
    
    if len(faces) > 0:
    	face = faces[1]
    	x,y, w,h = face
    	cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0))
    #print(faces)

    cv2.imshow("Probabilities", frame)
    #cv2.imshow('your_face', frameClone)
    #cv2.imshow("Probabilities", canvas)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break