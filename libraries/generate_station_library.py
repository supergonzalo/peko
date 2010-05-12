import os,pickle,re

info_file= 'METAR_Station_Places.txt'

def convert(data):
	mult=1
	temp=data.split('-')
	grad=float(temp[0])
	hemisf=temp[1][-1]
	if hemisf == 'W' or hemisf=='S':
		mult=float(-1.0)
	minutes=float(re.findall('\d*',temp[1])[0])
	return [mult*(grad+minutes/60.0), hemisf]

def get_station(name,info_file):	#creates a dictionary with climate station info

	g=open(info_file,'r')
	lib=g.readlines()
	g.close()
	for i in range(len(lib)):
		if re.findall(name,lib[i]): 
			data = lib[i].split(';')
	if data[11]=='':
		altitude=10.0		#If there's no data at all we asume the station is @10m
	else:
		altitude=float(data[11])
	city1=data[3]
	city2=data[5]
	[latitude, hemisf]=convert(data[7])
	[longitude, medisf]=convert(data[8])
	
	return {'latitude':latitude ,'hemisf':hemisf, 'longitude':longitude, 'medisf': medisf, 'altitude':altitude,'city':city1,'country':city2,'code':name}


home=os.getcwd()	
stations_to_check=['LERI', 'LELC', 'LEAS', 'LELL', 'LERT', 'LEVX', 'LEBZ', 'LEZA', 'GCLP', 'LEAM', 'LEZG', 'LETO', 'LEGA', 'EGCC', 'LEBA', 'LEAL', 'LEVS', 'GCLA', 'LEMG', 'LEHI', 'GCFV', 'LEJR', 'LEGE', 'LEMD', 'LELN', 'LEGT', 'EQYR', 'LFAT', 'LELO', 'LEBB', 'AGGH', 'LEXJ', 'LERS', 'LEIB', 'LEVC', 'LEBG', 'LEMH', 'LECH', 'GCXO', 'LEMO', 'LEST', 'LESA', 'LEVD', 'LEPA', 'GCRR', 'GCHI', 'LECV', 'LEVT', 'GCTS', 'SABA', 'LESO', 'LEZL', 'GEML', 'LEGR', 'LEPP', 'LEAB', 'LEBL', 'LECO']
os.chdir(home+'/../data-server/Doc/')


tempo={}

for element in stations_to_check:
	tempo[element]=get_station(element,info_file)

f=open('stations.lib','w')
pickle.dump(tempo,f)
f.close()
os.chdir(home)

os.chdir(home+'/../ui-server/public/')
f=open('abc.txt','w')
for element in tempo:
	f.write('%s,%s,%s,%s;' % (tempo[element]['latitude'],tempo[element]['longitude'],tempo[element]['city'],tempo[element]['country']))
f.close()
os.chdir(home)


