#!encoding=utf8
'''
Created on Jun 30, 2015

@author: luodichen
'''

import xlrd

class Data(object):
    ERR_NOERROR             =  0
    ERR_NOT_EXCEL_FILE      = -1
    ERR_MISS_COLUMNS        = -2
    
    COLUMNS_NAME = [
        "name", "idcard", "phone", "school", "class", "city", "district"
    ]
    
    COLUMNS = {
        u"学员姓名" : 0,
        u"姓名" : 0,
        u"身份证号码" : 1,
        u"身份证" : 1,
        u"电话" : 2,
        u"联系电话" : 2,
        u"工作单位" : 3,
        u"单位" : 3,
        u"班级名称" : 4,
        u"班级" : 4,
        u"市州" : 5,
        u"市（州）" : 5,
        u"区县" : 6,
        u"县（市区）" : 6,
    }
    
    @staticmethod
    def strcell(cell):
        return u"%.0f" % (cell, ) if isinstance(cell, float) else cell
    
    def __init__(self, filepath):
        self.file = filepath
        self.table = []
        
    def xls_handler(self):
        xls_file = None
        self.table = []
        
        try:
            xls_file = xlrd.open_workbook(self.file)
        except:
            return (self.ERR_NOT_EXCEL_FILE, None, )
            
        sheets = xls_file.sheets()
        
        for table in sheets:
            nrows = table.nrows
            col_index = {}
            i = 0
            while i < nrows:
                row = table.row_values(i)
                
                if 0 == len(col_index):
                    for j in range(len(row)):
                        if row[j] in self.COLUMNS:
                            col_index[self.COLUMNS[row[j]]] = j
                    
                    if 0 != len(col_index) and len(col_index) != len(self.COLUMNS_NAME):
                        err_msg = "file '%s' : miss columns in sheet '%s'" % (self.file, table.name)
                        return (self.ERR_MISS_COLUMNS, err_msg)
                else:
                    self.table.append(tuple(self.strcell(row[col_index[idx]]) for idx in range(len(col_index))))
                i += 1
        return (self.ERR_NOERROR, None,)
