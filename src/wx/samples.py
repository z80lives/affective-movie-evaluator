import wx
import wx.grid as gridlib

class SampleTabFrame(wx.Frame):
    def __init__(self, controllers):
        """Constructor"""
        wx.Frame.__init__(self, wx.GetApp().TopWindow, title="Sample Window")
        #wx.Frame.__init__(self, parent=None, title="A Simple Grid")
        panel = wx.Panel(self)
        self.controllers = controllers
 
        myGrid = gridlib.Grid(panel)
        self.setData(myGrid)
        myGrid.ShowScrollbars(wx.SHOW_SB_DEFAULT,wx.SHOW_SB_DEFAULT)
        
        self.setIcon()
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(myGrid, 1, wx.EXPAND)   
             
        panel.SetSizerAndFit(sizer)
        #panel.SetSizer(sizer)
        panel.Layout()
        
        self.Fit()

    def setData(self, grid):
        #for col in )
        titles= ["Sample ID", "Person ID", "Movie ID", "Person Name", "Movie Name", "Given Rating"]
        sampleController = self.controllers.sampleController
        #sampleController.init()
        movieController = self.controllers.movieController
        movieController.init()

        sample_list = sampleController.list_all()
        grid.CreateGrid(len(sample_list)+1, 8)
        grid.DisableCellEditControl()

        for i, title in enumerate(titles):
            grid.SetCellValue(0, i, title)
            grid.SetCellFont(0, i, wx.Font().Bold())

        for row_index, sample_id in enumerate(sample_list):
            grid.SetCellValue(row_index+1, 0, sample_id)   
            person_id = sampleController.data[sample_id]["subject_name"]   
            movie_id = sampleController.data[sample_id]["movie_id"]
            score = None
            try:
                score = sampleController.data[sample_id]["score_5"]            
            except KeyError:
                pass
            movie = movieController.getMovieObjById(movie_id)
            person = self.controllers.personController.getPerson(person_id)
                        
            grid.SetCellValue(row_index+1, 1, str(movie_id))
            grid.SetCellValue(row_index+1, 2, str(person_id))
            grid.SetCellValue(row_index+1, 3, person["name"])
            grid.SetCellValue(row_index+1, 4, movie.name)
            grid.SetCellValue(row_index+1, 5, str(score))

        for i in range(7):
            grid.AutoSizeColumn(i)      
 
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