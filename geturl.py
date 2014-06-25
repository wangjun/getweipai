#!/usr/bin/env python
#coding=utf-8

from BeautifulSoup import BeautifulSoup
import urllib2
import re
import sys
import Queue
import threading
import time 

queue = Queue.Queue()
def get_userinfo(url):
    global videonums
    html_page = urllib2.urlopen(url)
    userinfo = BeautifulSoup(html_page)
    videonums_info = userinfo.find('li','videos').span.getText()
    videonums = int(videonums_info)

def get_url(url):
    html_page = urllib2.urlopen(url)
    soup = BeautifulSoup(html_page)
    for link in soup.findAll('div',attrs={"class":"wf_cell video box "}):
        videoUrl.append("http://www.weipai.cn/video/"+link.get('id')) 

def get_video(url):
    html_page = urllib2.urlopen(url)
    soup = BeautifulSoup(html_page)
    for link in  soup.findAll('img',src=re.compile(r'.*v.weipai.cn/video.*|.*aliv.weipai.cn')):
	result.append(link.get('src'))

class GetUrlThread(threading.Thread):
    def __init__(self,queue):
            threading.Thread.__init__(self)
            self.queue = queue
    def run(self):
            while True:   
                     url = self.queue.get()
                     get_video(url)
                     self.queue.task_done()

result = []
videoUrl = []
videonums = 0
start = time.time()
def main():
    url = sys.argv[1]
    get_userinfo(url)
    print "总共有%d个视频！" %(videonums)
    print "你想获取多少个视频下载链接？"
    num = input("输入个数:")
   
    if num > videonums:
        num = videonums
    if num == 0:
        sys.exit(0)
    pagenumber = num/14+2

    for i in range(1,pagenumber):
	get_url(url+"?page="+str(i))
    
    for i in range(20):
        t = GetUrlThread(queue)
        t.setDaemon(True)
        t.start()

    for i in range(0,num):
        url = videoUrl[i]
        queue.put(url)
    
    queue.join()
   
if __name__ == "__main__":
    main()
    result = map(lambda foo: foo.replace('mov.3in1.jpg', 'flv'), result)
    for i in result:
	print i

print "Elapsed Time: %s" % (time.time() - start)
