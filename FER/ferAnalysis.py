
import cv2
import numpy as np
import imutils
from datetime import timedelta
import time
		

class FaceSystem:
	def __init__(self):
		from keras.preprocessing.image import img_to_array
		from keras.models import load_model
		self.img_to_array = img_to_array
		detection_model_path = 'FER/haarcascade_files/haarcascade_frontalface_default.xml'
		emotion_model_path = 'FER/models/_mini_XCEPTION.102-0.66.hdf5'

		self.face_detection = cv2.CascadeClassifier(detection_model_path)
		self.emotion_classifier = load_model(emotion_model_path, compile=False)

		self.preds = []
		self.EMOTIONS = ["angry" ,"disgust","scared", "happy", "sad", "surprised", "neutral"]

	def detect_faces(self, gray):
		#detect faces
		faces = self.face_detection.detectMultiScale(gray,scaleFactor=1.05,minNeighbors=5,minSize=(30,30),maxSize=(300,300),flags=cv2.CASCADE_SCALE_IMAGE)
		return faces

	##
	def extract_roi(self, gray, rect):
		x,y, w,h = rect

		#extract roi
		roi = gray[y:y + h, x:x + w]
		roi = cv2.resize(roi, (64, 64))
		roi = roi.astype("float") / 255.0
		roi = self.img_to_array(roi)
		roi = np.expand_dims(roi, axis=0)
		return roi


	def analyse(self, video_file, showVideo=False):
		cap = cv2.VideoCapture(video_file)
		length = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))


		data =[]
		c= 0
		last_inference_time = 0
		average_inference = 0.0
		remaining_time = 0.00
		while cap.isOpened():
			ret, frame = cap.read()
			c = c+ 1.0
			if ret == False:
				print("Cannot play ", video_file)
				break

			progress = c
			print("Progress = %d/%d, time=%.2f avg=%.2f, remaining=%s \r" % (progress, length, last_inference_time, average_inference, str(timedelta(seconds=remaining_time))), end="")
			start_time = time.time()
			
			gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
			faces = self.detect_faces(gray)
    
			#fetch the first face
			if len(faces) > 0:
				face = faces[0]

				roi = self.extract_roi(gray, face)

				preds =self. emotion_classifier.predict(roi)[0]
				emotion_probability = np.max(preds)
				label = self.EMOTIONS[preds.argmax()]
				#print(c, label, emotion_probability)

				if showVideo:
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

			if showVideo:
				cv2.imshow("EmotionPredictions", frame)
				if cv2.waitKey(1) & 0xFF == ord('q'):
					break


			last_inference_time = time.time() - start_time
			if c > 1:
				average_inference = ( (average_inference* (c-1)) + last_inference_time) / c
			else:
				average_inference = last_inference_time
			remaining_time = (length - c) * average_inference
		
		cap.release()
		cv2.destroyAllWindows()
