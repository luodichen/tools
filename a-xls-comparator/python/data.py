#!encoding=utf8
'''
Created on Jun 30, 2015

@author: luodichen
'''

import xlrd
import fileinput

class ParseError(Exception):
    def __init__(self, message, code):
        super(ParseError, self).__init__(message)
        self.code = code   

class Data(object):
    ERR_NOERROR             =  0
    ERR_NOT_EXCEL_FILE      = -1
    ERR_MISS_COLUMNS        = -2
    ERR_FORMAT_NOT_SUPPORTED= -3
    
    COL_NAME    = 0
    COL_IDCARD  = 1
    COL_PHONE   = 2
    COL_SCHOOL  = 3
    COL_CLASS   = 4
    COL_CITY    = 5
    COL_DISTRICT= 6
    
    COLUMNS_NAME = [
        "name", "idcard", "phone", "school", "class", "city", "district"
    ]
    
    COLUMNS = {
        u"学员姓名" : COL_NAME,
        u"姓名" : COL_NAME,
        u"身份证号码" : COL_IDCARD,
        u"身份证" : COL_IDCARD,
        u"电话" : COL_PHONE,
        u"联系电话" : COL_PHONE,
        u"工作单位" : COL_SCHOOL,
        u"单位" : COL_SCHOOL,
        u"班级名称" : COL_CLASS,
        u"班级" : COL_CLASS,
        u"市州" : COL_CITY,
        u"市（州）" : COL_CITY,
        u"区县" : COL_DISTRICT,
        u"县（市区）" : COL_DISTRICT,
    }
    
    @classmethod
    def strcell(cls, cell):
        return u"%.0f" % (cell, ) if isinstance(cell, float) else cell
    
    @classmethod
    def detect_header(cls, row):
        ret = {}
        for i in range(len(row)):
            if row[i] in cls.COLUMNS:
                ret[cls.COLUMNS[row[i]]] = i
        return ret
                
    def __init__(self, filepath):
        self.file = filepath
        self.table = []
        
        err, msg = self.xls_handler()
        if self.ERR_NOERROR == err:
            return
        err, msg = self.txt_handler()
        if self.ERR_NOERROR != err:
            raise ParseError(msg, err)
        
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
                    col_index = Data.detect_header(row)
                    if 0 != len(col_index) and len(col_index) != len(self.COLUMNS_NAME):
                        err_msg = "file '%s' : miss columns in sheet '%s'" % (self.file, table.name)
                        return (self.ERR_MISS_COLUMNS, err_msg)
                else:
                    self.table.append(tuple(self.strcell(row[col_index[idx]]) for idx in range(len(col_index))))
                i += 1
        return (self.ERR_NOERROR, None,)
    
    def txt_handler(self):
        col_index = {}
        try:
            for line in fileinput.input(self.file):
                row = line.decode("gbk").split("\t")
                
                if 0 == len(col_index):
                    col_index = Data.detect_header(row)
                    if 0 != len(col_index) and len(col_index) != len(self.COLUMNS_NAME):
                        err_msg = "file '%s' : miss columns" % (self.file, )
                        return (self.ERR_MISS_COLUMNS, err_msg)
                else:
                    self.table.append(tuple(self.strcell(row[col_index[idx]]) for idx in range(len(col_index))))
        except:
            return (self.ERR_FORMAT_NOT_SUPPORTED, "file format not support : %s" % (self.file, ))
        
        return (self.ERR_NOERROR, None)
    
    def get_table(self):
        return self.table
