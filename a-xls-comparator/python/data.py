#!encoding=utf8
'''
Created on Jun 30, 2015

@author: luodichen
'''

import xlrd

class Data(object):
    COLUMNS_NAME = [
        "name", "idcard", "phone", "school", "class", "city", "district"
    ]
    COLUMNS = {
        u"学员姓名" : 0,
        u"姓名" : 0,
        u"身份证号码" : 1,
        u"联系电话" : 2,
        u"工作单位" : 3,
        u"班级名称" : 4,
        u"班级" : 4,
        u"市州" : 5,
        u"市（州）" : 5,
        u"区县" : 6,
        u"县（市区）" : 6,
    }
    
    
    
    def __init__(self, filepath):
        self.file = filepath
        self.table = []
        
    def xls_handler(self):
        xls_file = xlrd.open_workbook(self.file)
        sheets = xls_file.sheets()
        
        for table in sheets:
            nrows = table.nrows
            col_index = {}
            i = 0
            while i < nrows:
                if 0 == len(col_index):
                    row = table.row_values(i)
                    
                elif len(self.COLUMNS_NAME) != len(col_index):
                    pass
                else:
                    pass
                i += 1