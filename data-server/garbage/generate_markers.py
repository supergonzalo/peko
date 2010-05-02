import re, os

def todec(temp):
	temp=temp.split('-')
	print temp
	if temp[1][-1]=='N' or temp[1][-1]=='E':	
		mult=1.0
	else:
		mult=-1.0
	return mult*(float(temp[0])+float(re.findall(r'\d+\.\d+|\d+',temp[1])[0])/60.0)



# Lists Stations directory
def generate_markers(fo):
	html=''
	workdir="/home/aspire/Documentos/Codigopuwapi/Stations"
	datadir="/home/aspire/Documentos/Codigopuwapi/geodjango-googlemaps/application/templates/waypoints/"
	info_file="/home/aspire/Documentos/Codigopuwapi/Doc/METAR_Station_Places.txt"
	
	f = open(info_file, 'r')		
	temp=f.readlines()	
	f.close()
	data=os.listdir(workdir)
	for element in data:
		for i in range(len(temp)):
			if re.findall(element,temp[i]): 
				foo = temp[i].split(';')
				ref="%s"%(foo[0]+' '+foo[3][0:4])
				print ref
				lat=todec(foo[7])
				lon=todec(foo[8])
				html=html+"%s, %s, %s \n"%(lat,lon,ref)

	f = open(datadir+'markers.txt','w')		
	temp=f.write(html)	
	f.close()	
	return 

generate_markers(1)

