import os,pickle,re,math,sys

info_file= 'METAR.txt'

def convert(data):
	mult=1
	temp=data.split('-')
	grad=float(temp[0])
	hemisf=temp[1][-1]
	if hemisf == 'W' or hemisf=='S':
		mult=float(-1.0)
	minutes=float(re.findall('\d*',temp[1])[0])
	return [mult*(grad+minutes/60.0), hemisf,mult*(grad+minutes/60.0)*math.pi/180.0]

def first_empty(dicc):
	for k in dicc:
		if dicc[k]==[]:
			return k

def get_station(line):	#creates a dictionary with climate station info
	data = line.split(';')
	if data[11]=='':
		altitude=10.0		#If there's no data at all we asume the station is @10m
	else:
		altitude=float(data[11])
	city1=data[3]
	city2=data[5]
	[latitude, hemisf,latrad]=convert(data[7])
	[longitude, medisf,longrad]=convert(data[8])
	name=line[0:4]
	metar=data[14][0:4]
	factor=float(data[15])	
	return {'latitude':latitude ,'hemisf':hemisf, 'longitude':longitude, 'medisf': medisf,'latrad':latrad,'longrad':longrad, 'altitude':altitude,'city':city1,'country':city2,'code':name,'metar':metar,'factor':factor}


home=os.getcwd()
sys.path.append(home+'/../data-server/')
import pywapi	
os.chdir(home+'/../data-server/Doc')
stations_to_check=dict()
f=open ('countries.lib','r')
countries =f.read().split(',')
f.close()
g=open(info_file,'r')
a=g.readlines()
g.close()
count=dict()
toabc=list()
for i in range(len(a)):
	try:
		count[a[i].split(';')[5]].append(a[i])
	except:
		count[a[i].split(';')[5]]=list()
		count[a[i].split(';')[5]].append(a[i])
		
#count es un diccionario de listas por paises

for each in range(len(countries)-1):
		
	for i in range(len(count[countries[each]])):
		try:
			station_data=get_station(count[countries[each]][i])
			stations_to_check[station_data['code']]=station_data
		except:
			print "Error in %s :%s" % (countries[each],station_data)
#Guardar stations.lib
f=open('stations.lib','w')
pickle.dump(stations_to_check,f)
f.close()


