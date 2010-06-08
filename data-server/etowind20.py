#! /usr/bin/env python


# Librerias para el calculo de la ETO por viento de forma horaria.


import math
import re
#import datetime
#import time


###################################### Atm Pressure
def atmp (z=0,t=20):

	return 101.3*((273+t-0.0065*z)/(273+t))**(5.26)


###################################### Psychrometric constant 

def gamma (p=101.3):
#Calculates gamma based on atm pressure
	return (0.665e-3)*p


###################################### Slope Vapour Pressure Curve 

def delta (t=20):

	return 4098*edt(t)/((t+237.3)**2)

###################################### (Aux) saturation vapour pressure

def edt(t):
	return 0.6108*math.exp(17.27*t/(t+237.3))



###################################### Wind speed @ ground

def wsp(knots):	#Estimates wind speed @ 2m based on a wsp measured @ 10m
	return (knots)*0.747

###################################### Get values from file f

def getdata(f):

#Gets a numeric "value" from a string 

	val= re.findall(r'\d+\.\d+|\d+',f)
	if val:
		return float(val[0])
	else:
		return 0

	
def etowind(foo,wstation):	#cambiar, ya recibe los datos para procesar en foo, si foo es lista, son datos metar y si es dict son datos google

	TMean=21.0
	P=101.3
	TDew=16.0
	Wspeed=1.0

	
	if isinstance(foo, dict): #Google data. 
		#print 'Google %s\n'%foo
		TMean=float(foo['current_conditions']['temp_c'])
		P=atmp(float(wstation['altitude']),TMean)
		RH=float(re.findall('\d+',foo['current_conditions']['humidity'])[0])
		Es=edt(TMean)
		Ea=Es*RH/100
		try:
			Wspeed=float(re.findall('\d[0-9]{0,2}',foo['current_conditions']['wind_condition'])[0])/0.447 #Es mph to m/s
		except:	
			Wspeed=0.1
				
	elif foo[0]=='Metar\n':	
		#print 'Metar: %s\n'%foo
		for element in range(len(foo)):
		
			if re.findall('temperature:',foo[element]): 
				TMean=float(getdata(foo[element]))
		
			if re.findall('pressure:',foo[element]):
				P=float(getdata(foo[element])/10.0)

			if re.findall('dew point:',foo[element]):
				TDew=float(getdata(foo[element]))

			if re.findall('wind:',foo[element]):
				Wspeed=float(getdata(foo[element]))/0.5144		#Es knots to m/s

	else:
		return ''
		
	Es=edt(TMean)
	Ea=edt(TDew)
		
	#print 'Tmean %s P %s TDEW %s Wspeed %s'%(TMean,P,TDew,Wspeed)	

	Wspeed=wsp(Wspeed)
	DeltaTMean=delta(TMean)
	Gamma=gamma(P)
	etowh= Gamma*(900.0/24.0)*Wspeed*(Es-Ea)/((DeltaTMean+Gamma*(1+0.34*Wspeed))*(TMean+273.0)) # mm/hour
	if etowh < 0:
		etowh=0
	if Ea < 0:
		Ea=0
		
	return "\nETO Wind: " +str(etowh) +"\nWindsp: " + str(Wspeed) + "\nTemp: " + str(TMean) + "\nea: " + str(Ea)




