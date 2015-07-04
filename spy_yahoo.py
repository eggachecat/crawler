# -*- coding: utf8 -*- 
import urllib
import re
from bs4 import BeautifulSoup
url = 'https://tw.news.yahoo.com/%E5%88%A9%E7%A9%BA%E5%87%BA%E7%9B%A1%E8%B2%B7%E7%9B%A4%E5%9B%9E%E9%A0%AD-6%E6%9C%88%E5%85%AD%E9%83%BD%E5%BB%BA%E7%89%A9%E8%B2%B7%E8%B3%A3%E7%A7%BB%E8%BD%89%E6%9C%88%E5%A2%9E6.3-040015893.html'
htmltext = urllib.urlopen(url).read().decode('utf-8', 'ignore')
soup = BeautifulSoup(htmltext)
keyword_nav = 'Yahoo奇摩首頁'.decode('utf-8', 'igonire')
keyword_class = '財經'.decode('utf-8', 'igonire')

for tag in soup.find_all("div", {"class":"yom-mod yom-articlemenu"}):
	navBar = str(tag).decode('utf-8', 'igonire')
	if keyword_nav in navBar and keyword_class in navBar:
		article = ''
		articleDiv = soup.find("div", {"class":"yom-mod yom-art-content "})		
		for paragraph in articleDiv.findChildren("p"):
			try:
				print paragraph.contents[0]
			except:
				pass


		
	# if keyword in tag:
	# 	print "!!!"
