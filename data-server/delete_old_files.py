#!/usr/bin/python

import os, re, glob, pickle, datetime

def clear(station,age):
	now=datetime.datetime.now()
	thres=str(int(now.strftime('%j'))-age)
	thres=str(now.year)+thres
	rsm=str(station+'.rsm')
	direct=os.listdir('.')
	for file in direct:
		if file != rsm:
			if file not in glob.glob('*.dex'):
				if file[0:7]<thres:
					os.remove(file)

			


if True:
	home=os.getcwd()
	f=open('../config.txt','r')
	conf=pickle.load(f)
	f.close
	age_tempo=int(conf["TEMP_FILES_XPIRE"])	
	os.chdir(home+'/Stations')
	centrals=os.listdir('.')
	for station in centrals:						#Para estacion en stations.lib Entrar en dir
		os.chdir(station)
		#print os.getcwd()
		clear(station,age_tempo)
		os.chdir('..')
	os.chdir(home)


