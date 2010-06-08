from django.http import HttpResponse
import datetime
import time, os, glob,re,pickle
from operator import itemgetter, attrgetter
from matplotlib.pyplot import axhline
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib.dates import DateFormatter


here=os.getcwd()
os.chdir('../')
f=open('config.txt','r')
config=pickle.load(f)
f.close
os.chdir(here)

workdir=config["WORKDIR"]+"/data-server/Stations"
info_file=config["WORKDIR"]+"/data-server/Doc/stations.lib"
dex_xpire=int(config["DEX_FILES_EXPIRE"])

f = open(info_file, 'r')		
temp=pickle.load(f)
f.close()


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

def test(request,format, station,xxx):
	home=os.getcwd()
	station=station[0:4]
	station_dir="%s/%s"%(workdir,station)
	if os.path.exists(station_dir):			
		os.chdir(station_dir)
	rsm=str(station+'.rsm')
	data=''
	if format=='h':
		data='<table border="1" width="100%"><tr><td align="center">Actualizado<td align="center">Consumo de agua/dia<td align="center">Temperatura media/dia<td align="center">Viento medio/dia</tr>'
			
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
					cant=cant+1.0
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
		#data='</td></table></div>'	
	
	elif format=='c':
		if os.path.isfile(rsm):
			f = open(rsm, 'r')		
			temp=pickle.load(f)	
			f.close()
			data='Dia del ano,eto del dia, temp media del dia, viento medio del dia;'
			for element in temp['index']:
				data+='%s,%s,%s,%s;' % (temp[element]['DayNumber'],temp[element]['ETOTODAY'],temp[element]['TempMed'],temp[element]['WindMed'])
		
	html = "<html><body>%s</body></html>" % (data)
	return HttpResponse(html)

def raw(request,format, station,xxx):
	home=os.getcwd()
	station=station[0:4]
	station_dir="%s/%s/"%(workdir,station)
	data=''
	
	rsm=str(station+'.rsm')
	try:
		f = open(station_dir+rsm, 'r')		
		temp=pickle.load(f)	
		f.close()
	
		element = temp['index'][0]
	
		for element in temp['index']:
			add="Dia,%s,"% temp[element]['DayNumber']
			try:
				add=add+"Eto,%s,Tmedia,%s,Wind,%s,"%(temp[element]['ETOTODAY'],temp[element]['TempMed'],temp[element]['WindMed'])	
			except:
				add=add+"No data"
		
			if format=='h':
				add="<p>"+add+"</p>"
			
			data+=add

	except:
		data= "No hay datos"	

	os.chdir(home)
	html = "<html><body><p>%s</body></html>" % (data)
# Devuelve el valor formateado
	return HttpResponse(html)

def rsm_data(request,format, station,xxx):

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
		fig=Figure(figsize=(9,3),facecolor='w', edgecolor='w')

		ax=fig.add_subplot(111)

		x=[]
		y=[]
		z=[]
		t=[]
		now=datetime.datetime.now()
		delta=datetime.timedelta(days=1)
		teto=0
		ttemp=0
		twind=0
		cant=0

		for element in temp['index']:
			average=int(cday())-int(temp[element]['DayNumber'])
			if average<8:
				x.append(now-datetime.timedelta(days=average))
				try:
					eto=float(temp[element]['ETOTODAY'])
					cant+=1.0
				except:
					eto=0
				y.append(eto)
				teto=teto+float(eto)

				#z.append(float(temp[element]['TempMed']))
				#t.append(float(temp[element]['WindMed']))
				#ttemp=ttemp+float(temp[element]['TempMed'])
				#twind=twind+float(temp[element]['WindMed'])
					
			else:
				break
		x.pop(0)
		y.pop(0)
		width=1
		try:
			teto=teto/cant
		except:
			teto=0		
		#ttemp=ttemp/cant
		#twind=twind/cant
		ax.set_ylabel('Evapo. mm',color='blue')
		ax.plot_date(x, [teto]*len(x), '-',color='green')
		ax.bar(x,y,width,alpha=0.5,color='blue')
		ax.xaxis.set_major_formatter(DateFormatter('%Y-%m-%d'))

		fig.autofmt_xdate()
		canvas=FigureCanvas(fig)
		response=HttpResponse(content_type='image/png')
		canvas.print_png(response)
	else:
		response= HttpResponse("<html><body><p>No data<br></body></html>")

	os.chdir(home)
	
	return response

def manh_distance(lat1,long1,lat2,long2):
	return (lat1-lat2)**2+(long1-long2)**2

def near(request,format, lat,longitud):
	
	base=[float(lat),float(longitud)]
	sorted_list=list()
	for element in temp:
			sorted_list.append([element,manh_distance(base[0],base[1],float(temp[element]['latitude']),float(temp[element]['longitude']))])
	result=sorted(sorted_list, key=itemgetter(1))
	ordenada=''
	for i in range(100):
		ordenada=ordenada+"<p>%s,%s,%s:%s:%s;</p>"%(temp[result[i][0]]['latitude'],temp[result[i][0]]['longitude'],temp[result[i][0]]['city'],temp[result[i][0]]['country'],temp[result[i][0]]['code'])
				
	return HttpResponse("<div id='ifrmTest'>%s</div>"% ordenada)

