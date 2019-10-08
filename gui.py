#!/usr/bin/env python
from __future__ import print_function

import wx
from src.wx.event_handlers import CPanelEventHandlers
from src.controllers import MainControllerObject

#import builtins as __builtin__
#define
#import os
import platform

frame = None
__MEM_VERSION__ = "0.1 alpha-92019"   #{release_number}.{iteration} release_type-{month}{year}

import builtins as __builtin__

def print(*args, **kwargs):
    if frame is None:
        return __builtin__.print(*args, **kwargs)
    else:
        frame.print(*args, **kwargs)

        

class ControlPanelFrame(wx.Frame, CPanelEventHandlers, MainControllerObject):
    def createMenus(self):
        filemenu = wx.Menu()                
        newItem = filemenu.Append(wx.ID_NEW, "&New Record", "Create a new Recording")          
        aboutItem = filemenu.Append(wx.ID_ABOUT, "&About", "Application Information")
        
        filemenu.AppendSeparator()
        exitItem = filemenu.Append(wx.ID_EXIT, "E&xit", "Quit Program")

        viewmenu = wx.Menu()
        samplesItem = viewmenu.Append(wx.ID_ANY, "Sa&mples", "View Samples")        
        manage_movie = viewmenu.Append(wx.ID_ANY, "Manage &Movies", "Add/Edit/Delete movies from the system",  kind=wx.ITEM_CHECK)
        manage_people = viewmenu.Append(wx.ID_ANY, "Manage &People", "Add/Edit/Delete people from the system", kind=wx.ITEM_CHECK)
        
        toolmenu = wx.Menu()
        test_camera = toolmenu.Append(wx.ID_ANY, "Test &Camera", "Test the camera")

        #self.Bind(wx.EVT_MENU, self.onNew, newItem)
        self.Bind(wx.EVT_MENU, self.onNewSample, newItem)
        self.Bind(wx.EVT_MENU, self.onAbout, aboutItem)
        self.Bind(wx.EVT_MENU, self.onQuit, exitItem)

        self.Bind(wx.EVT_MENU, self.onSampleMenu, samplesItem)
        self.Bind(wx.EVT_MENU, self.onCaptureTestButton, test_camera)
        self.Bind(wx.EVT_MENU, self.onMoviesTab, manage_movie)
        self.Bind(wx.EVT_MENU, self.onPersonTab, manage_people)
        
        self.Bind(wx.EVT_CLOSE, self.OnClose)
        return {
            "&File": filemenu,
            "&View": viewmenu,
            "&Tools": toolmenu
        }

    def OnClose(self, evt):
        self.mainControllerQuit()
        self.Destroy()

    def setIcon(self):
        icon = wx.Icon()
        icon.CopyFromBitmap(wx.Bitmap("./src/icon.ico", wx.BITMAP_TYPE_ANY))
        self.SetIcon(icon)

    def config(self):        
        config = {
            "capture_device": "0"
        }        
        self.config = config
    
    def __init__(self, title):
        #I'm avoiding wx.RESIZE_BORDER because I use i3wm stack window manager for my own system.
        #custom_style= wx.MINIMIZE_BOX | wx.MAXIMIZE_BOX |wx.FRAME_FLOAT_ON_PARENT| wx.SYSTEM_MENU | wx.CAPTION | wx.CLOSE_BOX
        custom_style= wx.MINIMIZE_BOX | wx.MAXIMIZE_BOX | wx.SYSTEM_MENU | wx.CAPTION | wx.CLOSE_BOX |  wx.RESIZE_BORDER
        wx.Frame.__init__(self, None, title=title,
                          size=(1024,720),
                          style=custom_style
        )
        self.setIcon()

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

        self.panel_notebook.SetMinSize((20,320))
        self.panel_notebook.SetForegroundColour("gray")
        self.txtConsole.SetMinSize((90, 23))

        self.do_layout()
        self.print("Affective M.E.M: %s"%(__MEM_VERSION__))
        self.print("Operating System: %s %s"% (platform.system(), platform.release()) )
        self.print("SYSTEM READY")
        #ConsoleUI = self
        MainControllerObject.__init__(self)
        

    def print(self, *args, **kwargs):        
        self.txtConsole.AppendText(*args)
        self.txtConsole.AppendText("\n")
        

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
frame = ControlPanelFrame("Affective Movie Evaluation Machine -- ControlPanel")
app.MainLoop()