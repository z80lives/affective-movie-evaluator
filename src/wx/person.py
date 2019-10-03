import wx

class FormObj:
    pass

class PersonPanel(wx.Panel):
    people_data = []
    update_label = ["Save", "Update"]
    edit_mode=False
    
    def __init__(self, parent, event_handler, tab_title, person_controller):
        super().__init__(parent, wx.ID_ANY)
        self.top_parent = wx.GetApp().TopWindow
        self.parent = parent
        self.event_handler = event_handler
        self.tab_title = tab_title
        self.controller = person_controller

        self.people_list_ctrl = wx.ListCtrl(self, wx.ID_ANY, style=wx.LC_HRULES | wx.LC_LIST | wx.LC_VRULES | wx.LC_SINGLE_SEL)
        
        self.populateData()
        self.createForm()
        self.setProperties()
        self.doLayout()
        self.doBind()

    def populateData(self):
        self.people_list_ctrl.ClearAll()
        people_data = self.controller.getAll()
        self.people_data = people_data
        for i, person in enumerate(people_data):
            self.people_list_ctrl.InsertItem(i, "%s"%(person["name"]))             
        #self.people_list_ctrl.InsertItem(0, "Hello")        

    def extractFormData(self):
        form = self.form
        return self.controller.createPerson(
            None,
            form.txtPerson.GetValue(),            
            form.choiceGender.GetString(form.choiceGender.GetSelection()),
            form.txtAge.GetValue(),
            form.txtOccupation.GetValue()    
        )
        #return {
        #    "name": form.txtPerson.GetValue(),
        #}

    def onRemovePressed(self, event):
        if self.edit_mode:
            focused_index = self.people_list_ctrl.GetFocusedItem()
            person = self.people_data[focused_index]
            self.controller.removePerson(person["id"])
            self.populateData()

    def onSavePressed(self, event):
        person = self.extractFormData() 
        if not self.edit_mode:               
            self.top_parent.print("Creating person: %s"% (person)) 
        else:
            focused_index = self.people_list_ctrl.GetFocusedItem()
            original_person_data = self.people_data[focused_index]
            person.id = original_person_data["id"]
            self.top_parent.print("Updating person: %s"% (person)) 

        self.controller.savePerson(person)
        self.clearForm()
        self.populateData()

    def createForm(self):
        #sizer_1 = wx.BoxSizer(wx.HORIZONTAL)
        form = FormObj()
                
        form.lblName = wx.StaticText(self, wx.ID_ANY, "Full Name")
        form.txtPerson = wx.TextCtrl(self, wx.ID_ANY, "")
        
        form.lblAge = wx.StaticText(self, wx.ID_ANY, "Age")
        form.txtAge = wx.TextCtrl(self, wx.ID_ANY, "")

        form.lblOccupation = wx.StaticText(self, wx.ID_ANY, "Occupation")
        form.txtOccupation = wx.TextCtrl(self, wx.ID_ANY, "")        
        
        form.lblGender = wx.StaticText(self, wx.ID_ANY, "Gender")
        form.choiceGender = wx.Choice(self, wx.ID_ANY, choices=["male", "female"])


        form.btnSave = wx.Button(self, label=self.update_label[0])        
        form.btnRemove = wx.Button(self, label="Delete")        
        form.btnRemove.Hide()
        #self.list_ctrl_1 = wx.ListCtrl(self, wx.ID_ANY, style=wx.LC_HRULES | wx.LC_LIST | wx.LC_VRULES)
        self.form = form


    def setProperties(self):        
        self.form.choiceGender.SetSelection(0)

    def doLayout(self):
        form = self.form
        h_context = wx.BoxSizer(wx.HORIZONTAL)
        tab_context_sizer = wx.BoxSizer(wx.VERTICAL)  
        list_context = wx.BoxSizer(wx.VERTICAL)      

        form_gridsizer = wx.GridSizer(8, 2, 0, 0)        
        form_gridsizer.Add(form.lblName, 0, wx.ALIGN_CENTER_HORIZONTAL,0)
        form_gridsizer.Add(form.txtPerson, 0, wx.ALL | wx.EXPAND, 0)
        form_gridsizer.Add(form.lblAge, 0, wx.ALIGN_CENTER_HORIZONTAL,0)
        form_gridsizer.Add(form.txtAge, 0,0,0)
        form_gridsizer.Add(form.lblOccupation,  0, wx.ALIGN_CENTER_HORIZONTAL,0)
        form_gridsizer.Add(form.txtOccupation,0,0,0)
        form_gridsizer.Add(form.lblGender,  0, wx.ALIGN_CENTER_HORIZONTAL,0)
        form_gridsizer.Add(form.choiceGender,0,0,0)

        form_gridsizer.Add(form.btnRemove, 0, 0, 0) 
        form_gridsizer.Add(form.btnSave, 0, wx.ALIGN_CENTER_HORIZONTAL, 0)

        tab_context_sizer.Add(form_gridsizer, 0, 0, 0)                
        list_context.Add(self.people_list_ctrl, 1, wx.EXPAND, 0)
        h_context.Add(tab_context_sizer)
        h_context.Add(list_context, 1, wx.EXPAND, 0)
        self.SetSizer(h_context) 
        self.Layout()

    def doBind(self):
        self.form.btnSave.Bind(wx.EVT_BUTTON, self.onSavePressed )
        self.form.btnRemove.Bind(wx.EVT_BUTTON, self.onRemovePressed )
        self.people_list_ctrl.Bind(wx.EVT_LIST_ITEM_SELECTED, self.updateMode)
        self.people_list_ctrl.Bind(wx.EVT_LIST_ITEM_DESELECTED, self.updateMode)

    def updateMode(self, evt):
        focused_index = self.people_list_ctrl.GetFocusedItem()
        item_count = self.people_list_ctrl.GetSelectedItemCount()
        if focused_index != -1 and item_count != 0:
            self.edit_mode = True
            self.form.btnRemove.Show()
            person = self.people_data[focused_index]
            self.form.btnSave.SetLabel(self.update_label[1])
            self.form.txtPerson.SetValue(person["name"])
            self.form.txtAge.SetValue(person["age"])
            self.form.txtOccupation.SetValue(person["occupation"])
            gender = person["gender"]
            if gender == "male":
                self.form.choiceGender.SetSelection(0)
            else:
                self.form.choiceGender.SetSelection(1)

        if item_count == 0 and focused_index != -1:
            self.form.btnSave.SetLabel(self.update_label[0])
            self.clearForm()
            self.edit_mode = False
            self.form.btnRemove.Hide()

    def clearForm(self):
        self.form.txtPerson.SetValue("")
        self.form.txtAge.SetValue("")
        self.form.txtOccupation.SetValue("")
        self.form.choiceGender.SetSelection(0)

    def onCloseTab(self, event):        
        #self.parent.DeletePage("Person Panel")
        self.event_handler.delPage("Person Panel")
        self.event_handler.personTab = None