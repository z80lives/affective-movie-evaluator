import wx
from src.wx.timeseries import SerialPlotter
        
class FormObj:
    pass

import cv2
import datetime
    
class CameraCaptureFrame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, wx.GetApp().TopWindow, title="Capture Test Window")
        self.gui = wx.GetApp().TopWindow
        self.gui.start_camera()
        self.gui.addCameraFrame(self, "test")
        width, height = self.gui.camera.getSize()
        self.SetSize((width, height))

        #self.bmp = self.gui.cameraBuffer

        #self.timer = wx.Timer(self)
        #self.timer.Start(1000./15)

        self.Bind(wx.EVT_CLOSE, self.OnClose)
        self.Layout()

    def OnClose(self, evt):
        self.gui.removeCameraFrame("test")        
        self.gui.stop_camera()
        self.Destroy()

class SearchBox(wx.Dialog):
    def __init__(self, parent, title):
        super(SearchBox, self).__init__(parent, title = title)
        self.createUI()        
        self.doLayout()


    def createUI(self):
        self.panel = wx.Panel(self)
        #searchBox = wx.TextCtrl(panel, wx.ID_ANY, "SEARCH")
        self.searchBox = wx.SearchCtrl(self.panel, wx.ID_ANY, value="")
        self.itemList = wx.ListBox(self.panel, wx.ID_ANY)
        self.btnSelect = wx.Button(self.panel, wx.ID_OK, label="C&onfirm")
        self.btnCancel = wx.Button(self.panel, wx.ID_CANCEL, label="Canc&el")
        #personList = wx.TextCtrl(panel, size = (-1,100),style = wx.TE_MULTILINE)
        
    def doLayout(self):
        panel = self.panel
        searchBox = self.searchBox
        personList = self.itemList

        body_sizer = wx.BoxSizer(wx.VERTICAL)     
        hbox1 = wx.BoxSizer(wx.HORIZONTAL) 
        hbox2 = wx.BoxSizer(wx.HORIZONTAL) 

        hbox3 = wx.BoxSizer(wx.HORIZONTAL)
        hbox3_vbox = wx.GridSizer(0, 3, 0, 0)

        hbox1.Add(searchBox,  proportion = 1, flag = wx.ALIGN_CENTRE)
        hbox2.Add(personList, proportion = 1, flag = wx.ALIGN_CENTER_HORIZONTAL |  wx.EXPAND, border = 1)

        hbox3_vbox.Add(self.btnCancel)
        hbox3_vbox.Add((0,0), proportion=0.5) #empty cell for grid
        hbox3_vbox.Add(self.btnSelect,  flag = wx.ALIGN_RIGHT)        
        hbox3.Add(hbox3_vbox)

        body_sizer.Add(hbox1, flag = wx.ALIGN_CENTRE)
        body_sizer.Add(hbox2, proportion = 1, flag = wx.EXPAND|wx.ALIGN_CENTRE)
        body_sizer.Add(hbox3, flag = wx.EXPAND|wx.ALIGN_CENTRE)
        panel.SetSizer(body_sizer)
        self.Layout()

    def OnClose(self):
        self.Destroy()


class SearchBoxPerson(SearchBox):
    person_data =[]
    def __init__(self, parent, db_person_list):
        super(SearchBoxPerson, self).__init__(parent, title = "Search Person")
        self.db_person_list = db_person_list
        self.populateList()

    def populateList(self):
        self.itemList.Clear()
        self.person_data = []
        for person in self.db_person_list:                     
            self.itemList.Append(person["name"])
            self.person_data.append(person)
            

    def getSelectedItem(self):
        idx = self.itemList.GetSelection()
        return self.person_data[idx]
    
class SearchBoxMovie(SearchBox):
    movie_data =[]
    def __init__(self, parent, db_movie_list):
        super(SearchBoxMovie, self).__init__(parent, title = "Search Person")
        self.db_movie_list = db_movie_list
        self.populateList()

    def populateList(self):
        self.itemList.Clear()
        self.movie_data = []
        for movie in self.db_movie_list:                     
            self.itemList.Append(movie["name"])
            self.movie_data.append(movie)
            

    def getSelectedItem(self):
        idx = self.itemList.GetSelection()
        return self.movie_data[idx]
    
