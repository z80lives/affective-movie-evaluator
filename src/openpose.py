#from imutils import  url_to_image, opencv2matplotlib
#from matplotlib import pyplot as plt
import cv2
import time
from datetime import timedelta
import numpy as np

class PoseSystem:
    def __init__(self):
        protoFile = "./BEGR/models/pose_deploy_linevec_faster_4_stages.prototxt"
        weightsFile = "./BEGR/models/pose_iter_160000.caffemodel"
        self.net = cv2.dnn.readNetFromCaffe(protoFile, weightsFile)
        self.inWidth = 368
        self.inHeight = 368

    def infer(self, img):
        inpBlob = cv2.dnn.blobFromImage(img, 1.0 / 255,
                                        (self.inWidth, self.inHeight),
                                        (0, 0, 0), swapRB=False, crop=False)
        self.net.setInput(inpBlob)
        output = self.net.forward()
        return output

    def drawKeypoints(self, frame, keypoints, threshold=0.5):
        H = keypoints.shape[2]
        W = keypoints.shape[3]

        frame_out = frame.copy()
        points = []

        frameWidth = frame.shape[1]
        frameHeight = frame.shape[0]

        for i in range(0, 15):
            probMap = keypoints[0, i, :, :]
            minVal, prob, minLoc, point = cv2.minMaxLoc(probMap)

            x = (frameWidth * point[0]) / W
            y = (frameHeight * point[1]) / H
            print(i, x, prob)

            if prob > threshold :
                cv2.circle(frame_out, (int(x), int(y)), 15, (0, 255, 255), thickness=-1, lineType=cv2.FILLED)
                cv2.putText(frame_out, "{}".format(i), (int(x), int(y)), cv2.FONT_HERSHEY_SIMPLEX, 1.4, (0, 0, 255), 3, lineType=cv2.LINE_AA)
                points.append((int(x), int(y)))
            else:
                points.append(None)
                
        return frame_out

    def viewKeypointsOnSample(self, sample_dir):
        video_file = sample_dir+"test.avi"
        keypoint_file  = sample_dir+"body_points.npy"
        keypoints = np.load(keypoint_file)
        cap = cv2.VideoCapture(video_file)
        length = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

        c= 0
        if length != len(keypoints):
            print("Number of keypoints less than the number of frames")
            return
        
        while True:
            ret, raw_img = cap.read()
            c = c+1
            if ret == False:
                break

            img = raw_img

            kp = keypoints[c]
            img = self.drawKeypoints(img, kp, threshold=0.2)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break


    def analyse(self, video_file, out_file, showVideo=False):
        cap = cv2.VideoCapture(video_file)
        length = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        
        data =[]
        c= 0
        last_inference_time = 0
        average_inference = 0.0
        remaining_time = 0.00
        while True:
            ret, raw_img = cap.read()
            c = c+ 1.0
            if ret == False:
                print("Cannot play ", video_file)
                break


            progress = c
            print("Progress = %d/%d, time=%.2f avg=%.2f, remaining=%s \r" % (progress, length, last_inference_time, average_inference, str(timedelta(seconds=remaining_time))), end="")

            start_time = time.time()
            output = self.infer(raw_img)
            last_inference_time = time.time() - start_time

            if c > 1:
                average_inference = ( (average_inference* (c-1)) + last_inference_time) / c
            else:
                average_inference = last_inference_time
            remaining_time = (length - c) * average_inference

            #print(output)            
            data.append(output)
            if showVideo:
                cv2.imshow("out", raw_img)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break

        npdata = np.array(data)
        np.save(out_file, npdata)
        
        cap.release()
        cv2.destroyAllWindows()

    
