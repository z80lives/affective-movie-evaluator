import cv2
import os
import threading
import uuid
import json

class RecordSystem:        
    def select_file(self, filename):
        pass

    def set_metadata(self, audience_name, movie_name, movie_year, genre="", tags=""):
        pass

    def play_video(self):
        pass

    def start_recording(self, filename, movie_player=None, showVideo=False, sampleFile=None):
        vidcam = cv2.VideoCapture(0)
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        if sampleFile:
            outsrc = cv2.VideoWriter("./data/"+sampleFile+"/"+filename+".avi", fourcc, 20.0, (640, 480))
        else:
            outsrc = cv2.VideoWriter("./data/"+filename+".avi", fourcc, 20.0, (640, 480))
    
        
        while True:
            _, raw_img = vidcam.read()

            if showVideo:
                cv2.imshow("out", raw_img)
            
            out_img = cv2.resize(raw_img, (640,480))
            outsrc.write(out_img)

            if movie_player:
                if not movie_player.isAlive():
                    break
            
            if showVideo and (cv2.waitKey(1) & 0xFF == ord('q')):
                break

        print("Done")
        vidcam.release()
        outsrc.release()

    def generateFileName(self):
        return str(uuid.uuid4())

    def createSampleDir(self):
        filename = self.generateFileName()
        os.mkdir("./data/"+filename)
        return filename

    def saveMetaData(self, filename, data):        
        with open("./data/"+filename+'/meta.json', 'w') as fp:
            json.dump(data, fp)
        
    def loadMetaData(self, filename):        
        with open('data.json', 'r') as fp:
            data = json.load(fp)
        return data

        
class VLCPlayer:
    def __init__(self, file_name):
        self.done = False

        self.thread = threading.Thread(target=self.play_movie, args=([file_name,]))
        self.thread.daemon = True                            # Daemonize thread
        self.thread.start()

    def play_movie(self, file_name):
        #os.system("cvlc --play-and-exit "+file_name)
        os.system("cvlc --fullscreen --play-and-exit "+file_name)
        print("Movie playback done")
        self.done = True
        #if play_movie is not None:                
        #os.system("cvlc --full-screen --play-and-exit "+file_name)
        ##os.system("vlc -I dummy --play-and-stop"+file_name)

    def isAlive(self):
        return not self.done
        #return self.thread.isAlive()
