#!python
'''
Created on May 15, 2015

@author: luodichen
'''

from pyquery import PyQuery
from fileinput import filename
import sqlite3

database = "../hnust-data.db"
pagecount = 466

def main():
    create_table = "CREATE TABLE IF NOT EXISTS students (_id INTEGER PRIMARY KEY AUTOINCREMENT, \
                    original_id INT, student_id TEXT, name TEXT, name_pinyin TEXT, used_name TEXT, sex TEXT, \
                    school TEXT, discipline TEXT, discipline2 TEXT, class TEXT, birth TEXT, idcard TEXT, \
                    examinee_id TEXT, validity TEXT, school_roll_state TEXT, starting_date TEXT, \
                    training_level TEXT, research TEXT, tutor TEXT, credit TEXT, nation TEXT, hometown TEXT, \
                    blood_type TEXT, political TEXT, marriage TEXT, foreigner TEXT, religion TEXT, health TEXT, \
                    address TEXT, post_code TEXT, mobile TEXT, email TEXT, homepage TEXT, comment TEXT, creator TEXT, \
                    create_time TEXT, from_xinjiang TEXT, property TEXT)"
                    
    insert_keys = "(original_id, student_id, name, name_pinyin, used_name, sex, \
                    school, discipline, discipline2, class, birth, idcard, \
                    examinee_id, validity, school_roll_state, starting_date, \
                    training_level, research, tutor, credit, nation, hometown, \
                    blood_type, political, marriage, foreigner, religion, health, \
                    address, post_code, mobile, email, homepage, comment, creator, \
                    create_time, from_xinjiang, property, xiaoxiang)"
    
    conn = sqlite3.connect(database)
    sqlite_cursor = conn.cursor()
    sqlite_cursor.execute(create_table)
    
    for k in range(1, pagecount + 1):
        file = open("../hnust-xx-package/page-xx-" + str(k) + ".html", "r")
        pq = PyQuery(unicode(file.read(), "utf-8"))
        rows =  pq("#mxh tr")
        for i in range(0, rows.length):
            cols =  rows.eq(i).find("td")
            insert_values = "("
            for j in range(1, cols.length - 2):
                col = cols.eq(j)
                print col.html() + ",",
                if 1 == j:
                    insert_values = insert_values  + "'" + col.html().strip() + "'"
                else:
                    insert_values = insert_values + ", '" + col.html().strip() + "'"
            
            insert_values = insert_values + ", '1')"
            sql_insert = "INSERT INTO students " + insert_keys + " VALUES " + insert_values
            sqlite_cursor.execute(sql_insert);
            print ""
        file.close()
        conn.commit()
    
    conn.close()
    
main()