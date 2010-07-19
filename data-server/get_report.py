import urllib,datetime
import os
import sys
import getopt
import string
import urllib
import re
import fnmatch
import glob,time
from metar import Metar
import pickle

import urllib2
from BeautifulSoup import BeautifulStoneSoup


log=list()

def cday(date):			#Day of the year
	return date.strftime('%j')

def tomonth(month):
	if month=='Jan': return 1
	if month=='Feb': return 2
	if month=='Mar': return 3
	if month=='Apr': return 4
	if month=='May': return 5
	if month=='Jun': return 6
	if month=='Jul': return 7
	if month=='Aug': return 8
	if month=='Sep': return 9
	if month=='Oct': return 10
	if month=='Nov': return 11
	if month=='Dec': return 12

	
BASE_URL = "http://weather.noaa.gov/pub/data/observations/metar/stations"
head=len('http://weather.noaa.gov/pub/data/observations/metar/stations/')-2
date=len('<img src="/icons/text.gif" alt="[TXT]"> <a href="ZYTX.TXT">ZYTX.TXT</a>                      ')

urlh = urllib.urlopen(BASE_URL)
now=datetime.datetime.now()
print str(now)
aux=dict()


for line in urlh:
	if len(line)==119:
		year=int(line[date+7:date+11])
		month=tomonth(line[date+3:date+6])
		day=int(line[date:date+2])
		hour=int(line[date+12:date+14])
		delta=now-datetime.datetime(year,month,day,hour,00)
		if delta.days < 1:
			aux[str(line[head:head+4])]= datetime.datetime(year,month,day,hour,00)
#update contiene metar stations y la [fecha hora] de la ultima actualizacion

home=os.getcwd()
f=open(home+'/Doc/stations.lib','r')
library = pickle.load(f)		#Dictionary of dictionaries with monitored stations
f.close()

for name in library:
	obs=''
	report=''
	goo={}
	station=library[name]
	print name
	if station['metar'] in aux:
		print 'New data for station'
		url = "%s/%s.TXT" % (BASE_URL, station['metar'])
		try:
			urlh = urllib.urlopen(url)
			for line in urlh:
				if line.startswith(station['metar']):			#Gets data from noaa server
					report = line.strip()
					obs = Metar.Metar(line)
		except :
			print "Error retrieving METAR: ",url,"\n"

	if report=='':												#No data, lets ask WUNDERGROUND
		print "No metar data for ",station['metar'],"\n"					#First parse station location to look for climate data
		city=str(station['city'] + ',' +station ['country'])
		print "Lets try %s \n"% city
		try:
			city = city.replace(' ', '%20')
			url = "http://api.wunderground.com/auto/wui/geo/WXCurrentObXML/index.xml?query=%s"%city
			page = urllib2.urlopen(url)
			soup = BeautifulStoneSoup(page)
			daytemp = soup.find("temp_c").string
			wind= soup.find("wind_mph").string
			wind=str(float(wind)*0.89)
			rh= soup.find("relative_humidity").string
			pressure= soup.find("pressure_mb").string
			dewpoint= soup.find("dewpoint_c").string
			#armar estructura de datos
			obs= "station:%s\n type: WUNDERGROUND \n time:--- \n temperature: %s\n dew point: %s\n wind: %s\n visibility: ---\n pressure:%s\n"%(station['code'],daytemp,dewpoint,wind,pressure)
			report=obs
		except:
			print "-------> Error in SOUP"
	if len(report)>10:		
		print "Data available"
		now=datetime.datetime.now()
		direct="%s/%s"%("/Stations",station['code'])
		current=home+direct
		if not os.path.exists(current):								#Creates Directory /Stations/XXXX (Satation ID)
			os.makedirs(current)
		entry_name=str(now.year)+str(cday(now))+str(now.hour)		#Creates filename
		if not os.path.isfile(current+'/'+entry_name):											#Creates file YYYYDDDHH		
			print 'Saving '+current+'/'+entry_name

			fil=open(current+'/'+entry_name, 'w')
			fil.writelines('Metar\n'+str(obs))
			fil.close
	else:
		print '############# No Data at all for %s #################' % (station['city'] + ' ' +station ['country'] + ':' + name + '\n' )
		log.append("%s"%(station['city'] + ' ' +station ['country'] + ':' + name + '\n' ))


print str(datetime.datetime.now())

f=open('getlog.txt','w')
f.writelines(log)
f.close()
