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
daily_cleanup='python delete_old_files.py'


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
		print "data-server STOPPING!!!!!!!!!!!!"

		# DESCRONEAR data-server.py -run @reboot

		#	- detiene el servidor de consultas (ver Esquema  de servidores y servicios: peko.tk)

		#detener ejecucion de server.py

		#	- descronea datos de centrales
		tab = CronTab()
		#lst = tab.find_command(hourly_central)
		#xst = tab.find_command(daily_central)
		#yst = tab.find_command(index)
		
		tab.remove_all(hourly_central)
		tab.remove_all(daily_central)
		tab.remove_all(daily_cleanup)
		#tab.remove_all(index)
		tab.write()
	
		#	- descronea script de limpieza


	elif sys.argv[1] == '-run':

		print "data-server STARTING!!!!!!!!!!!!"

		# CRONEAR data-server.py -run @reboot
		

		#	- inicia el servidor de consultas (ver Esquema  de servidores y servicios: peko.tk)

		#########Como ejecutar .py?????

		#	- comienza a tomar datos de centrales de acuerdo a lo especificado en dataserver.config
		tab = CronTab()
		here=os.getcwd()
		now=datetime.datetime.now()
		entry_name=str(cday(now))+'-'+str(now.hour)+' '
		
		cron = tab.new(command='cd '+here+'/data-server/ && '+hourly_central+'> last_hourly.txt', comment=entry_name+'By dataserver.py')
		cron2 = tab.new(command='cd '+here+'/data-server/ && '+daily_central+'> last_daily.txt', comment=entry_name+'By dataserver.py')
		cron3 = tab.new(command='cd '+here+'/data-server/ && '+daily_cleanup+'> last_cleanup.txt', comment=entry_name+'By dataserver.py')
		
		cron.every_hour()
		cron2.special = '45 3 * * *'
		cron3.special = '55 6 * * *'
	
		tab.write()
	#	- ejecuta script de limpieza de archivos temporales delete_old_files de acuerdo a lo especificado en config.txt

	#	cronear delete_old_files

	else:
		usage()

except:
	usage()





