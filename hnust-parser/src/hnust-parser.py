'''
Created on May 15, 2015

@author: luodichen
'''
#!python

from pyquery import PyQuery
from fileinput import filename
import sqlite3

def main():
    insert_keys = "(original_id, student_id, name, name_pinyin, used_name, sex, \
                    school, discipline, discipline2, class, birth, idcard, \
                    examinee_id, validity, school_roll_state, starting_date, \
                    training_level, research, tutor, credit, nation, hometown, \
                    blood_type, political, marriage, foreigner, religion, health, \
                    address, post_code, mobile, email, homepage, comment, creator, \
                    create_time, from_xinjiang, property)"
    
    conn = sqlite3.connect("../hnust-data.s3db")
    file = open("../hnust-package/page1.html", "r")
    pq = PyQuery(unicode(file.read(), "utf-8"))
    rows =  pq("#mxh tr")
    for i in range(0, rows.length):
        cols =  rows.eq(i).find("td")
        for j in range(1, cols.length - 2):
            col = cols.eq(j)
            print col.html() + ",",
        
        print ""
    
    
    conn.close()
    file.close()
main()