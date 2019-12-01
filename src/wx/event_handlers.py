import wx

from src.playback import RecordSystem, VLCPlayer
from src.utils import SampleLoader, SampleController, MovieController, PersonController
from src.wx.record import RecordTabPanel, CameraCaptureFrame
from src.wx.analyse_movie import AnalyseMovieTabPanel
from src.wx.samples import SampleTabPanel, SampleTabFrame
#from src.wx.analyse import AnalyseMovieTab
from src.wx.movies import MoviesPanel
from src.wx.person import PersonPanel
from src.gsr import GSRSensor

def analyse_func(video_dir, video_file_name, fer,head,body,preview,_print):
    if fer:            
        _print("Analysing facial keypoints...")
        from FER.ferAnalysis import FaceSystem
        
        system = FaceSystem()
        system.analyse(video_file_name, preview)

    if head:
        from src.headpose import HeadPoseEstimator
        sys = HeadPoseEstimator()
        #sys._print = _print
        _print("Analysing body keypoints...")
        loader = SampleLoader(video_dir)
        sys.analyse(loader.getVideoFile(), loader.getDir()+"head_points.npy", preview)
            
    if body:
        _print("Initializing pose system")
        from src.openpose import PoseSystem
        sys = PoseSystem()
        
        _print("Analysing body keypoints ")
        loader = SampleLoader(kwargs["filename"])
        sys.analyse(loader.getVideoFile(), loader.getDir()+"body_points.npy", preview)


        

