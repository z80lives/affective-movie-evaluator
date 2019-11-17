import cv2
import dlib
import numpy as np
#from imutils import face_utils
from ferAnalysis import FaceSystem
import time

dlib_detector = dlib.get_frontal_face_detector()
#dlib_detector = dlib.cnn_face_detection_model_v1("./FER/models/mmod_human_face_detector.dat")

sys = FaceSystem()

frame_rate = 16
prev = 0


cap = cv2.VideoCapture("./data/661737f0-3bf4-41ac-9c5e-a9f2147086d6/test.avi")
fps = cap.get(cv2.CAP_PROP_FPS)


while cap.isOpened():
    time_elapsed = time.time() - prev
    ret, frame = cap.read()

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    #faces = sys.detect_faces(gray)
    faces = dlib_detector(frame, 0)

    if len(faces) > 0:
        face = faces[0]
        
        face = (face.left(), face.top(), face.width(), face.height()) #convert from dlib.rectangle
        
        roi = sys.extract_roi(gray, face)
    
        preds = sys.emotion_classifier.predict(roi)[0]
        emotion_probability = np.max(preds)
        label = sys.EMOTIONS[preds.argmax()]

        x,y,w,h = face
        cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0))
        cv2.putText(
	        frame,
	        "%s, %.2f"%(label, emotion_probability),
	        (x,y),
	        cv2.FONT_HERSHEY_SIMPLEX,
	        1,
	        (0,0,128),
	        2
	    )


    
    #if time_elapsed > 1./frame_rate:
    cv2.imshow("FER test", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    time.sleep(1./fps)
    
print("AOK")
