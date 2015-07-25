#!encoding=utf-8
'''
Created on Jul 24, 2015

@author: luodichen
'''
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import urllib2
import cookielib
from pyquery import PyQuery
from urllib import urlencode

class MsgSnder:
    URL = 'http://www.demohour.com'
    
    def __init__(self):
        cj = cookielib.CookieJar()
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
        urllib2.install_opener(opener)
    
    def login(self, user, password):
        pq = PyQuery(urllib2.urlopen(self.URL).read())
        login_url = self.URL + pq('form#login').attr('action')
        login_data = {}
        inputs = pq('form#login input')
        for i in xrange(len(inputs)):
            login_data[inputs.eq(i).attr('name')] = inputs.eq(i).val()
        
        login_data['login'] = user
        login_data['password'] = password
        
        request = urllib2.Request(login_url, data=urlencode(login_data))
        urllib2.urlopen(request).read()
        
    def send_msg(self, userid, msg):
        ####### test #######
        #userid = '1544688'
        
        url = 'http://www.demohour.com/messages/history?recipient_id=' + userid
        pq = PyQuery(urllib2.urlopen(url).read())
        post_data = {}
        post_url = self.URL + pq('form#new_message').attr('action')
        inputs = pq("form#new_message input")
        for i in xrange(len(inputs)):
            post_data[inputs.eq(i).attr('name')] = inputs.eq(i).val()
        
        post_data['message'] = msg
        
        request = urllib2.Request(post_url, data=urlencode(post_data))
        urllib2.urlopen(request).read()
        
    def get_user_list(self, url):
        ret = []
        pq = PyQuery(url)
        user_list = pq("#review_list dt a[class='c205']")
        for i in xrange(len(user_list)):
            ret.append((user_list.eq(i).attr('href')[1:], user_list.eq(i).text(), ))
        
        return ret
        
    def search_userid(self, action, param, project_depth = 1, page_limit = 10):
        project_list_url = 'http://www.demohour.com/projects/latest?page=%d&sort=2'
        
        for i in xrange(page_limit):
            try:
                pq = PyQuery(project_list_url % (i + 1))
                project_link = pq("#project_list dd[class='c3'] a")
            except e:
                print e
                continue
            
            for j in xrange(len(project_link)):
                try:
                    project_url = project_link.eq(j).attr('href')
                    user_list = self.get_user_list(self.URL + project_url + '/reviews')
                    
                    action(user_list, param)
                except e:
                    print e
                    continue


def action_send(user_list, param):
    sender = param[0]
    msg = param[1]
    
    for user in user_list:
        userid = user[0]
        nickname = user[1]
        print 'send to %s(%s): %s' % (userid, nickname, msg, )
        sender.send_msg(userid, msg)

user = raw_input('user:')
password = raw_input('password:')
msg = raw_input('message:')
if 'yes' != raw_input("send %s to all users, type 'yes' to confirm:" % (msg, )):
    print "canceled."
    exit(0)

sender = MsgSnder()
sender.login(user, password)
sender.search_userid(action_send, (sender, msg, ))

