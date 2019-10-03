import wx
import wx.grid as gridlib

class SampleTabFrame(wx.Frame):
     def __init__(self):
        """Constructor"""
        wx.Frame.__init__(self, wx.GetApp().TopWindow, title="Sample Window")
        #wx.Frame.__init__(self, parent=None, title="A Simple Grid")
        panel = wx.Panel(self)
 
        myGrid = gridlib.Grid(panel)
        myGrid.CreateGrid(12, 8)
        myGrid.DisableCellEditControl()
 
        self.setIcon()
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(myGrid, 1, wx.EXPAND)        
        panel.SetSizerAndFit(sizer)
        #panel.SetSizer(sizer)
        panel.Layout()
        self.Fit()
 
     def setIcon(self):
        icon = wx.Icon()
        icon.CopyFromBitmap(wx.Bitmap("./src/icon.ico", wx.BITMAP_TYPE_ANY))
        self.SetIcon(icon)

class SampleTabPanel(wx.Panel):   
    def __init__(self, parent, event_handler):
        super().__init__(parent, wx.ID_ANY)
        self.parent = parent
        self.event_handler = event_handler
        #wx.Table
        #self.do_layout()

        myGrid = gridlib.Grid(self)
        myGrid.CreateGrid(12, 8)
 
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(myGrid, 1, wx.EXPAND)
        self.SetSizer(sizer)
        self.Layout()

    def do_layout(self):
        pass

    def do_bind(self):
        pass