#!/usr/bin/python

# Operaciones sobre la libreria general de estaciones

import os, array, sys

info_file= 'METAR_Station_Places.txt'

def init_lib():
	home=os.getcwd()	
	os.chdir(home+'/../data-server/Doc/')
	g=open(info_file,'r')
	lib=g.readlines()
	g.close()
	return lib

def find_code(a, x, lo=0, hi=None):
#"""Ordena la lista de centrales basado en los primeros 4 caracteres (code)"""
	if hi is None:
		hi = len(a)
	while lo < hi:
		mid = (lo+hi)//2
		midval = a[mid]
		if midval[0:4] < x:
			lo = mid+1
		elif midval[0:4] > x: 
			hi = mid
		else:
			return mid
	return -1
	
def baja(array,code):
	index=find_code(array,code)
	if index != -1:
		array.remove(lib[index])
	else:
		print 'No se encontro'
	return


def alta(lib,code,location,country,latitude,longitude,altitude):
	index=find_code(lib,code)
	if index != -1:
		answer=raw_input("El codigo se ha encontrado, ovewwrite?")
		if answer != 'yes':
			return -1
		else:
			baja(lib,code)

	newline='%s;--;---;%s;;%s;5;%s;%s;;;%s;;\n' % (code,location,country,latitude,longitude,altitude)
	lib.append(newline)
	lib.sort()

def mod(lib,code,location,country,latitude,longitude,altitude):
	index=find_code(lib,code)
	if index != -1:
		newline='%s;--;---;%s;;%s;5;%s;%s;;;%s;;\n' % (code,location,country,latitude,longitude,altitude)
		lib[index]=newline
		lib.sort()
	else:
		print 'No se encontro'
	return

def save(lib):
	g=open(info_file,'w')
	g.write(lib)
	g.close()

lib=init_lib()
answer=''
while not answer == 'x':
	answer=raw_input("Abm de estaciones, a=alta b=baja f=find m=modif x=exit")
	if answer =='a':
		array=raw_input("alta: code,location,country,latitude,longitude,altitude").split(',')
		alta(lib,array[0],array[1],array[2],array[3],array[4],array[5])
	elif answer =='b':
		array=raw_input("baja: code")
		baja(lib,array)
	elif answer =='f':
		array=raw_input("find: code")
		index=find_code(lib,array)
		print "\nIndex=%s" % index
		if index != (-1):
			print "\n%s" % lib[index]
	elif answer =='m':
		array=raw_input("modificar: code,location,country,latitude,longitude,altitude").split(',')
		mod(lib,array[0],array[1],array[2],array[3],array[4],array[5])
answer=raw_input("Guardar cambios?")
if answer == 'yes':
	save(lib)

