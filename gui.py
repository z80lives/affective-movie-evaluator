#!/usr/bin/env python
import wx

#import builtins as __builtin__
#define



class CPanelEventHandlers:
    def onQuit(self, event):
        self.Close(True)

    def onAbout(self, event):
        msg = "Created by Ibrahim & Faith for FYP\n\t HELP School of ICT \n\t  2019"
        dlg = wx.MessageDialog(self, msg, "Affective Movie Evaluator", wx.OK)
        dlg.ShowModal()
        dlg.Destroy()
        #print()

    def newRecord(self, event):
        print("Creating a new record")

    def onNew(self, event):        
        recordTab = RecordTabPanel(self.panel_notebook)
        self.panel_notebook.AddPage(recordTab, "Record Screening")
        #self.do_layout()
        self.Layout()
        
   #     with wx.FileDialog(self, "Open a movie file", wildcard="mp4 files (*.mp5)|*.mp4",
   #                    style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST) as fileDialog:

   #         if fileDialog.ShowModal() == wx.ID_CANCEL:
  #              return     # the user changed their mind

            # Proceed loading the file chosen by the user
  #          pathname = fileDialog.GetPath()
  #          print("File %s found!"% (pathname))
            
            #try:
            #    with open(pathname, 'r') as file:
            #        self.doLoadDataOrWhatever(file)
            #except IOError:
            #    wx.LogError("Cannot open file '%s'." % newfile)
import random
class TestTabPanel(wx.Panel):
    #----------------------------------------------------------------------
    def __init__(self, parent):
        """"""
        wx.Panel.__init__(self, parent=parent)

        colors = ["red", "blue", "gray", "yellow", "green"]
        self.SetBackgroundColour(random.choice(colors))

        btn = wx.Button(self, label="Press Me")
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(btn, 0, wx.ALL, 10)
        self.SetSizer(sizer)

class FormObj:
    pass
        
class RecordTabPanel(wx.Panel):
    
    def __init__(self, parent):
        super().__init__(parent, wx.ID_ANY)
        self.form = FormObj()
        #formObj.txtPerson
        self.form.txtPerson = wx.TextCtrl(self, wx.ID_ANY, "")
        self.form.txtMovieFile = wx.TextCtrl(self, wx.ID_ANY, "", style=wx.TE_READONLY)
        self.form.btnPickFile = wx.Button(self, wx.ID_ANY, "Open")
        self.form.txtMovieName = wx.TextCtrl(self, wx.ID_ANY, "")
        self.form.txtYear = wx.TextCtrl(self, wx.ID_ANY, "")
        self.form.txtGenre = wx.TextCtrl(self, wx.ID_ANY, "")
        self.form.txtTag = wx.TextCtrl(self, wx.ID_ANY, "")
        self.form.checkbox_1 = wx.CheckBox(self, wx.ID_ANY, "")
        
        self.do_layout()        

    def do_layout(self):
        tab_context_sizer = wx.BoxSizer(wx.VERTICAL)
        form_gridsizer = wx.GridSizer(7, 2, 0, 0)        

        fileOpenSizer = wx.BoxSizer(wx.HORIZONTAL)        
        lblPerson = wx.StaticText(self, wx.ID_ANY, "Person Name")
        
        form_gridsizer.Add(lblPerson, 0, 0, 0)
        form_gridsizer.Add(self.form.txtPerson, 0, wx.ALL | wx.EXPAND, 2)

        lblFilename = wx.StaticText(self, wx.ID_ANY, "FileName")
        form_gridsizer.Add(lblFilename, 0, 0, 0)
        fileOpenSizer.Add(self.form.txtMovieFile, 2, 0, 0)
        fileOpenSizer.Add(self.form.btnPickFile, 1, 0, 0)
        form_gridsizer.Add(fileOpenSizer, 1, wx.EXPAND, 0)

        lblMovieName = wx.StaticText(self, wx.ID_ANY, "Movie Name")
        form_gridsizer.Add(lblMovieName, 0, 0, 0)
        form_gridsizer.Add(self.form.txtMovieName, 0, wx.ALL | wx.EXPAND, 2)
        lblYear = wx.StaticText(self, wx.ID_ANY, "Year")
        form_gridsizer.Add(lblYear, 0, 0, 0)
        form_gridsizer.Add(self.form.txtYear, 0, wx.ALL | wx.EXPAND, 2)
        lblGenre = wx.StaticText(self, wx.ID_ANY, "Genre")
        form_gridsizer.Add(lblGenre, 0, 0, 0)
        form_gridsizer.Add(self.form.txtGenre, 0, wx.ALL | wx.EXPAND, 2)
        lblTags = wx.StaticText(self, wx.ID_ANY, "Tags")
        form_gridsizer.Add(lblTags, 0, 0, 0)
        form_gridsizer.Add(self.form.txtTag, 0, wx.ALL | wx.EXPAND, 2)
        lblPreview = wx.StaticText(self, wx.ID_ANY, "Preview \n(Not Recommended)")
        form_gridsizer.Add(lblPreview, 0, 0, 0)
        form_gridsizer.Add(self.form.checkbox_1, 0, 0, 0)

        tab_context_sizer.Add(form_gridsizer, 0, 0, 0)
        
        self.SetSizer(tab_context_sizer)        
        self.Layout()        
        

class ControlPanelFrame(wx.Frame, CPanelEventHandlers):    
    def createMenus(self):
        filemenu = wx.Menu()
        newItem = filemenu.Append(wx.ID_NEW, "&New Record", "Create a new Recording")        
        aboutItem = filemenu.Append(wx.ID_ABOUT, "&About", "Application Information")        
        filemenu.AppendSeparator()
        exitItem = filemenu.Append(wx.ID_EXIT, "E&xit", "Quit Program")

        self.Bind(wx.EVT_MENU, self.onNew, newItem)
        self.Bind(wx.EVT_MENU, self.onAbout, aboutItem)
        self.Bind(wx.EVT_MENU, self.onQuit, exitItem)
        return {
            "&File": filemenu
        }

    
    def __init__(self, title):
        #I'm avoiding wx.RESIZE_BORDER because I use i3wm stack window manager for my own system.
        custom_style=wx.MINIMIZE_BOX | wx.MAXIMIZE_BOX |wx.FRAME_FLOAT_ON_PARENT| wx.SYSTEM_MENU | wx.CAPTION | wx.CLOSE_BOX
        
        wx.Frame.__init__(self, None, title=title,
                          size=(1024,720),
                          style=custom_style
        )
        #self.control = wx.TextCtrl(self, style=wx.TE_MULTILINE)
        self.panel_notebook = wx.Notebook(self, wx.ID_ANY)
        #self.text_area = wx.TextCtrl(self, wx.ID_ANY, "")
        
        self.CreateStatusBar()

        menubar = wx.MenuBar()
        menus = self.createMenus()
        for k in menus:
            menubar.Append(menus[k], k)
        
        self.SetMenuBar(menubar)        
        self.Show(True)

        self.do_layout()

    def do_layout(self):
        self.context_sizer = wx.BoxSizer(wx.VERTICAL)
        self.context_sizer.Add(self.panel_notebook, 0, wx.ALL | wx.EXPAND, 1)
        #self.context_sizer.Add(self.text_area, 0, wx.ALL, 0)

        #recordTab = RecordTabPanel(self.panel_notebook)
        #self.panel_notebook.AddPage(recordTab, "Record Screening")
        
        self.SetSizer(self.context_sizer)
        self.Layout()

app = wx.App(False)
frame = ControlPanelFrame("Affective Movie Evaluator ControlPanel")
app.MainLoop()


