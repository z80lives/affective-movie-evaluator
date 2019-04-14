import wx

        
class FormObj:
    pass

class RecordTabPanel(wx.Panel):    
    def __init__(self, parent, event_handler):
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
        self.form.btnRecord = wx.Button(self, wx.ID_ANY, "Record")
        self.form.btnCloseTab = wx.Button(self, wx.ID_ANY, "Close")

        self.event_handler =  event_handler
        self.parent = parent
        self.do_layout()
        self.do_bind()


    def do_layout(self):
        tab_context_sizer = wx.BoxSizer(wx.VERTICAL)
        form_gridsizer = wx.GridSizer(8, 2, 0, 0)        

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
        form_gridsizer.Add(self.form.btnCloseTab, 0, 0, 0)
        form_gridsizer.Add(self.form.btnRecord, 0, 0, 0)

        tab_context_sizer.Add(form_gridsizer, 0, 0, 0)
        
        self.SetSizer(tab_context_sizer)        
        self.Layout()

        #event.Skip()
        
    def do_bind(self):
        #self.form.btnCloseTab.Bind(wx.EVT_BUTTON, lambda event: self.event_handler.onCloseTab(event, self) )
        self.form.btnCloseTab.Bind(wx.EVT_BUTTON, self.event_handler.onCloseTab )
        #self.form.btnCloseTab.Bind(wx.EVT_BUTTON, self.onCloseTab )
        self.form.btnRecord.Bind(wx.EVT_BUTTON, lambda event: self.event_handler.onRecord(event, self.form) )

        #self.Close() 
        
        
