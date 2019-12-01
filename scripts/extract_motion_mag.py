#from keras.preprocessing.image import img_to_array
import imutils
import cv2
#from keras.models import load_model
import numpy as np
import pandas as pd
import os
import matplotlib.pyplot as plt

#import ext.facenet.align.detect_face as fn_detector #use facenet detector

#test_movie = "C:\\Users\\USER\\Desktop\\affective-movie-evaluator\\data\\da012c7f-f39e-4b4b-89b8-76575b7b24d9\\test.avi"

#import dlib

#detector = dlib.get_frontal_face_detector()
align = None

detection_model_path = './models/haarcascade_files/haarcascade_frontalface_default.xml'

face_detection = cv2.CascadeClassifier(detection_model_path)

re_adjust_frame = 100 #readjust roi every nth frame
adjust_counter = 0


import tensorflow as tf
class FaceAligner(object):
	def __init__(self):
		with tf.Graph().as_default():
			gpu_options = tf.GPUOptions(per_process_gpu_memory_fraction=1.0)
			sess = tf.Session(config=tf.ConfigProto(gpu_options=gpu_options, log_device_placement=False))
			with sess.as_default():
				self.pnet, self.rnet, self.onet = fn_detector.create_mtcnn(sess, None)
		self.minsize = 20
		self.threshold = [ 0.6, 0.7, 0.7 ]
		self.factor = 0.709
		self.margin=44
		print("Initialised")

	def detect(self, frame):
		aligned_bb, _ = fn_detector.detect_face(frame, self.minsize, self.pnet, self.rnet, self.onet, self.threshold, self.factor)
		if len(aligned_bb) >= 1:
			img_size = np.asarray(frame.shape)[0:2]
			det = np.squeeze(aligned_bb[0,0:4])
			bb = np.zeros(4, dtype=np.int32)
			bb[0] = np.maximum(det[0]-self.margin/2, 0)
			bb[1] = np.maximum(det[1]-self.margin/2, 0)
			bb[2] = np.minimum(det[2]+self.margin/2, img_size[1])
			bb[3] = np.minimum(det[3]+self.margin/2, img_size[0])
			cropped = frame[bb[1]:bb[3],bb[0]:bb[2],:]
			aligned = cv2.resize(cropped, (64, 64))				
			return aligned
		return None

#align_mode="facenet_align"
def extract_features(camera, align_mode=None):
	preds = []	

	windowSize=100
	displacement=0
	figure = plt.figure(figsize=(10,10))
	ax = plt.axes(xlim=(0,10), ylim=(340,600))
	#plt.xlim(0,10)
	plt.ylim(0,3)
	plot_data, = ax.plot([],[])
	
	plt.ion()

	#aligner = FaceAligner()
	#prvs = cv.cvtColor(frame1,cv.COLOR_BGR2GRAY)
	

	prev = None
	init_detect_pos = None
	#plt.draw()
	
	while camera.isOpened():
		ret, frame = camera.read()
		
		mean_mag = 0
		if not ret:
			break

		orig_frame = frame.copy()

		

		gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
		faces = face_detection.detectMultiScale(gray,scaleFactor=1.5,minNeighbors=5,minSize=(100,100),maxSize=(300,300),flags=cv2.CASCADE_SCALE_IMAGE)
		
		roi = None
		roi_col = None
		if align_mode == "facenet_align":
			aligned = aligner.detect(frame)
			if aligned is not None:
				cv2.imshow('algined',  aligned)
			roi = cv2.cvtColor(aligned, cv2.COLOR_BGR2GRAY)
			roi_col = aligned
			#aligned = misc.imresize(cropped, (160, 160), interp='bilinear')

		
		#dets = detector(orig_frame, 1)

		if roi is None and len(faces) > 0:
			face = faces[0]
			x,y, w,h = face
			cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 255))
			kernel = np.ones((5, 5), np.uint8) #cleanup a bit
			orig_frame = cv2.dilate(orig_frame, kernel, iterations = 1)
			#extract roi, get region of interest
			roi = gray[y:y + h, x:x + w]
			roi_col = orig_frame[y:y + h, x:x + w]

			if init_detect_pos is None or adjust_counter == re_adjust_frame:
				init_detect_pos = x, y, w, h
				adjust_counter = 0
			else:
				x, y, w, h = init_detect_pos
				roi_col = orig_frame[y:y + h, x:x + w]
			adjust_counter += 1

		if roi is not None:
			
			roi = cv2.resize(roi, (64, 64))
			roi_col = cv2.resize(roi_col, (164, 164))

			
			if prev is None:
				prev = cv2.cvtColor(roi_col, cv2.COLOR_BGR2GRAY)
				hsv = np.zeros_like(roi_col)
				hsv[...,1] = 255
				print(hsv.shape)
			else:
				#nextImg = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
				nextImg = cv2.cvtColor(roi_col, cv2.COLOR_BGR2GRAY)
				flow = cv2.calcOpticalFlowFarneback(prev,nextImg, None, 0.5, 3, 15, 3, 5, 1.2, 0)
				mag, ang = cv2.cartToPolar(flow[...,0], flow[...,1])

				hsv[...,0] = ang*180/np.pi/2
				hsv[...,2] = cv2.normalize(mag,None,0,255,cv2.NORM_MINMAX)
				bgr = cv2.cvtColor(hsv,cv2.COLOR_HSV2BGR)
				cv2.imshow('optical_flow',bgr)
				mean_mag = np.mean(mag)

				xvals = np.arange(len(preds))

				x_start = 0
				x_end = 0
				if len(xvals) > 0:
					x_end = xvals[-1] + 3 
				x_start = x_end - windowSize + displacement
				if x_start < 0:
					x_start = 0      
				if(x_end < windowSize):
					x_end = windowSize
				ax.set_xlim(x_start, x_end)

				#sc.set_offsets(np.c_[xvals,preds])
				plot_data.set_data(xvals,preds)
				figure.canvas.draw_idle()
				plt.pause(0.01)


				
				#plt.plot([0,0,1],[1,1,0])
				#print(mean_mag)
				prev = nextImg

			#plt.plot()
			#plt.draw()
			#roi = roi.astype("float") / 255.0
			#roi = img_to_array(roi)
			#roi = np.expand_dims(roi, axis=0)
			

			#print(label, emotion_probability, len(faces))

		preds.append(mean_mag)
		#output
		cv2.imshow("Probabilities", frame)
		if roi is not None:
			cv2.imshow("Face", roi)
		key = cv2.waitKey(1) & 0xFF
		if key == ord('a'):
			break

		#cv2.imshow('your_face', frameClone)
		#cv2.imshow("Probabilities", canvas)
		#if cv2.waitKey(1) & 0xFF == ord('q'):
		#	break
	plt.close("all")
	camera.release()
	return preds

#camera = cv2.VideoCapture("./data/0efad150-04cd-47d5-bd2d-0594662b7064/sample.avi")
#emotion_data = extract_features(camera)

sample_ids = [x[0] for x in os.walk("./data")]
for sample_id in sample_ids:
    #test_movie = "../data/0efad150-04cd-47d5-bd2d-0594662b7064/sample.avi"
    print("Processing ", sample_id)
    vid_file = sample_id+"/sample.avi"
    camera = cv2.VideoCapture(vid_file)
    #camera = cv2.VideoCapture(test_movie)
    emotion_data = extract_features(camera)
    df = pd.DataFrame(emotion_data)
    df.to_csv(sample_id+"/motion_history.csv")
