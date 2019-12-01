import wx
class FormObj:
    pass

from src.wx.timeseries import SerialPlotter
from src.wx.record import SearchBoxMovie


from src.wx.player import VideoPlayerPanel

import pandas as pd
import numpy as np
#class SamplePreviewPanel(wx.Panel):
#    pass

class AnalyseMovieTabPanel(wx.Panel):    
    selectedMovie=None
    recordMode=False
    last_sample_id=None
    mean_mag=[]
    mean_aud_score = 0
    #timer = None    
    testStatus=False
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
        self.movie_player_ctrl = VideoPlayerPanel(self)
        

        #print(controllers.personController.getAll())
        #self.create_preview_panel(self.video_preview)        
        self.serial_plotter = SerialPlotter(self, ylim=(0,10))
        self.serial_plotter.updateCallback = self.plotterUpdate
        self.serial_plotter.xvals = []
        self.mean_mag = [(1,1),(2,3),(3,4),(4,5),(6,1)]
        self.serial_plotter.windowSize = 10
        #self.serial_plotter.vals = self.top_parent.edaFrames
        self.create_form(self.form)
        self.do_layout()
        self.do_bind()

    def create_form(self, form):        
        form.lblMovieID = wx.StaticText(self, wx.ID_ANY, "Movie")
        form.txtMovieID = wx.TextCtrl(self, wx.ID_ANY, "Not Selected", style=wx.TE_READONLY) 
        form.btnFindMovie = wx.Button(self, wx.ID_ANY, "Find Movie")    
        form.lblReport = wx.StaticText(self, wx.ID_ANY, "Report")
        form.btnSummary = wx.Button(self, wx.ID_ANY, "Summary")  
        form.btnSamples = wx.Button(self, wx.ID_ANY, "Samples")
        form.btnCalculcate = wx.Button(self, wx.ID_ANY, "Calculate Scores")
        #form.btnRecord = wx.Button(self, wx.ID_ANY, "Record")
        #form.btnTest = wx.Button(self, wx.ID_ANY, "Test")

    def create_preview_panel(self, video_preview):
        video_preview.videoFrame = wx.Panel(self, -1, size=(320,200))
        video_preview.timeslider = wx.Slider(self, -1, 0, 0, 1000)
        video_preview.timeslider.SetRange(0, 1000)
        #video_preview.Add(self.movie_player_ctrl, 1, wx.EXPAND)
        #self.top_parent.addCameraFrame(video_preview.videoFrame, "test", size=(320,200))


    def do_layout(self):
        form = self.form
        main_sizer = wx.BoxSizer(wx.HORIZONTAL)
        form_grid = wx.GridSizer(8, 2, 0, 0)
        vid_container = wx.BoxSizer(wx.VERTICAL)
        ts_container = wx.BoxSizer(wx.VERTICAL)

        form_grid.Add(form.lblMovieID)
        form_grid.Add(form.txtMovieID)
        form_grid.Add((0,0))
        form_grid.Add(form.btnFindMovie)
        #form_grid.Add(form.btnFindMovie)
        #form_grid.Add(form.btnRecord)
        form_grid.Add((0,0), 0,0,0)
        form_grid.Add((0,0), 0,0,0)
        #form_grid.Add(form.btnTest)
        form_grid.Add(form.lblReport)
        form_grid.Add(form.btnSummary)
        form_grid.Add(form.btnSamples)
        form_grid.Add((0,0), 0,0,0)
        form_grid.Add(form.btnCalculcate)


        ts_container.Add(self.serial_plotter)

        main_sizer.Add(form_grid, 0.3, wx.ALIGN_LEFT)
        #main_sizer.Add(vid_container)
        main_sizer.Add(self.movie_player_ctrl, 1, wx.EXPAND, 0)
        main_sizer.Add(ts_container, 1, wx.EXPAND)
        self.SetSizer(main_sizer)
        self.Layout()

    def loadTimeSeriesData(self, movie_id):
        samples = self.controllers.sampleController.getSamplesByMovie(movie_id)
        #samples = np.array(sample)
        total_aud_score = []
        for sample in samples:
            total_aud_score.append(sample["score_5"])

        #total_aud_score = np.array(total_aud_score)
        mean_aud_score = np.mean(total_aud_score)

    def searchMovie(self, event):
        movies = self.controllers.movieController.listMovies()
        movieDialog = SearchBoxMovie(self.parent, movies)
        result = movieDialog.ShowModal()
        if result == wx.ID_OK:
            item = movieDialog.getSelectedItem()    
            self.form.txtMovieID.SetValue(item["name"])
            self.selectedMovie = item
            self.movie_player_ctrl.setVideo("./movies/"+item["filename"])
            #df = pd.read_csv()
            self.loadTimeSeriesData(item["id"])
        movieDialog.Destroy()

            
    def do_bind(self):
        self.form.btnFindMovie.Bind(wx.EVT_BUTTON, self.searchMovie)
        #self.form.btnTest.Bind(wx.EVT_BUTTON, self.toggleTest)
        #self.Bind(wx.EVT_TIMER, self.onUpdate)

    def startRecord(self):
        self.top_parent.print("Starting record")

    def stopRecord(self):
        self.top_parent.print("Stopping record")


    def onRecordFrame(self, frame):
        pass

    def onRecordEnd(self, filename):
        pass 
        

    def toggleTest(self,event):
        #gsrEnabled = self.form.cbGSR.GetValue()
        gsrEnabled = False
        if not self.testStatus:
            self.serial_plotter.clear()
            #if gsrEnabled:
            #    self.top_parent.start_gsr()  
            #self.top_parent.start_camera() 
            self.startRecord()
        else:
            #if gsrEnabled:
            #    self.top_parent.stop_gsr()
            #self.top_parent.stop_camera()
            self.stopRecord()
        self.testStatus = not self.testStatus


    def plotterUpdate(self, val, ts):
        if len(ts.xvals) != len(self.mean_mag):
            ts.xvals = [n[0] for n in self.mean_mag]
            ts.vals = [n[1] for n in self.mean_mag]
        #eda = self.top_parent.edaFrames
        #eda = self.mean_mag
        #print(eda)
        #if len(eda) > 0:
        #    v = eda[len(eda)-1][1]
        #    t = eda[len(eda)-1][0]
        #    val.append(v)
        #    ts.xvals.append(t)
