import wx

class FormObj:
    pass

class AnalyseTabPanel(wx.Panel):
    def __init__(self, parent, event_handler, _sid):
        super().__init__(parent, wx.ID_ANY)
        self.form = FormObj()
        self._sid = _sid
        
        self.form.gauge_1 = wx.Gauge(self, wx.ID_ANY, 10)
        self.form.chkFER = wx.CheckBox(self, wx.ID_ANY, "FER")
        self.form.chkBEGR = wx.CheckBox(self, wx.ID_ANY, "BEGR (Head)")
        self.form.chkTimeSeries = wx.CheckBox(self, wx.ID_ANY, "Generate Time Series")
        self.form.chkRep = wx.CheckBox(self, wx.ID_ANY, "Generate Representation")
        self.form.chkScore = wx.CheckBox(self, wx.ID_ANY, "Calculate Score")
        self.form.chkPreview = wx.CheckBox(self, wx.ID_ANY, "Preview (Not Recommended)")
        self.form.btnCancel = wx.Button(self, wx.ID_ANY, "Cancel")
        self.form.btnStart = wx.Button(self, wx.ID_ANY, "Start")

        self.event_handler = event_handler
        self._do_layout()
        self.do_bind()
        
    def _do_layout(self):
        sizer_cont = wx.BoxSizer(wx.HORIZONTAL)
        sizer_left_v = wx.BoxSizer(wx.VERTICAL)
        grid_sizer_1 = wx.GridSizer(3, 3, 0, 0)
        
        lblProgressTitle = wx.StaticText(self, wx.ID_ANY, "Progress")
        sizer_left_v.Add(lblProgressTitle, 1, wx.ALIGN_BOTTOM | wx.ALL, 2)
        sizer_left_v.Add(self.form.gauge_1, 0, wx.EXPAND, 0)
        lblProgress = wx.StaticText(self, wx.ID_ANY, "")
        sizer_left_v.Add(lblProgress, 2, 0, 0)

        
        sizer_cont.Add(sizer_left_v, 1, wx.EXPAND, 0)

        
        grid_sizer_1.Add(self.form.chkFER, 0, 0, 0)
        grid_sizer_1.Add(self.form.chkBEGR, 0, 0, 0)
        grid_sizer_1.Add(self.form.chkTimeSeries, 0, 0, 0)
        grid_sizer_1.Add(self.form.chkRep, 0, 0, 0)
        grid_sizer_1.Add(self.form.chkScore, 0, 0, 0)
        grid_sizer_1.Add(self.form.chkPreview, 0, 0, 0)
        grid_sizer_1.Add(self.form.btnCancel, 0, wx.ALIGN_BOTTOM, 0)
        grid_sizer_1.Add((0, 0), 0, 0, 0)
        grid_sizer_1.Add(self.form.btnStart, 0, wx.ALIGN_BOTTOM | wx.ALIGN_RIGHT, 0)

        sizer_cont.Add(grid_sizer_1, 1, wx.EXPAND, 0)

        self.SetSizer(sizer_cont)
        self.Layout()

        
    def do_bind(self):
        self.form.btnCancel.Bind(wx.EVT_BUTTON, self.event_handler.onCloseAnalyserTab )
        self.form.btnStart.Bind(wx.EVT_BUTTON,
                                lambda event:
                                self.event_handler.onAnalyse(event, self._sid, self.form)
        )
        
        
