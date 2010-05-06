#!/usr/bin/python

from __future__ import with_statement
import os, re, glob


def addto_rsm(station,dexinfo):						#Adds dexinfo to the top of station.rsm, if file does not exist it creates it
	#print 'dexinfo#####################\n'
	#print dexinfo
	rsm=station+'.rsm'
	temp=''
	if os.path.isfile(rsm):
		f=open(rsm,'r')
		temp=f.readlines()
		f.close()
	f=open(rsm,'w')
	f.writelines(dexinfo)
	f.writelines(temp)
	f.close()

def create_rsm(station):			#Creates .rsm file for a directory '.', if exists deletes the previous one
	date_file_list=[]
	rsm=station[0:4]+'.rsm'
#Reindex .dex files, delete old rsm file
	if os.path.isfile(rsm):
		f=open(rsm,'w')
		f.write('')
		f.close()
	for file in glob.glob('*.dex'):				#reverse order
		date_file_list.append(file)
	date_file_list.sort()
	#date_file_list.reverse() 							# newest mod date now first
	for element in date_file_list:
		eto=element+'\n'
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
					eto=eto+line
			
			#print element
			#print eto
		addto_rsm(station,eto+'\n')	#Write footer to .rsm


def reindex(directory):

	home=os.getcwd()
	os.chdir(directory)
	centrals=os.listdir('.')

	for station in centrals:
		os.chdir(station)
		print os.getcwd()
		create_rsm(station)
		os.chdir('..')
	os.chdir(home)
				
reindex('Stations')


