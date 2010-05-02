#! /usr/bin/env python


######################################################################################################################
#Recibe dos parametros: -run o -stop

#-run:
#	- inicia el servidor de consultas (ver Esquema  de servidores y servicios: peko.tk)
#	- comienza a tomar datos de centrales de acuerdo a lo especificado en dataserver.config
#	- ejecuta script de limpieza de archivos temporales delete_old_files de acuerdo a lo especificado en  dataserver.config

#-stop:
#	-revierte lo ejecutado en -run, no borra datos.
#######################################################################################################################

import os
import sys
from libraries.crontab import CronTab
import datetime



#Some defines
#Datos horarios de centrales
hourly_central='python get_report.py'
#Datos diarios de centrales
daily_central='python etoit.py'

def cday(date):			#Day of the year
	return date.strftime('%j')


def usage():			#Usage help
  program = os.path.basename(sys.argv[0])
  print "\nUsage: ",program,"<opt>"
  print """Options:
  -run		Start data server\n  -stop		Stop data server
"""
try:
	if sys.argv[1] == '-stop':
		print "stop"
		#	- detiene el servidor de consultas (ver Esquema  de servidores y servicios: peko.tk)
		#	- descronea datos de centrales
		tab = CronTab()
		lst = tab.find_command(hourly_central)
		xst = tab.find_command(daily_central)
		
		tab.crons.remove(lst[0])
		tab.crons.remove(xst[0])
		tab.write()
	
		#	- descronea script de limpieza


	elif sys.argv[1] == '-run':
		
		#	- inicia el servidor de consultas (ver Esquema  de servidores y servicios: peko.tk)
		#	- comienza a tomar datos de centrales de acuerdo a lo especificado en dataserver.config
		tab = CronTab()
		here=os.getcwd()
		now=datetime.datetime.now()
		entry_name=str(cday(now))+'-'+str(now.hour)+' '
		
		cron = tab.new(command='cd '+here+'/data-server/ && '+hourly_central, comment=entry_name+'By dataserver.py')
		cron2 = tab.new(command='cd '+here+'/data-server/ && '+daily_central, comment=entry_name+'By dataserver.py')
		
		cron.every_hour()
		cron2.every_day()
	
		tab.write()
	#	- ejecuta script de limpieza de archivos temporales delete_old_files de acuerdo a lo especificado en  	dataserver.config

	else:
		usage()

except:
	usage()





