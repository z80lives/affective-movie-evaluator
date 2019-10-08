import cv2
import os
import threading
import uuid
import json

class RecordSystem:    
    def __init__(self):
        self.writer = None
        self.frame_count = 0

    def getWriter(self, filename):
        fourcc = cv2.VideoWriter_fourcc(*'XVID')    
        outsrc = cv2.VideoWriter("./data/"+filename+".avi", fourcc, 20.0, (640, 480))
        self.writer = outsrc
        return outsrc

    def writeFrame(self, frame):
        if self.writer:
            self.writer.write(frame)
            return True
        return False

    def saveWriter(self, writer):
        if writer:
            writer.release()
        writer = None

    def save(self):
        if self.writer:
            self.writer.release()
            self.writer = None

    def set_metadata(self, audience_name, movie_name, movie_year, genre="", tags=""):
        pass

    def play_video(self):
        pass

    def start_recording(self, filename, movie_player=None, showVideo=False, sampleFile=None):
        vidcam = cv2.VideoCapture(0)
        #fourcc = cv2.VideoWriter_fourcc(*'XVID')
        fourcc = cv2.VideoWriter_fourcc(*'MP4V')
        print("Recording sample: %s", sampleFile)
        if sampleFile:
            outsrc = cv2.VideoWriter("./data/"+sampleFile+"/"+filename+".avi", fourcc, 20.0, (640, 480))
        else:
            #outsrc = cv2.VideoWriter("./data/"+filename+".avi", fourcc, 20.0, (640, 480))
            outsrc = cv2.VideoWriter("./data/"+filename+".mp4", fourcc, 20.0, (640, 480))
    
        
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
        print("sample_id: %s"% (sampleFile))
        vidcam.release()
        outsrc.release()
        cv2.destroyAllWindows()
        

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
        with open('meta.json', 'r') as fp:
            data = json.load(fp)
        return data

        
class VLCPlayer:
    onExitCallback=None
    def __init__(self, file_name):
        self.done = False
        self.thread = threading.Thread(target=self.play_movie, args=([file_name,]))
        self.thread.daemon = True                            # Daemonize thread
        self.thread.start()
        self.file_name = file_name

    def play_movie(self, file_name):
        #os.system("cvlc --play-and-exit "+file_name)
        #os.system("cvlc --fullscreen --play-and-exit "+file_name)
        #os.system("cvlc --fullscreen --play-and-exit "+file_name)
        #os.system("\"C:\\Program Files (x86)\\VideoLAN\\VLC\\vlc.exe\" -I dummy --play-and-stop "+file_name)
        os.system("\"C:\\Program Files\\VideoLAN\\VLC\\vlc.exe\" -I dummy --play-and-exit --video-on-top "+file_name)

        print("Movie playback done")
        self.done = True

        if self.onExitCallback:
            self.onExitCallback(self.file_name)
        #if play_movie is not None:                
        #os.system("cvlc --full-screen --play-and-exit "+file_name)
        ##os.system("vlc -I dummy --play-and-stop"+file_name)
    
    def setExitCallback(self, callback):
        self.onExitCallback = callback

    def kill(self):
        pass #Should I let process kill the thread?

    def isAlive(self):
        return not self.done
        #return self.thread.isAlive()