class RecordTabPanel(wx.Panel):    
    selectedPerson=None
    selectedMovie=None
    gsrTest=False
    recordMode=False
    last_sample_id=None
    #timer = None
    vidWriter=None
    vidGSRWriter=None
    def __init__(self, parent, event_handler, controllers):
        super().__init__(parent, wx.ID_ANY)
        self.top_parent = wx.GetApp().TopWindow
        self.form = FormObj()
        self.video_preview = FormObj()
        self.gsr_preview = FormObj()
        self.controllers = controllers        

        #self.timer = wx.Timer(self)

        self.event_handler =  event_handler
        self.parent = parent

        #print(controllers.personController.getAll())
        self.create_preview_panel(self.video_preview)        
        self.serial_plotter = SerialPlotter(self)
        self.serial_plotter.updateCallback = self.gsrUpdate
        self.serial_plotter.xvals = []
        self.serial_plotter.windowSize = 10
        #self.serial_plotter.vals = self.top_parent.edaFrames
        self.create_form(self.form)
        self.do_layout()
        self.do_bind()

    def create_form(self, form):
        form.lblPersonID = wx.StaticText(self, wx.ID_ANY, "Person")
        form.txtPersonID = wx.TextCtrl(self, wx.ID_ANY, "Not Selected", style=wx.TE_READONLY)
        
        #form.txtPersonID = wx.ComboBox(self, wx.ID_ANY, choices=[])
        form.btnFindPerson = wx.Button(self, wx.ID_ANY, "Find Person")
        form.lblMovieID = wx.StaticText(self, wx.ID_ANY, "Movie")
        form.txtMovieID = wx.TextCtrl(self, wx.ID_ANY, "Not Selected", style=wx.TE_READONLY) 
        form.btnFindMovie = wx.Button(self, wx.ID_ANY, "Find Movie")
        form.lblGSR = wx.StaticText(self, wx.ID_ANY, "GSR/EDA Sensor")
        form.cbGSR = wx.CheckBox(self, wx.ID_ANY, "")        
        form.btnRecord = wx.Button(self, wx.ID_ANY, "Record")
        form.btnTest = wx.Button(self, wx.ID_ANY, "Test")

    def create_preview_panel(self, video_preview):
        video_preview.videoFrame = wx.Panel(self, -1, size=(320,200))
        video_preview.timeslider = wx.Slider(self, -1, 0, 0, 1000)
        video_preview.timeslider.SetRange(0, 1000)
        self.top_parent.addCameraFrame(video_preview.videoFrame, "test", size=(320,200))


    def do_layout(self):
        form = self.form
        main_sizer = wx.BoxSizer(wx.HORIZONTAL)
        form_grid = wx.GridSizer(8, 2, 0, 0)
        vid_container = wx.BoxSizer(wx.VERTICAL)
        ts_container = wx.BoxSizer(wx.VERTICAL)

        form_grid.Add(form.lblPersonID, 0,0,0)
        form_grid.Add(form.txtPersonID, 0,0,0)
        form_grid.Add((0,0))
        form_grid.Add(form.btnFindPerson)

        form_grid.Add(form.lblMovieID)
        form_grid.Add(form.txtMovieID)
        form_grid.Add((0,0))
        form_grid.Add(form.btnFindMovie)

        form_grid.Add(form.lblGSR)
        form_grid.Add(form.cbGSR)
        form_grid.Add((0,0), 0,0,0)
        form_grid.Add(form.btnRecord)

        form_grid.Add((0,0), 0,0,0)
        form_grid.Add(form.btnTest)

        vid = self.video_preview
        vid_container.Add(vid.videoFrame)
        vid.videoFrame.SetSize((320,200))
        vid_container.Add(vid.timeslider)

        ts_container.Add(self.serial_plotter)

        main_sizer.Add(form_grid)
        main_sizer.Add(vid_container)
        main_sizer.Add(ts_container)
        self.SetSizer(main_sizer)
        self.Layout()

    def searchPerson(self, event):
        persons = self.controllers.personController.getAll()
        searchDialog = SearchBoxPerson(self.parent, persons)
        result = searchDialog.ShowModal()
        if result == wx.ID_OK:
            item = searchDialog.getSelectedItem()            
            self.form.txtPersonID.SetValue(item["name"])
            self.selectedPerson = item
        searchDialog.Destroy()

    def searchMovie(self, event):
        movies = self.controllers.movieController.listMovies()
        movieDialog = SearchBoxMovie(self.parent, movies)
        result = movieDialog.ShowModal()
        if result == wx.ID_OK:
            item = movieDialog.getSelectedItem()            
            self.form.txtMovieID.SetValue(item["name"])
            self.selectedMovie = item
        movieDialog.Destroy()

    def do_bind(self):
        self.form.btnFindPerson.Bind(wx.EVT_BUTTON, self.searchPerson)
        self.form.btnFindMovie.Bind(wx.EVT_BUTTON, self.searchMovie)
        self.form.btnRecord.Bind(wx.EVT_BUTTON, self.startRecord)
        self.form.btnTest.Bind(wx.EVT_BUTTON, self.toggleTest)
        #self.Bind(wx.EVT_TIMER, self.onUpdate)

    def startRecord(self, evt):
        gsrEnabled = self.form.cbGSR.GetValue()
        if self.selectedPerson is None:
            self.top_parent.print("Please select a person")
            return 

        if self.selectedMovie is None:
            self.top_parent.print("Please select a movie")
            return

        if not self.recordMode:
            self.recordMode = True
            self.serial_plotter.clear()
            sys = self.controllers.recordSystem
            mov = self.controllers.movieController
            mplayer = self.controllers.mediaplayer
            file_name = self.selectedMovie["filename"]
            metadata = mov.getMovieByFile(file_name)
            file_name = mov.get_dir() + file_name
            self.top_parent.print("file_name %s"% file_name)
            player = mplayer(file_name)
            filename = sys.createSampleDir()
            samplemeta = { "movie_id": "%s"%(metadata["id"]),
                           "subject_name": self.selectedPerson["id"],
                           "datetime": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                         }

            #self.timer = wx.Timer(self)
            #self.timer.Start(1000./15)
            #self.controllers.gsr.openPort()
            #self.Bind(wx.EVT_TIMER, self.readGSR)            
            if gsrEnabled:
                self.top_parent.start_gsr() 

            self.top_parent.start_camera()

            sys.saveMetaData(filename, samplemeta)

            if gsrEnabled:
                self.vidGSRWriter = sys.getWriter(filename+"/gsrsample")
            self.form.cbGSR.Disable()

            self.vidWriter = sys.getWriter(filename+"/sample")
            self.top_parent.callbacks["onGSR"] = self.onGSRUpdate

            #sys.start_recording("sample", player, False, filename)
            #sys.onStopRecording()
            #self.top_parent.setRecordStartEvent(self.onRecordStart)
            self.top_parent.setRecordFrameEvent(self.onRecordFrame)
            #self.top_parent.setRecordEndEvent(self.onRecordEnd)
            self.last_sample_id = filename
            mplayer.onExitCallback = self.onRecordEnd

            #self.top_parent.print("Record complete")
            self.top_parent.print("Sample id= %s"%(filename))
            
            #self.timer.stop()

    def onRecordFrame(self, frame):
        #print("Recording frame")
        self.vidWriter.write(self.top_parent.camera.imgBuffer)
    
    def onGSRUpdate(self, gsrval):
        self.vidGSRWriter.write(self.top_parent.camera.imgBuffer)

    def onRecordEnd(self, filename):
        gsrEnabled = self.form.cbGSR.GetValue()
        self.form.cbGSR.Enable()
        if gsrEnabled:
            self.top_parent.stop_gsr()
        self.top_parent.stop_camera()
        edaFrames = self.top_parent.edaFrames

        if gsrEnabled:
            self.top_parent.callbacks["onGSR"] = None
            self.controllers.recordSystem.saveWriter(self.vidGSRWriter)
        self.controllers.recordSystem.saveWriter(self.vidWriter)        
        self.top_parent.saveEDAFile("./data/"+self.last_sample_id+"/eda.csv")
        self.recordMode = False
        self.top_parent.print("End of record session: %s"% self.last_sample_id)
        sid = self.last_sample_id
        

    def toggleTest(self,event):
        gsrEnabled = self.form.cbGSR.GetValue()
        if not self.gsrTest:
            self.serial_plotter.clear()
            if gsrEnabled:
                self.top_parent.start_gsr()  
            self.top_parent.start_camera() 
        else:
            if gsrEnabled:
                self.top_parent.stop_gsr()
            self.top_parent.stop_camera()
        self.gsrTest = not self.gsrTest

    def gsrUpdate(self, val, ts):
        eda = self.top_parent.edaFrames
        if len(eda) > 0:
            v = eda[len(eda)-1][1]
            t = eda[len(eda)-1][0]
            val.append(v)
            ts.xvals.append(t)
            #if len(ts.)
    #def onUpdate(self, evt):        
    #    self.serial_plotter.update(evt)

    def readGSR(self, event):
        print("Recording")
        #self.top_parent.print("Record complete")
        #self.top_parent.print(self.controllers.gsr.readVal())
