#!/usr/bin/python

from __future__ import with_statement
import os, re, glob, pickle

def create_rsm(station):
	rsm=station[0:4]+'.rsm'
	print '\n Indexing %s' % str(station)	#Buscar todos los .dex
	index=dict()
	date_file_list=list()
	for file in glob.glob('*.dex'):				
		date_file_list.append(file)
																				#Index = [.dex] ordenada backwards
	date_file_list.sort()
	date_file_list.reverse()
	index['index']=date_file_list
																				#Para index[.dex] -> dict[yyyyddd]=[resumen del dia].split
	for element in date_file_list:
		eto=dict()
		eto['DayNumber']=element[4:7]
		with open(element, "r") as f:
			f.seek (0, 2)           					# Seek @ EOF
			fsize = f.tell()       					 	# Get Size
			f.seek (max (fsize-1024, 0), 0) 	# Set pos @ last n chars
			lines = f.readlines()       			# Read to end
		lines = lines[-10:]    							# Get last 10 lines
		findstr=['ETO WindTODAY','ETOradTODAY','ETOTODAY','Estimada','TempMax','TempMin','TempMed','WindMed']
		for line in lines:
			for item in findstr:
				if item in line:
					eto[item]=line.split(':')[1]

		index[element]=eto
	print len(index)															
	f=open(rsm,'w')#wirte XXXX.rsm 
	pickle.dump(index,f)
	f.close()



#if True:
#	home=os.getcwd()
#	os.chdir('Stations')
#	centrals=os.listdir('.')
	
#	for station in centrals:						#Para estacion en stations.lib Entrar en dir
#		os.chdir(station)
#	print os.getcwd()
#		create_rsm(station)
#		os.chdir('..')
#	os.chdir(home)


