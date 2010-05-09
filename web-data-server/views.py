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

###########################################################################################Ultimo cambio, testear
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
	xml=''
	f = open(info_file, 'r')		
	#temp=f.readlines()	
	temp=pickle.load(f)
	f.close()

	if output == 'x':				#Generates xml output

<marker lat="43.65654" lng="-79.90138" label="Marker One">
      <infowindow>Some stuff to display in the&lt;br&gt;First Info Window</infowindow>
     </marker>

		for element in temp:
			ref="%s. %s" % (temp[element]['city'],temp[element]['country'])
			xml=xml+"<marker lat=\"%s\" lng=\"%s\" label=\"%s\" > <infowindow> html=\"%s\" </infowindow> </marker>"%(temp[element]['latitude'], temp[element]['longitude'], ref, temp[element]['code'])
		html="<markers> %s </markers>" % xml

	else:
		for element in temp:
			ref="%s. %s" % (temp[element]['city'],temp[element]['country'])
			html=html+"<p><a href=%s>%s</a> %s lat=%s lng=%s</p>"%(temp[element]['code'], temp[element]['code'],ref,temp[element]['latitude'],temp[element]['longitude'])
		html = "<html><body> %s </body></html>" %(html)

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
	data=''
	
	if os.path.exists(station_dir):			
		os.chdir(station_dir)

	rsm=str(station+'.rsm')
	if os.path.isfile(rsm):
		f = open(rsm, 'r')		
		temp=f.readlines()	
		f.close()

		for element in temp:
			data=data+"<p>%s</p>"%(element)
	else:
		data= "No data"	
	os.chdir(home)
	html = "<html><body><p>%s</body></html>" % (data)
	return HttpResponse(html)


