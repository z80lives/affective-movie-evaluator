import cv2

class Webcam:
    def __init__(self):
        self.cap = cv2.VideoCapture(0)

    def setResolution(self, w, h):
        self.cap.set(3 , w)
        self.cap.set(4 , h )

    def setLight(self, brightness=120, contrast=50,
                 saturation=70, hue=13, gain=50, exposure=-3, white_balance=5000):
        cap = self.cap
        cap.set(10, brightness  ) # brightness     min: 0   , max: 255 , increment:1  
        cap.set(11, contrast   ) # contrast       min: 0   , max: 255 , increment:1     
        cap.set(12, saturation   ) # saturation     min: 0   , max: 255 , increment:1

        cap.set(13, hue   ) # hue         
        cap.set(14, gain   ) # gain           min: 0   , max: 127 , increment:1
        cap.set(15, exposure   ) # exposure       min: -7  , max: -1  , increment:1
        cap.set(17, white_balance ) # white_balance  min: 4000, max: 7000, increment:1

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

        
