#!/usr/bin/env python
from __future__ import print_function

import wx
from src.wx.event_handlers import CPanelEventHandlers
#import builtins as __builtin__
#define


frame = None


import builtins as __builtin__

def print(*args, **kwargs):
    if frame is None:
        return __builtin__.print(*args, **kwargs)
    else:
        frame.print(*args, **kwargs)

        

class ControlPanelFrame(wx.Frame, CPanelEventHandlers):
    def createMenus(self):
        filemenu = wx.Menu()                
        newItem = filemenu.Append(wx.ID_NEW, "&New Record", "Create a new Recording")        
        aboutItem = filemenu.Append(wx.ID_ABOUT, "&About", "Application Information")
        
        filemenu.AppendSeparator()
        exitItem = filemenu.Append(wx.ID_EXIT, "E&xit", "Quit Program")

        viewmenu = wx.Menu()
        samplesItem = viewmenu.Append(wx.ID_ANY, "Sa&mples", "View Samples")        

        self.Bind(wx.EVT_MENU, self.onNew, newItem)
        self.Bind(wx.EVT_MENU, self.onAbout, aboutItem)
        self.Bind(wx.EVT_MENU, self.onQuit, exitItem)

        self.Bind(wx.EVT_MENU, self.onSampleMenu, samplesItem)
        
        return {
            "&File": filemenu,
            "&View": viewmenu
        }

    
    def __init__(self, title):
        #I'm avoiding wx.RESIZE_BORDER because I use i3wm stack window manager for my own system.
        custom_style= wx.MINIMIZE_BOX | wx.MAXIMIZE_BOX |wx.FRAME_FLOAT_ON_PARENT| wx.SYSTEM_MENU | wx.CAPTION | wx.CLOSE_BOX
        
        wx.Frame.__init__(self, None, title=title,
                          size=(1024,720),
                          style=custom_style
        )
        #self.control = wx.TextCtrl(self, style=wx.TE_MULTILINE)
        self.panel_notebook = wx.Notebook(self, wx.ID_ANY)
        self.txtConsole = wx.TextCtrl(self, wx.ID_ANY, "", style=wx.TE_MULTILINE | wx.TE_PROCESS_ENTER | wx.TE_PROCESS_TAB | wx.TE_READONLY)
        #self.text_area = wx.TextCtrl(self, wx.ID_ANY, "")
        
        self.CreateStatusBar()

        menubar = wx.MenuBar()
        menus = self.createMenus()
        for k in menus:
            menubar.Append(menus[k], k)
        
        self.SetMenuBar(menubar)        
        self.Show(True)

        self.txtConsole.SetMinSize((90, 23))

        self.do_layout()
        #self.print("Hello")

        #ConsoleUI = self
        

    def print(self, *args, **kwargs):
        self.txtConsole.SetValue(*args)
        

    def do_layout(self):
        self.context_sizer = wx.BoxSizer(wx.VERTICAL)
        self.context_sizer.Add(self.panel_notebook, 0, wx.ALL | wx.EXPAND, 1)
        self.context_sizer.Add(self.txtConsole, 2, wx.ALL | wx.EXPAND, 1)
        #self.context_sizer.Add(self.text_area, 0, wx.ALL, 0)

        #recordTab = RecordTabPanel(self.panel_notebook)
        #self.panel_notebook.AddPage(recordTab, "Record Screening")
        
        self.SetSizer(self.context_sizer)
        self.Layout()

app = wx.App(False)
frame = ControlPanelFrame("Affective Movie Evaluator ControlPanel")
app.MainLoop()


