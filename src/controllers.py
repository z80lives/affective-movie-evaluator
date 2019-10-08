import wx
from src.gsr import GSRSensor
from src.device import Webcam
import cv2
import numpy as np 
import time

class MainControllerObject(object):
    timer=None
    cameraTimer=None
    cameraBuffer=None
    miniBuffer=None
    refreshFrames={}
    isRecording=False
    callbacks={"onFrame": None, "onEnd": None, "onGSR": None}
    edaFrames = []
    edaFrameWindow = []
    edaStartTime = None
    edaWindowLimit=(0, 10)
        


    def setRecordFrameEvent(self, callback):
        self.callbacks["onFrame"] = callback

    def setRecordEndEvent(self, callback):
        self.callbacks["onEnd"] = callback

    def __init__(self):
        self.print("Main controller initialized")
        self.gsr = GSRSensor()
        self.camera = Webcam()
        self.blankMiniBuffer()
        self.Bind(wx.EVT_TIMER, self.onTimer)

    def start_gsr(self):
        if self.timer is None:
            gsr_ok = self.gsr.openPort()
            if gsr_ok:          
                self.timer = wx.Timer(self, 1)
                self.timer.Start(1000./60)               
                #self.Bind(wx.EVT_TIMER, self.readGSR)
                self.edaFrames = []
                self.edaStartTime = time.time()
                self.print("GSR Active")                
            else:
                self.print("Failed to initialise GSR sensor. Make sure it is connected properly.")
                return False
        return True

    def start_camera(self):
        if self.cameraTimer is None:
            self.camera.read()
            self.cameraTimer = wx.Timer(self, 0)
            self.cameraTimer.Start(1000./self.camera.fps)                    
            width, height = self.camera.getSize()
            self.cameraBuffer = wx.Bitmap.FromBuffer(width, height, self.camera.rgbFrame)

            if not self.miniBuffer:
                self.miniBuffer = wx.Bitmap.FromBuffer(320, 200, self.camera.smallRGB)
            #self.cameraBuffer.CopyFromBuffer(self.camera.rgbFrame)
            #self.Bind(wx.EVT_PAINT, self.OnPaint)
            #self.Bind(wx.EVT_TIMER, self.updateFromCamera)

    def onTimer(self, evt):
        timerobj = evt.GetTimer()
        if timerobj == self.timer:
            self.readGSR(evt)
        elif timerobj == self.cameraTimer:
            self.updateFromCamera(evt)
        
    def OnPaint(self, evt):
        for key in self.refreshFrames:
            frame, size = self.refreshFrames[key]
            dc = wx.BufferedPaintDC(frame)
            if size is None:
                dc.DrawBitmap(self.cameraBuffer, 0, 0)
            else:
                dc.DrawBitmap(self.miniBuffer, 0, 0)

    def addCameraFrame(self, frame, key, size=None):
        self.refreshFrames[key] = (frame, size)
        frame.Bind(wx.EVT_PAINT, self.OnPaint)

    def removeCameraFrame(self, key):
        self.refreshFrames[key][0].Unbind(wx.EVT_PAINT)
        self.refreshFrames[key] = None        

    def updateFromCamera(self, evt):
        ret, frame = self.camera.read()
        if ret:
            #self.cameraBuffer = wx.Bitmap.FromBuffer(640, 480, self.camera.rgbFrame)
            if self.callbacks["onFrame"]:
                self.callbacks["onFrame"](frame)
            #frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)            
            self.cameraBuffer.CopyFromBuffer(self.camera.rgbFrame)
                        
            frame = cv2.resize(self.camera.rgbFrame, (320, 200))
            self.miniBuffer.CopyFromBuffer(frame)
            for key in self.refreshFrames:
                self.refreshFrames[key][0].Refresh()
            #self.Refresh()

    def stop_camera(self):
        if self.cameraTimer:
            #if self.callbacks["onEnd"]:
            #    self.callbacks["onEnd"]()
            self.cameraTimer.Stop()
            #self.camera.
            self.cameraTimer = None
            self.camera.close()
            self.blankMiniBuffer()
            #self.camera.None()

    def blankMiniBuffer(self):
        frame = np.zeros((320,200,3))
        if self.miniBuffer:
            self.miniBuffer.CopyFromBuffer(frame)
        else:
            self.miniBuffer = self.miniBuffer = wx.Bitmap.FromBuffer(320, 200, frame)
        for key in self.refreshFrames:
            self.refreshFrames[key][0].Refresh()

    def stop_gsr(self):
        if self.timer:
            self.timer.Stop()
            self.gsr.closePort()
            self.timer = None

    def readGSR(self, evt):
        val = self.gsr.readVal()    
        if val and val.strip():
            edaval = int(val)
            time_elapsed = time.time() - self.edaStartTime
            self.edaFrames.append((time_elapsed, edaval))
            if self.callbacks["onGSR"]:
                self.callbacks["onGSR"](edaval)
            #self.edaFrameWindow.append((time_elapsed, edaval))  
            #self.cutEDAWindow()                  

            #self.print("%i"%edaval)

    def cutEDAWindow(self):
        limit = self.edaWindowLimit[1]
        if len(self.edaFrameWindow) > limit:
            self.edaFrameWindow = self.edaFrameWindow[:-limit]

    def mainControllerQuit(self):
        """
        Triggered by OnClose event of the main frame.
        """
        self.stop_camera()
        self.stop_gsr()

    def saveEDAFile(self, filename):
        csv_lines = []
        for (x, val) in self.edaFrames:
            csv_lines.append([x, int(val)])
        np.savetxt(filename, csv_lines, delimiter=",")
