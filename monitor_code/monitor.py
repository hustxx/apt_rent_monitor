# Thsi is for apartments price auto checking
# Xiang Xu Jun 2015

#! /usr/bin/python

import urllib2
import re

class apt_rent_monitor:
	
	def __init__(self):
		self.aptURL = []
		self.aptURL.append(["Archerstone", "http://www.equityapartments.com/california/san-francisco-bay-apartments/fremont/archstone-fremont-center-apartments.aspx"])
		self.aptURL.append(["Alborada", "http://www.equityapartments.com/california/san-francisco-bay-apartments/fremont/alborada-apartments.aspx"])
		self.pattern1 = re.compile('<div class="floorplan">.*?<h3>(.*?)</h3>.*?<p>from <b>(.*?)</b>(.*?)</p>', re.S)

	def getPage(self, aptURL):
		try:
			request = urllib2.Request(aptURL)
			response = urllib2.urlopen(request)
			pageCode = response.read()
			return pageCode
		except urllib2.URLError, e:
			if hasattr(e, "reason"):
				print u"can not connect to the website", e.reason
				return None

	def getPrices(self, pattern, aptURL):
		pageCode = self.getPage(aptURL)
		if not pageCode:
			print "can not reach the website..."
			return None
		items = re.findall(pattern, pageCode)

		aptPrices = []
		for item in items: 
			aptPrices.append([item[0].strip(), item[1].strip(), item[2].strip()])
		return aptPrices

	def printPrices(self):
		apartments = []
		for apt in self.aptURL:
			aptPrices = self.getPrices(self.pattern1, apt[1])
			apartments.append([apt[0], aptPrices])
		 	print apt[0]
			for room in aptPrices:
				print room[0], room[1], room[2]		

spider = apt_rent_monitor()
pageCode = spider.printPrices()

