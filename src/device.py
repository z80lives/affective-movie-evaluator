import cv2
#import wx

class Webcam:
    imgBuffer = None
    rgbFrame = None
    smallRGB=None
    def __init__(self):
        self.open()
        self.fps = 15

    def open(self):
        self.cap = cv2.VideoCapture(0)

    def close(self):
        self.cap.release()
        self.open()

    def read(self):
        ret, self.imgBuffer = self.cap.read()
        self.rgbFrame = cv2.cvtColor(self.imgBuffer, cv2.COLOR_BGR2RGB)
        self.smallRGB = cv2.resize(self.rgbFrame, (320,200))
        return (ret, self.imgBuffer)

    def getSize(self):
        (h,w) = self.imgBuffer.shape[:2]
        return (w,h)

    def setResolution(self, w, h):
        self.cap.set(3 , w)
        self.cap.set(4 , h )

    def checkDevice(self, source):
        cap = cv2.VideoCapture(source) 
        if cap is None or not cap.isOpened():
            print('Warning: unable to open video source: ', source)
            return False
        return True

    def setLight(self, brightness=127, contrast=127,
                 saturation=127, hue=127, gain=50, exposure=-3, white_balance=5000):
        cap = self.cap
        cap.set(10, brightness  ) # brightness     min: 0   , max: 255 , increment:1  
        cap.set(11, contrast   ) # contrast       min: 0   , max: 255 , increment:1     
        cap.set(12, saturation   ) # saturation     min: 0   , max: 255 , increment:1

        cap.set(13, hue   ) # hue         
        cap.set(14, gain   ) # gain           min: 0   , max: 127 , increment:1
        #cap.set(15, exposure   ) # exposure       min: -7  , max: -1  , increment:1
        #cap.set(17, white_balance ) # white_balance  min: 4000, max: 7000, increment:1

    def setFocus(self, v):
        self.cap.set(28, v)
        
    def test_run(self):
        while True:
            ret, img = self.cap.read()
            if not ret:
                break
            
            cv2.imshow("Webcam output", img)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        self.cap.release()
        cv2.destroyAllWindows()

        
