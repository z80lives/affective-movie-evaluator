import wx
class FormObj:
    pass

class MoviesPanel(wx.Panel):   
    movie_data=[]
    update_label = ["Save", "Update"]
    edit_mode=False

    def __init__(self, parent, event_handler, tab_title):
        super().__init__(parent, wx.ID_ANY)
        self.parent = parent
        self.tab_title = tab_title
        self.form = FormObj()
        self.event_handler = event_handler

        #self.createForm()
        self.doLayouts()
        self.bindEvents()

    def doLayouts(self):
        self.Layout()

    def bindEvents(self):
        pass
        #self.form.btnCloseTab.Bind(wx.EVT_BUTTON, self.onCloseTab)
        
    def onCloseTab(self, event):        
        #self.parent.DeletePage("Movies Panel")
        self.event_handler.delPage("Movies Panel")
        self.event_handler.moviesTab = None
        #self.Destroy()