import wx
from matplotlib.figure import Figure as Fig
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas
from matplotlib.backends.backend_wxagg import NavigationToolbar2WxAgg as NavigationToolbar

from collections import deque
#import serial
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib as mlp
import numpy as np
import random

class SerialPlotter(wx.Panel):  
    windowSize=10
    displacement=0
    updateCallback=None
    xvals = None
    lastTime = 0
    def __init__(self, parent, windowSize=10):
        super().__init__(parent)
        self.figure = plt.figure(figsize=(20,20))
        self.ax = plt.axes(xlim=(0,10), ylim=(0,600))
        self.plot_data, = self.ax.plot([],[])
        self.canvas = FigureCanvas(self, -1, self.figure)
        self.toolbar = NavigationToolbar(self.canvas)
        self.toolbar.Realize()

        self.timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.update, self.timer)

        self.doLayout()
        self.vals = [] #deque()        
        plt.ion()

        self.timer.Start(1000)

    def doLayout(self):
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.canvas, 1, wx.EXPAND)
        sizer.Add(self.toolbar, 0, wx.RIGHT | wx.EXPAND)
        self.SetSizer(sizer)

    def clear(self):
        #self.ax.clf()
        if self.xvals:
            self.xvals.clear()
        self.vals.clear()

    def update(self, evt):
        #data = float(random.randint(1,50))        
        #self.vals.append(data)
        if self.updateCallback:
            self.updateCallback(self.vals, self)
        length = len(self.vals)

        
        if self.xvals is None:            
            x_end = float(length)
            self.plot_data.set_data(range(length), self.vals)
        else:
            x_start = 0
            x_end = 0
            if len(self.xvals) > 0:
                x_end = self.xvals[-1] + 3           
            self.plot_data.set_data(self.xvals, self.vals)

        #print(length+1)
        
        x_start = x_end - self.windowSize + self.displacement

        if x_start < 0:
            x_start = 0      
        if(x_end < self.windowSize):
            x_end = self.windowSize
        self.ax.set_xlim(x_start, x_end)

        plt.plot()

    #def close(self)