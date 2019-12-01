import wx
import cv2
import numpy as np

class VideoPanel(wx.Panel):
    miniBuffer=None
    updateTimer = None
    callbacks={"onFrame": None}
    frame_count=0
    current_frame=0
    state="play"
    onUpdate=None
    def __init__(self, parent):
        super().__init__(parent, wx.ID_ANY, size=(320,200))
        self.fps = 24
        self.frame = 0
        self.vidsrc = None
        self.dc = None
        self._Buffer = wx.Bitmap(*(320,200))

        #self.blank = np.zeros((320,200))
        self.blank = self.getBlankMiniBuffer()
        self.blankMiniBuffer()
        #self.miniBuffer = wx.Bitmap.FromBuffer(320, 200, self.blank)
        self.Layout()

        self.updateTimer = wx.Timer(self, 0)
        self.updateTimer.Start(1000./self.fps)  
        self.Bind(wx.EVT_TIMER, self.update)
        self.Bind(wx.EVT_PAINT, self.onPaint)
                
        #self.Bind(wx.EVT_CLOSE, self.onClose)

    
    def onClose(self, evt):
        if self.updateTimer:
            self.updateTimer.Stop()
            self.updateTimer = None
            self.vidsrc.release()
            #self.Destroy()


    def onPaint(self, evt):
        self.dc = wx.BufferedPaintDC(self, self._Buffer)
        #self.dc.DrawBitmap(self.miniBuffer, 0, 0)

    def blankMiniBuffer(self):
        frame = np.zeros((320,200,3))
        if self.miniBuffer:
            self.miniBuffer.CopyFromBuffer(frame)
        else:
            self.miniBuffer = self.miniBuffer = wx.Bitmap.FromBuffer(320, 200, frame)      
        self.Refresh()

    def getBlankMiniBuffer(self):
        frame = np.zeros((320,200,3))
        return wx.Bitmap.FromBuffer(320, 200, frame)      

    def update(self, dc):
        dc = wx.MemoryDC()
        dc.SelectObject(self._Buffer)
        self.draw(dc)
        if self.state == "stop":
            dc.DrawBitmap(self.getBlankMiniBuffer(),0,0)
        else:
            dc.DrawBitmap(self.miniBuffer,0,0)
        del dc
        self.Refresh(eraseBackground=False)
        self.Update()

        
    def draw(self, dc):
        #self._Bitmap.CopyFromBuffer(frame)
        if self.vidsrc is None or (not self.vidsrc.isOpened()):
            return

        self.vidsrc.set(cv2.CAP_PROP_POS_FRAMES, self.frame-1)
        ret, frame = self.vidsrc.read()
        if ret:
            
            #fram = wx.Bitmap.FromBuffer(640, 480, self.camera.rgbFrame)
            if self.callbacks["onFrame"]:
                self.callbacks["onFrame"](frame)
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)     
            frame = cv2.resize(frame, (320, 200))      
            if self.state == "play": 
                self.frame += 1            
            #print(frame)
            self.miniBuffer.CopyFromBuffer(frame)
            #self._Buffer.CopyFromBuffer(frame)
        #self.Refresh()
        if self.onUpdate:
            self.onUpdate(self.frame_count,self.frame)  


    def stopVideo(self):
        self.state = "stop"        
        #self.updateTimer.Stop()
        self.update(None)
        self.frame = 0
        if self.onUpdate:
            self.onUpdate(self.frame_count,0)   

    def pauseVideo(self):
        self.state = "pause"

    def playVideo(self):
        self.state = "play"
        if not self.updateTimer.IsRunning():
            self.updateTimer.Start()

    def nextFrame(self):
        if self.frame < self.frame_count-1:
            self.frame += 1

    def prevFrame(self):
        if self.frame > 0:
            self.frame -= 1

    def setVideo(self, vid_src):
        self.vidsrc = vid_src
        self.frame = 0
        self.frame_count = vid_src.get(cv2.CAP_PROP_FRAME_COUNT)

class VideoPlayerPanel(wx.Panel):
    vidframe=None 
    play_label=["Play", "Pause"]
    def __init__(self, parent):
        super().__init__(parent, wx.ID_ANY)
        
        #self.vidframe = wx.Panel(self, wx.ID_ANY, size=(320,200))
        self.vidframe = VideoPanel(self)

        v_sizer = wx.BoxSizer(wx.VERTICAL)
        cpanel = self.setupControlPanel()
        
        v_sizer.Add(self.vidframe)
        v_sizer.Add(cpanel)
        self.timeslider = wx.Slider(self, -1, 0, 0, 1000)
        self.timeslider.SetRange(0, 1000)
        self.timeslider.Disable()
        v_sizer.Add(self.timeslider, 1, wx.EXPAND)

        self.SetSizer(v_sizer)
        self.Layout()
        self.bindActions()

        #self.Bind(wx.EVT_PAINT, self.onPaint)
        #self.Bind(wx.EVT_CLOSE, self.onClose)

    #def onPaint(self, evt):
    #    self.vidframe.Refresh()
    def togglePlay(self, evt):
        play_index = self.updatePlayButton()
        if play_index == 0:
            self.vidframe.playVideo()
        else:
            self.vidframe.pauseVideo()

    def updatePlayButton(self):
        play_index = 0
        if self.vidframe.state == "play":
            play_index = 1

        self.btnPlay.SetLabel(self.play_label[play_index])
        return play_index


    def bindActions(self):
        self.btnStop.Bind(wx.EVT_BUTTON, lambda evt: self.vidframe.stopVideo())
        self.btnPlay.Bind(wx.EVT_BUTTON, self.togglePlay)
        self.btnNextFrame.Bind(wx.EVT_BUTTON, lambda evt: self.vidframe.nextFrame())
        self.btnPrevFrame.Bind(wx.EVT_BUTTON, lambda evt: self.vidframe.prevFrame())
        self.timeslider.Bind(wx.EVT_SCROLL_THUMBRELEASE, self.sliderRelease)

    def setupControlPanel(self):
        self.btnPrevFrame = wx.Button(self, wx.ID_ANY, "Prev")
        self.btnPlay = wx.Button(self, wx.ID_ANY, self.play_label[0])
        self.updatePlayButton()
        self.btnStop = wx.Button(self, wx.ID_ANY, "Stop")
        self.btnNextFrame = wx.Button(self, wx.ID_ANY, "Next")
        boxSizer = wx.BoxSizer(wx.HORIZONTAL)
        boxSizer.Add(self.btnPrevFrame)
        boxSizer.Add(self.btnPlay)
        boxSizer.Add(self.btnStop)
        boxSizer.Add(self.btnNextFrame)
        return boxSizer



    def onClose(self, evt):        
        self.vidframe.onClose(evt)                
        self.Destroy()

    def onUpdate(self, frame_count, frame):        
        self.timeslider.SetValue(frame)

    def sliderRelease(self, evt):
        pos = evt.GetPosition()
        print("Slider released", pos) 
        self.vidframe.frame = pos

    def setVideo(self, video_url):
        self.vidframe.setVideo(cv2.VideoCapture(video_url))
        self.timeslider.Enable()
        self.timeslider.SetRange(0, self.vidframe.frame_count)
        self.vidframe.onUpdate=self.onUpdate
