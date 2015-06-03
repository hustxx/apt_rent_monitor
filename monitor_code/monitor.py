# Thsi is for apartments price auto checking
# Xiang Xu Jun 2015

#! /usr/bin/python

import urllib2
import re

class apt_rent_monitor:
	
	def __init__(self):
		aptName = ["Archerstone", "Alborada", "Mission Peaks", "Mission Peaks II"]
		aptUrl = ["http://www.equityapartments.com/california/san-francisco-bay-apartments/fremont/archstone-fremont-center-apartments.aspx",
		          "http://www.equityapartments.com/california/san-francisco-bay-apartments/fremont/alborada-apartments.aspx",
			  "https://www.essexapartmenthomes.com/api/get-available/sfo1132",
			  "https://www.essexapartmenthomes.com/api/get-available/sfo1205"]
#		pattern1 = re.compile('<div class="floorplan">.*?<h3>(.*?)</h3>.*?<p>from <b>(.*?)</b>(.*?)</p>', re.S)
		pattern1 = re.compile('<div class="unit">.*?<h4>(.*?)</h4>.*?<p><b>\$(.*?)</b>.*?<p>available <b>(.*?)</b>', re.S)
		pattern2 = re.compile('{"unit_id":.*?"unit_type_floor_plan_name":"(.*?)","make_ready_date":.*?,"rent":(.*?),".*?"beds":"1.0".*?"available_date":"(.*?)"', re.S)
		
		self.moveInDate = "06-24-2015"
		self.aptInfo = []
		self.availableRooms = []
		for i in range(2):
			self.aptInfo.append([aptName[i], aptUrl[i], pattern1])
		for j in range(2,4):
			aptUrl[j] = aptUrl[j] + "/" + self.moveInDate
			self.aptInfo.append([aptName[j], aptUrl[j], pattern2])

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
	
	def printPrices(self, allAptPrices):
		for apt in allAptPrices:
			print apt[0]
			for room in apt[1]:
				print room[0], room[1], room[2]

	def start(self):
#		apartments = []
		for apt in self.aptInfo:
			aptPrices = self.getPrices(apt[2], apt[1])
#			sort(aptPrices, key=aptPrices[1].lower)
			self.availableRooms.append([apt[0], aptPrices])
#		self.printPrices(apartments)		 	
			print apt[0]
			for room in aptPrices:
				print room[0], room[1], room[2]		

spider = apt_rent_monitor()
#pageCode = spider.getPage(spider.aptInfo[2][1])
#result = re.findall(spider.aptInfo[2][2], pageCode)
#print result
spider.start()
