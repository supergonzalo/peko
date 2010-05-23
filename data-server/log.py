#!/usr/bin/python

import os
import pickle,datetime,os

def cday(date):			#Day of the year
	return date.strftime('%j')

def init_log(logname):
	now=datetime.datetime.now()
	if os.path.isfile(logname):
		f=open(logname,'r')
		log=pickle.load(f)
		log[int(cday(now))]={now.hour:list()}
		f.close 
	else:
		
		log=dict()
		log[int(cday(now))]={now.hour:['Created %s hs' % now.hour]}
	return log

def printlog(message, datalog):
		now=datetime.datetime.now()
		datalog[int(cday(now))][now.hour].append(message)

def logcommit(log, logname):
	f=open(logname,'w')
	pickle.dump(log, f)
	f.close()



