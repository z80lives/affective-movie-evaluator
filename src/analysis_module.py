import time
from datetime import timedelta
import cv2
import numpy as np

class PoseAnalyser:
    #def _print(*args, **kwargs):
    #    print(args, kwargs)
    last_inference_time = 0
    average_inference = 0.0
    remaining_time = 0.00
        
    def viewKeypointsOnSample(self, sample_dir, sample_type="mixed", drawKeypoints=None, options={}):
        if drawKeypoints is None:
            self._print("Please provide a draw key_point method")
            return
        
        video_file = sample_dir+"test.avi"
        keypoint_file  = sample_dir+sample_type+"_points.npy"
        keypoints = np.load(keypoint_file)
        cap = cv2.VideoCapture(video_file)
        length = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))        

        fps = cap.get(cv2.CAP_PROP_FPS)
        
        c=0

        if length != len(keypoints):
            self._print("Number of keypoints less than the number of frames")
            return

        while cap.isOpened():
            ret, raw_img = cap.read()
            c = c+1
            if ret == False:
                break

            img = raw_img

            kp = keypoints[c-1]
            img = drawKeypoints(img, kp, options=options)

            cv2.imshow("keypoints", img)
            time.sleep(1./fps)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break


    def getTime(self):
        return self.time
    
    def analyse(self, video_file, out_file, showVideo=False, infer_method=None, print=print):
        self._print =print
        if infer_method == None:
            self._print("Please provide an infer method")
            return

        data =[]
        cap = cv2.VideoCapture(video_file)
        length = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        self.last_inference_time = 0
        self.average_inference = 0.0
        self.remaining_time = 0.00

        c = 0
        while cap.isOpened():
            ret, raw_img = cap.read()
            c = c + 1.0

            if ret == False:
                self._print("Cannot open ", video_file)
                break

            progress = c
            tdelta = str(timedelta(seconds=self.remaining_time))
            self._print("Progress = %d/%d Remaining:%s %.2fs/f \r" % (progress, length, tdelta, self.average_inference), end="")
            
            start_time = time.time()
            output = infer_method(raw_img)
            self.last_inference_time = time.time()- start_time

            if c > 1:
                self.average_inference = ( (self.average_inference * (c-1)) + self.last_inference_time)/c
            else:
                self.average_inference = self.last_inference_time

            self.remaining_time = (length - c) * self.average_inference

            data.append(output)
            if showVideo:
                cv2.imshow("Pose Capture", raw_img)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break

        npdata = np.array(data)
        np.save(out_file, npdata)

        cap.release()
        cv2.destroyAllWindows()