class CPanelEventHandlers:
    recordTab = None
    moviesTab = None
    personTab = None
    analyse_process=None
    def onQuit(self, event):
        self.Close(True)


    def onAbout(self, event):
        msg = "Created by Ibrahim & Faith for FYP\n\t HELP School of ICT \n\t  2019"
        dlg = wx.MessageDialog(self, msg, "Affective Movie Evaluator", wx.OK)
        dlg.ShowModal()
        dlg.Destroy()
        #print()

    def newRecord(self, event):
        self.print("Creating a new record")

    def onNewSample(self, event):
        class EmptyClass: pass
        controllers = EmptyClass()
        controllers.personController = PersonController()
        controllers.movieController = MovieController()
        controllers.sampleController = SampleController()
        controllers.recordSystem = RecordSystem()
        controllers.mediaplayer = VLCPlayer
        #controllers.gsr = GSRSensor()
        
        recordTab = RecordTabPanel(self.panel_notebook, self, controllers)
        idx = self.panel_notebook.AddPage(recordTab, "Record Screening")
        self.Layout()

    def onMovieAnalyse(self, event):
        class EmptyClass: pass
        controllers = EmptyClass()
        controllers.movieController = MovieController()
        controllers.sampleController = SampleController()
        controllers.mediaplayer = VLCPlayer

        controllers.sampleController.read_dirs()

        screeningTab = AnalyseMovieTabPanel(self.panel_notebook, self, controllers)
        idx = self.panel_notebook.AddPage(screeningTab, "Screening Tab")
        self.Layout()

    def onNewScreening(self, event):
        pass

    def onNew(self, event):
        #file selector dialog
        with wx.FileDialog(self, "Open a movie file", wildcard="mp4 files (*.mp5)|*.mp4",
                           style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST) as fileDialog:
            if fileDialog.ShowModal() == wx.ID_CANCEL:
                return     
            pathname = fileDialog.GetPath()
            self.print("File %s found!"% (pathname))


        sys = RecordSystem()
        msys = MovieController()
        msys.read_files()

        mdata = msys.getMovieByFile(pathname)
            
        #try:
        #    with open(pathname, 'r') as file:
        #        self.doLoadDataOrWhatever(file)
        #except IOError:
        #    wx.LogError("Cannot open file '%s'." % newfile)

        #open the tab later
        recordTab = RecordTabPanel(self.panel_notebook, self)
        idx = self.panel_notebook.AddPage(recordTab, "Record Screening")

        #auto fill text fields
        recordTab.form.txtMovieFile.SetValue(pathname)
        inp_map = {
            "name": recordTab.form.txtMovieName,
            "year": recordTab.form.txtYear,
            "genre": recordTab.form.txtGenre,
            "tags": recordTab.form.txtTag
        }
        self.recordTab = recordTab
        for k in inp_map:
            try:
                inpField = inp_map[k]
                inpField.SetValue(mdata[k])
            except KeyError: #ignore if key doesnt exist
                continue

        #self.do_layout()
        self.Layout()

    def onMoviesTab(self, event):
        if self.moviesTab is None:
            tab_title = "Movies Panel"
            movieController = MovieController()
            moviesTab = MoviesPanel(self.panel_notebook, self, tab_title, movieController)
            idx = self.panel_notebook.AddPage(moviesTab, tab_title)
            self.moviesTab = moviesTab
        else:
            self.moviesTab.onCloseTab(event)

    def onPersonTab(self, event):
        if self.personTab is None:
            tab_title = "Person Panel"
            person_controller = PersonController()
            personTab = PersonPanel(self.panel_notebook, self, tab_title, person_controller)
            idx = self.panel_notebook.AddPage(personTab, tab_title)
            self.personTab = personTab
        else:
            self.personTab.onCloseTab(event)

    def onCloseTab(self, event):
        self.delPage("Record Screening")
        self.Layout()

    def onCloseAnalyserTab(self, event):
        self.onStopProcess(event)
        self.delPage("Analyse Sample")
        self.Layout()


    def onRecord(self, event, form):
        sys = RecordSystem()
        msys = MovieController()
        msys.read_files()

        person = form.txtPerson.GetValue()
        movie_path = form.txtMovieFile.GetValue()
        mdata = msys.getMovieByFile(movie_path)

        file_name = msys.get_dir() + msys.getMovieObjById(mdata['id']).filename
        data = {"movie_id": "%s"%(mdata["id"]),"subject_name": person}

        player = VLCPlayer(file_name)

        sys = RecordSystem()
        filename = sys.createSampleDir()
        sys.saveMetaData(filename, data)
        sys.start_recording("sample", player, False, filename)
        self.print("Record complete...")
        self.print("New sample created. sample_id= %s"%(filename))
        

    def onSampleMenu(self, event):
        if self.recordTab is not None:
            self.recordTab.Close()
        #print("Sample Menu")
        #sampleTab = SampleTabPanel(self.panel_notebook, self)
        #self.panel_notebook.AddPage(sampleTab, "Sample Records")
        class EmptyClass: pass
        controllers = EmptyClass()
        controllers.personController = PersonController()
        controllers.movieController = MovieController()
        controllers.sampleController = SampleController()
        sampleFrame = SampleTabFrame(controllers)
        sampleFrame.Show()
        self.Layout()

    def onCaptureTestButton(self, event):
        self.print("Camera Capture event started.")
        captureFrame = CameraCaptureFrame()
        captureFrame.Show()
        self.Layout()
        

    def onAnalyseMenu(self, event):
        with wx.FileDialog(self, "Open a sample file", wildcard="avi files (*.avi)|*.avi",
                           style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST) as fileDialog:
            if fileDialog.ShowModal() == wx.ID_CANCEL:
                return     
            pathname = fileDialog.GetPath()
            self.print("File %s found!"% (pathname))
            
        _sid = pathname[:pathname.rindex("/")]
        _sid = _sid[_sid.rindex("/")+1:]
                
        analyseTab = AnalyseMovieTabPanel(self.panel_notebook, self, _sid)
        self.panel_notebook.AddPage(analyseTab, "Analyse Sample")
        self.Layout()
        

    def onAnalyse(self, event, sid, form):        
        #import sys, time, threading
        from multiprocessing import Process
        fer = form.chkFER.GetValue()
        head = form.chkBEGR.GetValue()
        body = False
        preview = form.chkPreview.GetValue()
        video_file_name = "./data/"+sid+ "/test.avi"
        video_dir = "./data/"+sid+"/"

        if not preview:
            p = Process(name='process',
                        target=analyse_func,
                        args=(video_dir, video_file_name,
                              fer,head,body,preview,self.print,) )
            p.start()
        else:
            analyse_func(video_dir, video_file_name,
                          fer,head,body,preview,self.print)
        
        self.analyse_process = p

    def onStopProcess(self, event):
        if self.analyse_process is not None:
            self.analyse_process.terminate()


    def delPage(self, pageTitle):
        for index in range(self.panel_notebook.GetPageCount()):
            if self.panel_notebook.GetPageText(index) == pageTitle:
                self.panel_notebook.DeletePage(index)
                self.panel_notebook.SendSizeEvent()
                break

        
