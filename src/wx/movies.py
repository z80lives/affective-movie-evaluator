import wx
class FormObj:
    pass

from src.wx.player import VideoPlayerPanel

class MoviesPanel(wx.Panel):   
    movie_data=[]
    update_label = ["Save", "Update"]
    edit_mode=False
    selectedMovie=None
    def __init__(self, parent, event_handler, tab_title, movie_controller):
        super().__init__(parent, wx.ID_ANY)
        self.parent = parent
        self.tab_title = tab_title
        self.form = FormObj()
        self.event_handler = event_handler
        self.controller = movie_controller

        self.movie_list_ctrl = wx.ListCtrl(self, wx.ID_ANY, size=(3,1), style= wx.LC_REPORT | wx.LC_SINGLE_SEL |wx.BORDER_SUNKEN)

        self.movie_list_ctrl.InsertColumn(0,'Name')
        self.movie_list_ctrl.InsertColumn(1,'Genre')
        self.movie_list_ctrl.InsertColumn(2,'Year')
        self.movie_list_ctrl.InsertColumn(3,'Filename',width=125)
        
        self.movie_player_ctrl = VideoPlayerPanel(self)

        self.populateData()
        self.createForm(self.form)
        self.doLayouts()
        self.bindEvents()

    def populateData(self):
        movie_data = self.controller.listMovies()
        self.movie_data = movie_data
        self.updateMovieList()
    
    def updateMovieList(self):        
        #self.movie_list_ctrl.ClearAll()   
        for i, movie in enumerate(self.movie_data):
            self.movie_list_ctrl.InsertItem(i, movie["name"])
            self.movie_list_ctrl.SetItem(i, 1, "%s"%movie["genre"])
            self.movie_list_ctrl.SetItem(i, 2, "%s"%movie["year"])
            self.movie_list_ctrl.SetItem(i, 3, "%s"%movie["filename"])
            #self.movie_list_ctrl.InsertStringItem(i, movie["name"])
            #self.movie_list_ctrl.SetStringItem(i, 1, "01/19/2010")
            #self.movie_list_ctrl.SetStringItem(i, 2, "USA")
            #self.list_ctrl.SetItemData(i, i)

            #self.movie_list_ctrl.AppendColumn("Name", movie["name"])
            #self.movie_list_ctrl.InsertItem(i, "%s"%(movie["name"])) 

    def createForm(self, form):
        form.lblName = wx.StaticText(self, wx.ID_ANY, "Movie Name")
        form.movieName = wx.TextCtrl(self, wx.ID_ANY, "")
        form.lblGenre = wx.StaticText(self, wx.ID_ANY, "Genre")
        form.genre = wx.TextCtrl(self, wx.ID_ANY, "")
        form.lblTags = wx.StaticText(self, wx.ID_ANY, "Tags")
        form.tags = wx.TextCtrl(self, wx.ID_ANY, "")
        form.lblYear = wx.StaticText(self, wx.ID_ANY, "Year")
        form.year = wx.TextCtrl(self, wx.ID_ANY, "")
        form.btnSave = wx.Button(self, wx.ID_ANY, self.update_label[0])
        form.btnRemove = wx.Button(self, label="Delete")        
        form.btnRemove.Hide()

    def clearForm(self):
        self.form.movieName.SetValue("")
        self.form.genre.SetValue("")
        self.form.tags.SetValue("")
        self.form.year.SetValue("")
        
    def updateMode(self, evt):
        focused_index = self.movie_list_ctrl.GetFocusedItem()
        item_count = self.movie_list_ctrl.GetSelectedItemCount()
        if focused_index != -1 and item_count != 0:
            self.edit_mode = True
            self.form.btnRemove.Show()
            movie = self.movie_data[focused_index]            
            self.form.btnSave.SetLabel(self.update_label[1])
            self.form.movieName.SetValue(movie["name"])
            self.form.genre.SetValue(movie["genre"])
            self.form.tags.SetValue(movie["tags"])
            self.form.year.SetValue(movie["year"])
            self.movie_player_ctrl.setVideo("./movies/"+movie["filename"])
            
        if item_count == 0 and focused_index != -1:
            self.form.btnSave.SetLabel(self.update_label[0])
            self.clearForm()
            self.edit_mode = False
            self.form.btnRemove.Hide()

    def doLayouts(self):
        form = self.form
        h_context = wx.BoxSizer(wx.HORIZONTAL)
        #tab_context_sizer = wx.BoxSizer(wx.VERTICAL)  
        list_context = wx.BoxSizer(wx.VERTICAL)   

        formbox = wx.GridSizer(8, 2, 0, 0)
        formbox.Add(form.lblName)
        formbox.Add(form.movieName)
        formbox.Add(form.lblGenre)
        formbox.Add(form.genre)
        formbox.Add(form.lblTags)
        formbox.Add(form.tags)
        formbox.Add(form.lblYear)
        formbox.Add(form.year)
        formbox.Add(form.btnRemove)
        formbox.Add(form.btnSave)

        #tab_context_sizer.Add(formbox, 0, 0, 0)
        list_context.Add(self.movie_list_ctrl, 1, wx.EXPAND, 0)

        h_context.Add(formbox, 0.3, wx.ALIGN_LEFT)
        h_context.Add(list_context, 1, wx.EXPAND, 0)
        h_context.Add(self.movie_player_ctrl, 1, wx.EXPAND)
        self.SetSizer(h_context) 
        self.Layout()

    def bindEvents(self):
        self.movie_list_ctrl.Bind(wx.EVT_LIST_ITEM_SELECTED, self.updateMode)
        self.movie_list_ctrl.Bind(wx.EVT_LIST_ITEM_DESELECTED, self.updateMode)


        
    def onCloseTab(self, event):        
        #self.parent.DeletePage("Movies Panel")
        self.event_handler.delPage("Movies Panel")
        self.movie_player_ctrl.onClose(event)
        #self.event_handler.moviesTab.Destroy()
        self.event_handler.moviesTab = None
        