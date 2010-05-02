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
	return knots*0.514444444*4.87/math.log(67.87*10-5.42)

###################################### Get values from file f

def getdata(f):

#Gets a numeric "value" from a string 

	val= re.findall(r'\d+\.\d+|\d+',f)
	if val:
		return float(val[0])
	else:
		return 0

	
def etowind(foo,wstation):

	gdat=False
	TMean=21.0
	P=101.3
	TDew=16.0
	Wspeed=1.0
	
	
	if foo[1]!='\n': #Metar data. 
		
		
		for i in range(len(foo)):
	

			#print 'Metar: %s'%foo[i]
		
			if re.findall('temperature:',foo[i]): 
				TMean=float(getdata(foo[i]))
		
			if re.findall('pressure:',foo[i]):
				P=float(getdata(foo[i])/10.0)

			if re.findall('dew point:',foo[i]):
				TDew=float(getdata(foo[i]))

			if re.findall('wind:',foo[i]):
				Wspeed=wsp(float(getdata(foo[i])))


		
		Es=edt(TMean)
		Ea=edt(TDew)
		
		
	
	else:	

		#print 'Google?'
 		gdat=eval(foo[3])
				
		if len(gdat['current_conditions'])==0:
			print 'no data'
			return'-1'
		else:
			#print 'yes! google'
			TMean=float(gdat['current_conditions']['temp_c'])
			P=atmp(float(wstation['altitude']),TMean)
			RH=float(re.findall('\d+',gdat['current_conditions']['humidity'])[0])
			Es=edt(TMean)
			Ea=Es*RH/100
			w=gdat['current_conditions']['wind_condition']
			if w.isdigit():
				Wspeed=float(re.findall('\d+',w)[0])*0.44704 #to m/s	
			else:
				Wspeed=0

	
	
	DeltaTMean=delta(TMean)
	Gamma=gamma(P)
	etowh= Gamma*(900.0/24.0)*Wspeed*(Es-Ea)/((DeltaTMean+Gamma*(1+0.34*Wspeed))*(TMean+273.0)) # mm/hour
		
	return "\nETO Wind: " +str(etowh) +"\nWindsp: " + str(Wspeed) + "\nTemp: " + str(TMean) + "\nea: " + str(Ea)




