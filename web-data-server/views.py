from django.http import HttpResponse
import datetime
import time, os, glob,re,pickle


here=os.getcwd()
os.chdir('../')
f=open('config.txt','r')
config=pickle.load(f)
f.close
os.chdir(here)

workdir=config["WORKDIR"]+"/data-server/Stations"
info_file=config["WORKDIR"]+"/data-server/Doc/stations.lib"
dex_xpire=int(config["DEX_FILES_EXPIRE"])

def cday():
	now = datetime.datetime.now()
	return now.strftime('%j')

# Prints current day of the year
def current_datetime(request):
	html = "<html><body>Today is day %s.</body></html>" % cday()
	return HttpResponse(html)


#Sorts .dex files
def put_some_order(folder):
	date_file_list=[]
	for file in glob.glob(folder + '*.dex'):
		stats = os.stat(file)
		lastmod_date = time.localtime(stats[8])
		date_file_tuple = file, lastmod_date
		date_file_list.append(date_file_tuple)
	date_file_list.sort()
	date_file_list.reverse() 	# newest mod date now first

	if date_file_list:
		return date_file_list
	return '-1'

# Lists .dex files available in a STATION directory 
def station_data_available(request, format,offset,prev):
	
	home=os.getcwd()
	station_dir="%s/%s/"%(workdir,offset[0:4])
	data=''
	
	if os.path.exists(station_dir):			
		os.chdir(station_dir)
		dex_files=put_some_order('./')
		if dex_files == '-1':
			
			data='No .dex info for station'
		else:
			if prev:
				prev=int(prev)
			else:
				prev=len(dex_files)
			if prev <=0:		#Some parsing of the input data, just in case
				prev =1
			if prev >= dex_xpire:
				prev=dex_xpire
			if prev >= len(dex_files):
				prev=len(dex_files)
			for element in range(prev):
				data=data+"<p><a href=%s>%s</a></p>"%(dex_files[element][0],dex_files[element][0])
		
	else:
		data= "No data for station"	
	os.chdir(home)

	html = "<html><body> %s </body></html>" % (data)
	return HttpResponse(html)

# Lists Stations directories
def list_stations(request,output='h'):
	
	html=''
	xml='<?xml version=\"1.0\" encoding=\"UTF-8\" standalone=\"yes\"?>'
	f = open(info_file, 'r')		
	#temp=f.readlines()	
	temp=pickle.load(f)
	f.close()


	if output == 'x':                               #Generates xml output

		for element in temp:
			ref="%s. %s" % (temp[element]['city'],temp[element]['country'])
			xml=xml+"<marker lat=\"%s\" lng=\"%s\" label=\"%s\" html=\"%s\" />"%(temp[element]['latitude'], temp[element]['latitude'],ref,temp[element]['latitude'])
		html="<markers> %s </markers>" % xml
		html=xml

	elif output == 'h':
		for element in temp:
			ref="%s. %s" % (temp[element]['city'],temp[element]['country'])
			html=html+"<p><a href=%s>%s</a> %s lat=%s lng=%s</p>"%(temp[element]['code'], temp[element]['code'],ref,temp[element]['latitude'],temp[element]['longitude'])
		html = "<html><body> %s </body></html>" %(html)

	elif output == 't':
		for element in temp:
			ref="%s. %s" % (temp[element]['city'],temp[element]['country'])
			xml=xml+"%s,%s,%s;<br>\n" % (temp[element]['latitude'],temp[element]['longitude'],ref)
                #html="<markers> %s </markers>" % xml
		html=xml


	return HttpResponse(html)


def publish_data(request,format,station,xxx,filename):

	home=os.getcwd()
	station_dir="%s/%s"%(workdir,station[0:4])
	data=''
	
	if os.path.exists(station_dir):			
		os.chdir(station_dir)

	dex=str(filename+'.dex')
	if os.path.isfile(dex):
		f = open(dex, 'r')		
		temp=f.readlines()	
		f.close()

		for element in temp:
			data=data+"<p>%s</p>"%(element)
	else:
		data= "No data"	
	os.chdir(home)


	html = "<html><body> %s </body></html>" % (data)
	return HttpResponse(html)

