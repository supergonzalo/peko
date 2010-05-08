#!/usr/bin/python

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

import rsm

import pickle


#Gets Weather Reports from stations given as a parameter (argv) and stores them in files
#../Stations/XXXX/YYYYDDDHH X=Station Identifier Y=Year D=Day of the year(1-365/366) H=Hour 
#Also creates ../Stations/XXXX/YYYYDDDIndex with period calculation of ETO due to wind activity
#On a changing day (or new station added) creates a '.dex' file where it appends ETO (windo, radiation, and total) for the #day. 

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

def get_last_Index(work):		#Returns last modified *.dex file in a directory "work"
	root = '.'
	os.chdir(work)
	date_file_list = []

	for folder in glob.glob(root):

		#print "folder =", folder
		for file in glob.glob(folder + '/*.dex'):
			stats = os.stat(file)
			lastmod_date = time.localtime(stats[8])
			date_file_tuple = lastmod_date, file
			date_file_list.append(date_file_tuple)
	date_file_list.sort()
	date_file_list.reverse() 	# newest mod date now first

	if date_file_list:
		return date_file_list[0][1]
	return '-1'

def present(filename):				#looks for a filename in a directory
	for file in os.listdir('./'):
		if fnmatch.fnmatch(filename,file):
		
			return True
	return False

def get_station(name,info_file):	#creates a dictionary with climate station info
	
	home=os.getcwd()		
	os.chdir(home+'/Doc')
	lib=arch(info_file,'r',0)
	for i in range(len(lib)):
		if re.findall(name,lib[i]): 
			data = lib[i].split(';')
	if data[11]=='':
		altitude=10.0	
	else:
		altitude=float(data[11])
	city=data[3]+','+data[5]
	temp=data[7].split('-')
	grad=float(temp[0])
	hemisf=temp[1][-1]
	minutes=float(re.findall('\d*',temp[1])[0])
	os.chdir(home)
	return {'latitude':grad+minutes/60,'hemisf':hemisf,'altitude':altitude,'city':city,'code':name}


def etoit(station,dayofyear):

	info=['','','','','','','','','','','','','','','','','','','','','','','','']
		
	for i in range (24):
		if os.path.isfile(dayofyear+str(i)):
			observation=arch(dayofyear+str(i), 'r',0)
			if len(observation[1])>5 or len(observation[3])>5: #there's data in the file
				info[i]="\nTimestamp: "+str(i)+ etowind20.etowind(observation,station)
	
		
	dex=dayofyear+'.dex'
	if os.path.isfile(dex):
		os.remove(dex)
	for i in range (len(info)):
		arch(dex,'a',info[i])				#Cambiar para que no acceda al archivo pro cadda linea!
	dexinfo=arch(dex,'r',0)

	if not len(dexinfo)==0:
		arch(dex,'a',etrad10.etorad(dexinfo,station,dex))	#writes timestamp
				#para poder llamar a addto limpiar la parte del dex que corresponde al ultimo reporte
				#rsm.addto_rsm(stationcode,dexinfo)
				



############################# RUN ############################################################


os.chdir('./Doc')
f=open('stations.lib','r')
library = pickle.load(f)					#Dictionary of dictionaries with monitored stations
f.close()
os.chdir('..')


for element in library:
	print '@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@'
	print element
	print '@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@'
	
	direct="%s/%s"%("Stations",element)
	home=os.getcwd()
	if os.path.exists(direct):			#Changes to Directory /Stations/XXXX (Station ID)
		os.chdir(direct)

	for item in os.listdir('.'):
		if item[-4:] != '.dex' or item[-4:] != '.rsm':	#is not an index file
			buff={}
			if item[0:7] not in buff:	#that day havent been indexed
				if 1:					#range to index, 1 alldir
					buff[item[0:7]]=1
					etoit(library[element],item[0:7])
		else:
			print "No data for station"
	
	os.chdir(home)
	
			



