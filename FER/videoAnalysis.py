from keras.preprocessing.image import img_to_array
import imutils
import cv2
from keras.models import load_model
import numpy as np

#test_movie = "C:\\Users\\USER\\Desktop\\affective-movie-evaluator\\data\\da012c7f-f39e-4b4b-89b8-76575b7b24d9\\test.avi"
test_movie = "../data/0efad150-04cd-47d5-bd2d-0594662b7064/sample.avi"
#camera = cv2.VideoCapture(0)
camera = cv2.VideoCapture(test_movie)

detection_model_path = 'haarcascade_files/haarcascade_frontalface_default.xml'
emotion_model_path = 'models/_mini_XCEPTION.102-0.66.hdf5'

face_detection = cv2.CascadeClassifier(detection_model_path)
emotion_classifier = load_model(emotion_model_path, compile=False)

preds = []
EMOTIONS = ["angry" ,"disgust","scared", "happy", "sad", "surprised",
 "neutral"]

while camera.isOpened():
    _, frame = camera.read()

    #face detection
    #frame2 = frame.clone()
    #frame2 = imutils.resize(frame,width=300)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_detection.detectMultiScale(gray,scaleFactor=1.5,minNeighbors=5,minSize=(100,100),maxSize=(300,300),flags=cv2.CASCADE_SCALE_IMAGE)
    
    if len(faces) > 0:
    	face = faces[0]
    	x,y, w,h = face
    	cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 255))


    	#extract roi, get region of interest
    	roi = gray[y:y + h, x:x + w]
    	#o = cv2.cvtColor(roi, cv2.COLOR_GRAY2BGR)
    	roi = cv2.resize(roi, (64, 64))
    	roi = roi.astype("float") / 255.0
    	roi = img_to_array(roi)
    	roi = np.expand_dims(roi, axis=0)

    	#cv2.imshow("ROI", o)

    	preds = emotion_classifier.predict(roi)[0]
    	emotion_probability = np.max(preds)
    	label = EMOTIONS[preds.argmax()]

    	print(label, emotion_probability, len(faces))

    	cv2.putText(
					frame,
					"%s, %.2f"%(label, emotion_probability),
					(x,y),
					cv2.FONT_HERSHEY_SIMPLEX,
					1,
					(0,255,255),
					2
					)

    #output
    cv2.imshow("Probabilities", frame)
    #cv2.imshow('your_face', frameClone)
    #cv2.imshow("Probabilities", canvas)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
