import os,pickle,re,math

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

def get_station(name,info_file):	#creates a dictionary with climate station info
	for i in range(len(lib)):
		if re.findall(name,lib[i]): 
			data = lib[i].split(';')
	if data[11]=='':
		altitude=10.0		#If there's no data at all we asume the station is @10m
	else:
		altitude=float(data[11])
	city1=data[3]
	city2=data[5]
	[latitude, hemisf,latrad]=convert(data[7])
	[longitude, medisf,longrad]=convert(data[8])
		
	return {'latitude':latitude ,'hemisf':hemisf, 'longitude':longitude, 'medisf': medisf,'latrad':latrad,'longrad':longrad, 'altitude':altitude,'city':city1,'country':city2,'code':name,'metar':name}


home=os.getcwd()	
os.chdir(home+'/../data-server/Doc/')
stations_to_check=list()
f=open ('countries.lib','r')
countries =f.read().split(',')
f.close()
g=open(info_file,'r')
lib=g.readlines()
g.close()
for each in range(len(countries)-1):
	print countries[each]
	for i in range(len(lib)):
		if re.findall(countries[each],lib[i]): 
			stations_to_check.append(lib[i][0:4])

tempo={}

for element in stations_to_check:
	tempo[element]=get_station(element,lib)

origen=tempo

#tempo tiene las estaciones con sus datosfrom operator import itemgetter
	
#crear array con todas las combinaciones
prototipo=['A','B','C','D','E','F','G','H','I','J','K','L','M']
dest=dict()
for uno in prototipo:
	for dos in prototipo:
		for tres in prototipo:
			for cuatro in prototipo:
				dest[str(uno+dos+tres+cuatro)]=list()

#copiar primero las lineas que si se corresponden al array
for element in origen:
	if element.isalpha():
		dest[element]=origen[element]

#mapear las que no se corresponden a los lugares libres
for item in origen:
	if not item.isalpha():
		print item
		newkey=first_empty(dest)
		dest[newkey]=origen[item]
		dest[newkey]['code']=newkey

tempo=dest.copy()
dest.clear()

for element in tempo:
	if tempo[element]:
		dest[element]=tempo[element]
		

f=open('stations.lib','w')
pickle.dump(dest,f)
f.close()
os.chdir(home)

os.chdir(home+'/../ui-server/public/')
f=open('abc.txt.test','w')
for element in tempo:
	f.write('%s,%s,%s:%s:%s;' % (tempo[element]['latitude'],tempo[element]['longitude'],tempo[element]['city'],tempo[element]['country'],tempo[element]['code'])) #last change
f.close()
os.chdir(home)

