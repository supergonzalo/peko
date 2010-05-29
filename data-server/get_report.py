#!/usr/bin/python
#
import os
import sys
import getopt
import string
import urllib
import datetime
import etrad10
import re
import fnmatch
import glob,time
import pywapi
import pprint
from metar import Metar
import etowind20
import pickle



#Gets Weather Reports from stations given as a parameter (argv) and stores them in files
#../Stations/XXXX/YYYYDDDHH X=Station Identifier Y=Year D=Day of the year(1-365/366) H=Hour 

BASE_URL = "http://weather.noaa.gov/pub/data/observations/metar/stations"

def cday(date):			#Day of the year
	return date.strftime('%j')

def gparser (city):	#Gets weather from google in case station is not working
	
	try:
		result=pywapi.get_weather_from_google(city)
		
	except:
		print '\nNo data for'+ city
		result =0

	return result


def arch(filename, mode, data=0):
	f = open(filename, mode)		#Writes / reads filename. In a 'r', data is a dummy
	if mode=='r' or mode=='r+':
		temp=f.readlines()	
	else:
		f.write(data)
		temp=True
	f.close()	
	return temp


def usage():			#Usage help
  program = os.path.basename(sys.argv[0])
  print "Usage: ",program,"<city> [ <city> ... ]"
  print """Options:
  <city> . Station code, ex 'LELC'
"""
  sys.exit(1)

stations = []
debug = False

try:
  opts, stations = getopt.getopt(sys.argv[1:], 'd')
  for opt in opts:
    if opt[0] == '-d':
      debug = True
except:
  usage()
 
if not stations:
	home=os.getcwd()		
	os.chdir(home+'/Doc')
	f=open('stations.lib','r')
	library = pickle.load(f)		#Dictionary of dictionaries with monitored stations
	f.close()
	os.chdir(home)

for name in library:
	print name
	obs=''
	report=''
	goo={'current_conditions':''}
	#station=get_station(name,'METAR_Station_Places.txt')		#Climatic station dictionary, downloaded from noaa
	station=library[name]
 	home=os.getcwd()
	url = "%s/%s.TXT" % (BASE_URL, station['code'])
	try:
		urlh = urllib.urlopen(url)
		for line in urlh:
      			if line.startswith(name):			#Gets data from noaa server
       				report = line.strip()
        			obs = Metar.Metar(line)
		
		if report=='':												#No data, lets ask google
			print "No metar data for ",name,"\n\n"					#First parse station location to look for climate data
			goo=gparser(station['city'] + ',' +station ['country'] )
					
		if len(goo['current_conditions'])!=0 or len (report)!=0:		#If theres something to log
			now=datetime.datetime.now()
			direct="%s/%s"%("Stations",station['code'])
			if not os.path.exists(direct):								#Creates Directory /Stations/XXXX (Satation ID)
    				os.makedirs(direct)
			os.chdir(direct)

			entry_name=str(now.year)+str(cday(now))+str(now.hour)		#Creates filename
			if not os.path.isfile(entry_name):											#Creates file YYYYDDDHH		
				arch(entry_name, 'w', 'Metar\n'+str(obs)+'\nGoogle\n' + str(goo))
						
			os.chdir(home)
		else:
			print '############# No Data #################'
		
		
	except Metar.ParserError, err:
		print "METAR code: ",line
    		print string.join(err.args,", "),"\n"
    		os.chdir(home)
  	except:
    		print "Error retrieving",name,"data","\n"
    		os.chdir(home)


	
   	

