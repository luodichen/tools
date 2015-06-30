#!encoding=utf-8
'''
Created on Jun 30, 2015

@author: luodichen
'''

import xlrd

excel_file = xlrd.open_workbook(unicode(r"D:\ljq\555学员学情统计表.xls", "utf8"))
table = excel_file.sheets()[0]
for i in range(50):
    print table.row_values(i)[1]
