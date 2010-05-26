#! /usr/bin/env python

from operator import itemgetter

def first_empty(dicc):
	for k in dicc:
		if dicc[k]==[]:
			return k

metar='METAR_Station_Places.txt'
testfile='test.txt'
#Leer archivo de origen
f=open(metar,'r')
origen=f.readlines()
f.close()
	
#crear array con todas las combinaciones
prototipo=['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','W','X','Y','Z']
dest=dict()
for uno in prototipo:
	for dos in prototipo:
		for tres in prototipo:
			for cuatro in prototipo:
				dest[str(uno+dos+tres+cuatro)]=list()

#copiar primero las lineas que si se corresponden al array
for i in range(len(origen)):
	if origen[i].split(';')[0] in dest:
		dest[origen[i].split(';')[0]]=origen[i]
		

#mapear las que no se corresponden a los lugares libres
for i in range(len(origen)):
	if origen[i].split(';')[0] not in dest:
		newkey=first_empty(dest)
		dest[newkey]=newkey+origen[i][4:]
		

#guardar el array en el archivo con el formato requerido
items = dest.items()
items.sort(key = itemgetter(1))

f=open(metar,'w')
for k in dest:
		if dest[k]!=[]: 
			f.write(dest[k])
f.close()

