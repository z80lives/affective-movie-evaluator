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
    def __init__(self, parent):
        super().__init__(parent, wx.ID_ANY, size=(320,200))
        self.fps = 24
        self.frame = 0
        self.vidsrc = None
        self.dc = None
        self._Buffer = wx.Bitmap(*(320,200))

        #self.blank = np.zeros((320,200,3))
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

    def update(self, dcSrc):
        dc = wx.MemoryDC()
        dc.SelectObject(self._Buffer)
        self.draw(dc)
        dc.DrawBitmap(self.miniBuffer,0,0)
        del dc
        self.Refresh(eraseBackground=False)
        self.Update()
        
    def draw(self, dc):
        #self._Bitmap.CopyFromBuffer(frame)
        if self.vidsrc is None or (not self.vidsrc.isOpened()):
            return
            
        if self.state == "stop":
            frame = np.zeros((320,200,3))
            self.miniBuffer.CopyFromBuffer(frame)
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

    def update_old(self, evt):
        if self.vidsrc is None or (not self.vidsrc.isOpened()):
            self.Refresh(eraseBackground=False)
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
            self.miniBuffer.CopyFromBuffer(frame)
        self.Refresh()

    def stopVideo(self):
        self.state = "stop"
        self.blankMiniBuffer()

    def playVideo(self):
        self.state = "play"

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

    def bindActions(self):
        self.btnStop.Bind(wx.EVT_BUTTON, lambda evt: self.vidframe.stopVideo())
        self.btnPlay.Bind(wx.EVT_BUTTON, lambda evt: self.vidframe.playVideo())
        self.btnNextFrame.Bind(wx.EVT_BUTTON, lambda evt: self.vidframe.nextFrame())
        self.btnPrevFrame.Bind(wx.EVT_BUTTON, lambda evt: self.vidframe.prevFrame())

    def setupControlPanel(self):
        self.btnPrevFrame = wx.Button(self, wx.ID_ANY, "Prev")
        self.btnPlay = wx.Button(self, wx.ID_ANY, "Play")
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

    def setVideo(self, video_url):
        self.vidframe.setVideo(cv2.VideoCapture(video_url))