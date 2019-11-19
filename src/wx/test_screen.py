import wx
class FormObj:
    pass

from src.wx.timeseries import SerialPlotter
from src.wx.record import SearchBoxMovie
 
class TestScreeningTab(wx.Panel):    
    selectedMovie=None
    recordMode=False
    last_sample_id=None
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
        form.lblMovieID = wx.StaticText(self, wx.ID_ANY, "Movie")
        form.txtMovieID = wx.TextCtrl(self, wx.ID_ANY, "Not Selected", style=wx.TE_READONLY) 
        form.btnFindMovie = wx.Button(self, wx.ID_ANY, "Find Movie")                
        #form.btnRecord = wx.Button(self, wx.ID_ANY, "Record")
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

        form_grid.Add(form.lblMovieID)
        form_grid.Add(form.txtMovieID)
        form_grid.Add((0,0))
        form_grid.Add(form.btnFindMovie)

        #form_grid.Add(form.btnRecord)

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
        self.form.btnFindMovie.Bind(wx.EVT_BUTTON, self.searchMovie)
        self.form.btnTest.Bind(wx.EVT_BUTTON, self.toggleTest)
        #self.Bind(wx.EVT_TIMER, self.onUpdate)

    def startRecord(self):
        self.top_parent.print("Starting record")

    def startRecord(self):
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
            self.top_parent.start_camera() 
            self.startRecord()
        else:
            #if gsrEnabled:
            #    self.top_parent.stop_gsr()
            self.top_parent.stop_camera()
            self.stopRecord()
        self.testStatus = not self.testStatus

    def gsrUpdate(self, val, ts):
        eda = self.top_parent.edaFrames
        if len(eda) > 0:
            v = eda[len(eda)-1][1]
            t = eda[len(eda)-1][0]
            val.append(v)
            ts.xvals.append(t)
