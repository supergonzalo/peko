#!/usr/bin/python

import os
import pickle,datetime,os

def cday(date):			#Day of the year
	return date.strftime('%j')

def init_log(logname):
	log=list()
	return log

def printlog(message, datalog):
		datalog.append(message)

def logcommit(log, logname):
	now=datetime.datetime.now()
	if os.path.isfile(logname):
		f=open(logname,'r')
		old=pickle.load(f)
		f.close()
	else:
		old=dict()
	if not old.has_key(cday(now)):
		old[cday(now)]=dict()

	if not old[cday(now)].has_key(now.hour):
		old[cday(now)][now.hour]=list()
	old[cday(now)][now.hour].extend(log)

	f=open(logname,'w')
	pickle.dump(old,f)
	f.close()

