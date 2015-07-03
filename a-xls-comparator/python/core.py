#!encoding=utf-8
'''
Created on Jun 30, 2015

@author: luodichen
'''

from data import Data

class DataIndex(object):
    def __init__(self, table):
        self.table = table
        self.index_column = (Data.COL_NAME, Data.COL_IDCARD, Data.COL_PHONE, )
        self.index = ({}, {}, {}, ) # name, idcard, phone
        self.load()
        
    def load(self):
        for row in self.table:          
            for i in range(len(self.index_column)):
                key = row[self.index_column[i]].replace(" ", "")
                if key not in self.index[i]:
                    self.index[i][key] = []
                self.index[i][key].append(row)

