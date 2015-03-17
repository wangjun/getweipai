#!/usr/bin/env python
#coding=utf-8
#Author:Richard Liu
#Blog: http://richardxxx0x.wicp.net
#Email:<richardxxx0x@gmail.com>
#Usage:python geturl.py weipaiUrl  其中weipaiUrl参数即微拍个人主页网址，直接复制网址替换weipaiUrl即可.

"""
...............................
#    # ###### # #####    ##   # 
#    # #      # #    #  #  #  # 
#    # #####  # #    # #    # # 
# ## # #      # #####  ###### # 
##  ## #      # #      #    # # 
#    # ###### # #      #    # # 
...............................

get weipai video url from user's page.
 
USAGE: python geturl.py <weipaiurl>
EXAMPLE: python geturl.py http://www.weipai.cn/user/5135b9d5813494e64000012f
"""

from BeautifulSoup import BeautifulSoup
import urllib2
import re
import sys
import time

def get_userinfo(url):
    global videonums
    html_page = urllib2.urlopen(url)
    userinfo = BeautifulSoup(html_page)
    videonums_info = userinfo.find('li','videos').span.getText()
    videonums = int(videonums_info)

def get_url(url):
    html_page = urllib2.urlopen(url)
    soup = BeautifulSoup(html_page)
    for link in  soup.findAll('img',src=re.compile(r'.*v.weipai.cn/video.*|.*aliv.weipai.cn')):
	videoUrl.append(link.get('src'))



videoUrl = []
videonums = 0
num = 0
def main():
    global num
    url = sys.argv[1]
    get_userinfo(url)
    print "总共有%d个视频！" %(videonums)
    print "你想获取多少个视频下载链接？"
    num = input("输入个数:")
    start = time.time()

    if num > videonums:
        num = videonums
    if num == 0:
        sys.exit(0)
    pagenumber = num/14+2

    for i in range(1,pagenumber):
        get_url(url+"?page="+str(i))
        
    print "Elapsed Time: %s" % (time.time() - start)

    
  
if __name__ == "__main__":
    print __doc__
    if len(sys.argv) == 2:
        main()
        videoUrl = [re.sub(r'\.\d?\.?jpg','.flv',url) for url in videoUrl]
        videoUrl = videoUrl[0:num]
        result = '\n'.join(videoUrl)
        file = open('videoUrl.txt','w')    
        file.write(result)
        file.close() 
        print "视频链接已经存在videoUrl.txt文件中:)，如需下载视频，可以通过百度离线或者linux工具，如wget or axel"
