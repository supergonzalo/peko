from django.http import HttpResponse
import datetime
import os, glob,re


# Prints current day of the year
def current_datetime(request):
	now = datetime.datetime.now()
	html = "<html><body>Today is day %s.</body></html>" % now.strftime('%j')
	return HttpResponse(html)

# Lists .dex files available in a STATION directory 
def station_data_available(request, offset):

	home=os.getcwd()
	workdir="/home/aspire/Documentos/Codigopuwapi/Stations"
	station_dir="%s/%s"%(workdir,offset)
	data=''
	
	if os.path.exists(station_dir):			
		os.chdir(station_dir)
		for file in glob.glob('./*.dex'):
			data=data+"<p><a href=%s>%s</a></p>"%(file, file)
	else:
		data= "No data for station"	
	os.chdir(home)

	html = "<html><body> %s </body></html>" % (data)
	return HttpResponse(html)

# Lists Stations directories
def list_stations(request):
	html=''
	workdir="/home/aspire/Documentos/Codigopuwapi/Stations"
	info_file="/home/aspire/Documentos/Codigopuwapi/Doc/METAR_Station_Places.txt"
	f = open(info_file, 'r')		
	temp=f.readlines()	
	f.close()

	data=os.listdir(workdir)
	
	for element in data:

		for i in range(len(temp)):
			if re.findall(element,temp[i]): 
				foo = temp[i].split(';')
		ref=" %s, %s"%(foo[3],foo[5])


		html=html+"<p><a href=%s>%s</a>%s</p>"%(element, element,ref)
		
	html = "<html><body> %s </body></html>" %(html)
	return HttpResponse(html)


def publish_data(request,station,filename):


	home=os.getcwd()
	workdir="/home/aspire/Documentos/Codigopuwapi/Stations"
	station_dir="%s/%s"%(workdir,station)
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


