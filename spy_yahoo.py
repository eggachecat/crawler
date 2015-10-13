# coding=utf-8
import MySQLdb
import urlparse
import urllib
import re
import sys
from bs4 import BeautifulSoup
import threading
import os
import time

urls_pool_lock = threading.Lock()
save_file_lock = threading.Lock()

#constant values-key
keyword_nav = 'Yahoo奇摩首頁'.decode('utf-8', 'igonire')

keyword_class_finanical = '財經'.decode('utf-8', 'igonire')
keyword_class_politics = '政治'.decode('utf-8', 'igonire')
keyword_class_tv = '影劇'.decode('utf-8', 'igonire')
keyword_class_sports = '運動'.decode('utf-8', 'igonire')
keyword_class_social = '社會'.decode('utf-8', 'igonire')
keyword_class_local = '地方'.decode('utf-8', 'igonire')
keyword_class_international = '國際'.decode('utf-8', 'igonire')
keyword_class_life = '生活'.decode('utf-8', 'igonire')

classList = [keyword_class_finanical,keyword_class_politics,keyword_class_life,keyword_class_international,keyword_class_tv,keyword_class_local,keyword_class_sports,keyword_class_social]

#constant values-url
iniUrl = 'https://tw.news.yahoo.com/finance/'
rootUrl = 'https://tw.news.yahoo.com'

#init url
urls = [iniUrl,rootUrl]
visited = [iniUrl,rootUrl]

def initCrawler():
	url = getUrl()
	if not url:
		print "get url error"
		exit(1)
	try:
		htmltext = urllib.urlopen(url).read().decode('utf-8', 'ignore')
	except:
		print thread_id," : ",url,"read failed !!"
		exit(1)

	soup = BeautifulSoup(htmltext)
	fetchUrl(soup)

def crawler(thread_id):
	
	while True :
		url = getUrl()
		if not url:
			print "get url error"
			break

		try:
			htmltext = urllib.urlopen(url).read().decode('utf-8', 'ignore')
		except:
			print thread_id," : ",url,"read failed !!"
			continue

		soup = BeautifulSoup(htmltext)

		#thread to analysize html
		t = threading.Thread(target= fetchUrl, args=[soup])
		t.setDaemon(False)
		t.start()

		for navi_div in soup.find_all("div", {"class":"yom-mod yom-articlemenu"}):
			navBar = str(navi_div).decode('utf-8', 'igonire')
			if keyword_nav in navBar:
				article_class = detectClass(classList,navBar)

				articleTitle = soup.find("h1", {"class":"headline"}).contents[0]

				article = ''
				articleDiv = soup.find("div", {"class":"yom-mod yom-art-content "})		
				for paragraph in articleDiv.findChildren("p"):
					try:
						article += paragraph.contents[0]
					except:
						continue

				try:
					# print article_class,"<->",articleTitle,":"
					# print article
					with save_file_lock:
						saveFile(article_class, articleTitle, article)	
				except:
					pass
def saveUrl(period):
	visited_des = "visited.txt"
	urls_des = "urls.txt"
	while True:
		time.sleep(period)
		
		try:
			visiteFileHandle = open(visited_des, "w")
			for url in visited:
				visiteFileHandle.write(url+'\n')
			visiteFileHandle.close()
		except:
			print "save visited failed!"

		try:
			urlsFileHandle = open(urls_des, "w")
			for url in urls:
				urlsFileHandle.write(url+'\n')
			urlsFileHandle.close()
			print "urls left: ",len(urls)
		except:
			print "save urls failed!"


def saveFile(newClass, title, content):
	des = "news/"+newClass+"/"+title+".txt"
	try:
		fileHandle = open(des, "w+")
		fileHandle.write(title.encode("utf-8")+'\n')
		fileHandle.write(content.encode("utf-8"))
		fileHandle.close()
	except:
		print des," failed to save file"
		pass

def detectClass(classList,navi):
	for articleClass in classList:
		if articleClass in navi:
			return articleClass
	return False

		
# def save_to_mysql():
# 	#handle database
# 	db = MySQLdb.connect("localhost","root","password","testdb" )
# 	cursor = db.cursor()

def fetchUrl(soup):
	for tag in soup.find_all("a", href=True):
			newUrl = urllib.quote(tag["href"].encode('utf8'))
			newUrl = urlparse.urljoin(rootUrl, newUrl)	
			# print newUrl,len(newUrl)
			if (rootUrl in newUrl) and (newUrl not in visited) and (len(newUrl)>100):
				urls.append(newUrl)
				visited.append(newUrl)


def getUrl():
	if len(urls) > 0:
		with urls_pool_lock:
			url = urls[0]
			urls.pop(0)
			return url

	return False

def main():

	if not os.path.exists("news"):
		os.makedirs("news")
	for Class in classList:
		if not os.path.exists("news/"+Class):
			os.makedirs("news/"+Class)

	NumOfThread = 10  #number of thread

	thread_pool = []

	initCrawler()
	print len(urls)

	for x in range(1,NumOfThread):
		t = threading.Thread(target= crawler, args= [x])
		thread_pool.append(t)
		t.start()

	protect = threading.Thread(target= saveUrl, args= [60])
	protect.setDaemon(True)
	protect.start()


	for t in thread_pool:
		t.join()

if __name__ == '__main__':
	main()