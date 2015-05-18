#!python

import urllib2
import sqlite3

url_kd = "http://kdjw.hnust.cn/kdjw/uploadfile/studentphoto/pic/"
url_xx = "http://xxjw.hnust.cn/xxjw/uploadfile/studentphoto/pic/"
store_path = "../photo-package/"
database = "../../hnust-parser/hnust-data.db"
sql_query = "SELECT student_id, xiaoxiang FROM students WHERE student_id LIKE '09%'"

def download_photo(student_id, is_xiaoxiang = False):
    if is_xiaoxiang:
        url = url_xx
    else:
        url = url_kd
        
    url = url + student_id + ".JPG"
    print url
    
    try:
        http_file = urllib2.urlopen(url)
        save_file = open(store_path + student_id + ".jpg", "wb")
        bufsize = 2048
        while True:
            data = http_file.read(bufsize)
            if 0 == len(data):
                break
            save_file.write(data)
        print "saved."
    except Exception as e:
        print "failed."
        print e
        return False
    
    return True

def work():
    conn = sqlite3.connect(database)
    cur = conn.cursor()
    cur.execute(sql_query)
    
    while True:
        row = cur.fetchone()
        if None == row:
            break
        download_photo(row[0], 1 == row[1])
    
    conn.close()

work()