def rsm_data(request,format, station,xxx):
	home=os.getcwd()
	station=station[0:4]
	station_dir="%s/%s"%(workdir,station)
	data='<table border="1" width="100%"><tr><td align="center">Actualizado<td align="center">Consumo de agua/dia<td align="center">Temperatura media/dia<td align="center">Viento medio/dia</tr>'
	
	if os.path.exists(station_dir):			
		os.chdir(station_dir)

	rsm=str(station+'.rsm')
	if os.path.isfile(rsm):
		f = open(rsm, 'r')		
		temp=pickle.load(f)	
		f.close()
		digits=5
		#for element in temp['index']:
		element = temp['index'][0]	
		data=data+'<tr><td align="center">Hace %s dias<td align="center"> %s mm <td align="center"> %s C <td align="center"> %s m/s</tr>'%(str(int(cday())-int(temp[element]['DayNumber']))[0:digits],temp[element]['ETOTODAY'][0:digits],temp[element]['TempMed'][0:digits],temp[element]['WindMed'][0:digits])
		cant=0
		teto=0
		ttemp=0
		twind=0
		for element in temp['index']:
			average=int(cday())-int(temp[element]['DayNumber'])
			if average<7:
				cant=cant+1
				teto=teto+float(temp[element]['ETOTODAY'])
				ttemp=ttemp+float(temp[element]['TempMed'])
				twind=twind+float(temp[element]['WindMed'])
		
		teto=str(teto/cant)
		ttemp=str(ttemp/cant)
		twind=str(twind/cant)
		data=data+'<tr><td align="center">Media de 7 dias<td align="center"> %s mm <td align="center"> %s C <td align="center"> %s m/s</tr></table><br>'%(teto[0:digits],ttemp[0:digits],twind[0:digits])
		
					
	else:
		data= "No data"	
	os.chdir(home)
	data=data+'<table width=100%><tr><td align="center" width="20%">Datos de la central:</td><td align="left">'
	data=data+station
	data=data+' </td><td align="center" title="Denunciar una central que no funciona bien"><a href="http://peko.tk/index.html">Votar negativo</a><td align="center" title="Crear un programa de riego para mi parcela"><a href="href="http://peko.tk/index.html">Programa de Riego Avanzado</a><td></div>'	

	html = "<html><body>%s</body></html>" % (data)
	return HttpResponse(html)

def raw(request,format, station,xxx):
	home=os.getcwd()
	station=station[0:4]
	station_dir="%s/%s"%(workdir,station)
	data=''
	
	if os.path.exists(station_dir):			
		os.chdir(station_dir)

	rsm=str(station+'.rsm')
	if os.path.isfile(rsm):
		f = open(rsm, 'r')		
		resumen=f.readlines()	
		f.close()

		for element in resumen:
			data=data+"<p>%s</p>"%(element)			#############################

	#levanta los valores del cache para los ultimos 7 dias
	#Calcula para la ultima semana los valores de tmax tmin windmedio y eto media 	
	#Copia al array resultado los valores solicitados
	else:
		data= "No tenemos suficientes datos de la estacion"	

	os.chdir(home)
	html = "<html><body><p>%s</body></html>" % (data)
# Devuelve el valor formateado
	return HttpResponse(html)



def test(request,format, station,xxx):

	import random
	from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
	from matplotlib.figure import Figure
	from matplotlib.dates import DateFormatter
	home=os.getcwd()
	station=station[0:4]
	station_dir="%s/%s"%(workdir,station)
	if os.path.exists(station_dir):			
		os.chdir(station_dir)

	rsm=str(station+'.rsm')
	if os.path.isfile(rsm):
		f = open(rsm, 'r')		
		temp=pickle.load(f)	
		f.close()
	
	element = temp['index'][0]
	fig=Figure(figsize=(6,3))
	ax=fig.add_subplot(111)
	x=[]
	y=[]
	now=datetime.datetime.now()
	delta=datetime.timedelta(days=1)
	for element in temp['index']:
		average=int(cday())-int(temp[element]['DayNumber'])
		if average<7:
			x.append(now-datetime.timedelta(days=average))
			y.append(float(temp[element]['ETOTODAY']))
				
		else:
			break

	ax.plot_date(x, y, '-')
	ax.xaxis.set_major_formatter(DateFormatter('%Y-%m-%d'))
	fig.autofmt_xdate()
	canvas=FigureCanvas(fig)
	response=HttpResponse(content_type='image/png')
	canvas.print_png(response)

	return response




