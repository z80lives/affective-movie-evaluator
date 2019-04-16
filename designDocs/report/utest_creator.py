import pandas as pd
        
class UnitTestPlan:
    def __init__(self, width="6in"):
        self.width= width
        self.title = "Unit Test Plan"
        #self.title="\multicolumn{2}{|c|}{Team sheet}"
        self.rows = []
        self.col_count = 2
        self.setupTable()

    def setupTable(self, color="blue", span=None):
        self.clearTable()
        self.addRow(self.title, color=color, span=span, heading=True)

    def clearTable(self):
        self.rows = []

    def addRow(self, txt, span=None,
               bold=False,
               color=None,
               colVal=25, heading=False,
               multicolumn=None):
        bottom=False
        top = False

        row = txt
        if type(row) != type([]):
            row = [txt]
        
        if heading:
            bold = True
            bottom=True

        length = 0
        for i,t in enumerate(row):
            
            if bold:
                t="\\textbf{%s}" % (t)
            if span:
                s = "<%s> \n " % (span)
                t = s + t
            
            if color:
                t = t + " \cellcolor{%s!%i}"%(color, colVal)
            row[i] = t
            length += 1

        if length < self.col_count:
            multicolumn = True

        if multicolumn:
            #row = ["\multicolumn{2}{|p{%s}|}{%s}" % (self.width, row[0])]
            row = [row[0]]
            
        if top:
            self.rows.append(None)
        self.rows.append(row)
        if bottom:
            self.rows.append(None)
            
    def split(self):
        self.rows.append(None)
        
    def makeTable(self):
        #test = pd.DataFrame({'A': [1000, 1000], 'B' : [60, 100]})
        #test2 = [list(test)] + [None] + test.values.tolist()
        #return test2
        tbl = self.rows
        return [None] + tbl + [None]

    def makeLatex(self, c="|p{6in}|"):
        #wrap = "#+BEGIN_EXPORT latex\n %s \n#+END_EXPORT"
        
        env = "\\begin{{{0}}}\n{1}\n\end{{{0}}}"
        env2 = "\\begin{{{0}}}{{{2}}}\n{1}\n\end{{{0}}}"
        longtable= env.format("longtable", "%s")
        #tabular = env2.format("tabular", "\hline %s \n\hline", c)
        tabular = env2.format("longtable", "\hline %s \n\hline", c)

        head = None
        
        tbody=""
        prev_hl = False
        prev_ml = False
        row_c = 0
        for row in self.rows:
            if row is None:
                tbody += "\n \\hline"
                prev_hl = True
                continue
            
            rwstr = "\n"
            col_c = 0
            multicolumn = False
            for i, col in enumerate(row):
                if i > 0:
                    rwstr += " \hspace{1in} "
                rwstr += col
                col_c += 1

            if col_c < self.col_count:
                multicolumn = True
                

            cond1 = multicolumn and not prev_hl and row_c != 0
            cond2 = prev_ml and not prev_hl
            if cond1 or cond2:
                tbody += "\hline" + rwstr + "\\\\"
            else:
                tbody += rwstr+" \\\\ "            
                
            #if prev_ml and row_c != 0 and not multicolumn:
            #    tbody = "\hline1" 

            prev_hl = False
            prev_ml = multicolumn
            row_c += 1

            if head is None: #this is is the head
                head = tbody                
                tbody =  "%s \n\\hline \n\\endfirsthead \n\\multicolumn{1}{l}{Continued from previous page} \\\\ \n\\hline \n%s \\\\ \n\\hline \n\\endhead \n\\hline\\multicolumn{1}{r}{Continued on next page} \\ \n\\endfoot \n\\endlastfoot \n\\hline \n" % (head, head )
                
            
        tbl = tabular % (tbody)
        latex_code = tbl
        return latex_code
        #return wrap % (latex_code)

    def createPlan(self, ad):
          self.addRow(["\\textbf{Module Name: } %s"%("SampleLoader"), "\\textbf{File:}\\path{%s}"%("./test/path_test.py")])
          self.addRow("1. Module Overview", bold=True)
          self.addRow(ad[0])
          self.addRow("1.1 Inpself to Module", bold=True)
          self.addRow(ad[1])
          self.addRow("1.2 Output from Module", bold=True)
          self.addRow(ad[2])
          self.addRow("1.3 Logic Flow", bold=True)
          self.addRow(ad[3])
          self.addRow("2. Test Data", bold=True)
          self.addRow(ad[4])
          self.addRow("2.1 Positive Test Cases", bold=True)
          self.addRow(ad[5])
          self.addRow("2.2 Negative Test Cases", bold=True)
          self.addRow(ad[6])
          self.addRow("2.2 Interface Modules", bold=True)
          self.addRow(ad[7])
          self.addRow("2.3 Test Tools", bold=True)
          self.addRow(ad[8])    


        
