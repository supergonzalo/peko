#! /usr/bin/env python


# Librerias para el calculo de la ETO ETO por radiacion de forma DIARIA (Pos dia).


import math, re,os
import datetime
import etowind20


###################################### (Aux) To Radians

def torad(deg,minutes,hemisf):

	rad=(deg+minutes/60.0)*math.pi/180.0
	if( hemisf=='S'):
		rad = - rad
	return rad
	
###################################### (Aux) Day of the year-> J

def doy(date):
	
	return date.strftime('%j')


###################################### Inverse distance Sun-Earth

def dr(j):
	return 1+0.033*math.cos(2*math.pi*j/365)

###################################### Solar Declination

def dmin(j):
	return (0.409*math.sin(2*math.pi*j/365-1.39))

###################################### Sunset hour angle

def ws(j, lat):
	return math.acos(-math.tan(lat)*math.tan(dmin(j)))

###################################### Extraterrestrial radiation

def ra(j,lat):

	return 24*60*0.082*dr(j)*(ws(j,lat)*math.sin(lat)*math.sin(dmin(j))+math.cos(lat)*math.cos(dmin(j))*math.sin(ws(j,lat)))/math.pi

###################################### Daylight hours

def N(j,lat):

		return 24*ws(j,lat)/math.pi

###################################### Solar radiation Rs

def rs(krs,tmax,tmin,ra):
	

	return (krs*ra*(tmax-tmin)**0.5)

###################################### RS0

def rso(z,j,lat):

	return (0.75+2*z/100000)*ra(j,lat)

###################################### Rnl 

def rnl(tmed,ex_rad,rs,rso):

	return (tmed*(0.34-0.14*ex_rad)**0.5)*(1.35*rs/rso-0.35)


###################################### Rn

def rn(rns,rnl):
	return rns-rnl


###################################### ETo

def eto(tmed,rn,p,es,ea,ws):
	#0.95 Estimador Gonzalo, estima G
	return (0.408*rn*0.97*etowind20.delta(tmed)+etowind20.gamma(p)*(900/(tmed+273))*ws*(es-ea))/(etowind20.delta(tmed)+etowind20.gamma(p)*(1+0.34*ws))


#########################################################################################################################
def getdata(f):

#Gets a numeric "value" from a string 

	val= re.findall(r'\d+\.\d+|\d+',f)
	if val:
		return float(val[0])
	else:
		return float(0)

def arch(filename, mode, data):
	f = open(filename, mode)				#filename format:  Y=year, D=day of year H=Hour	
	if mode=='r' or mode=='r+':
		temp=f.readlines()	
	else:
		f.write(data)
		temp=True
	f.close()	
	return temp
#########################################################################################################################
###################################### Load data into memory
def data_matrix(foo):
	
	temp_ea=0
	counter=0
	temp_etwind=0
	temp_windsp=0
	t=0
	u=0
	tmax=-50.0
	tmin=100.0
	

	for i in range(len(foo)):
		
		if re.findall('Timestamp:',foo[i]): 
			counter=counter+1
		
		if re.findall('ETO Wind:',foo[i]):
			temp_etwind=temp_etwind+getdata(foo[i])

		if re.findall('Windsp:',foo[i]):
			temp_windsp=temp_windsp+getdata(foo[i])
		
		if re.findall('Temp:',foo[i]):
		
			t=getdata(foo[i])			#temp
			if t>tmax:
				tmax=t
			if t<tmin:
				tmin=t
			u=u+t

		if re.findall('ea:',foo[i]):
			temp_ea=temp_ea+getdata(foo[i])
		

	
	return {'tmax':float(tmax),'tmin':float(tmin),'med_wind':float(temp_windsp/counter),'etowind':float(temp_etwind*24/counter),'tmed':float(u/counter),'eamed':float(temp_ea/counter)}

#######################################Programa################################################

	
def etorad(fs,station_name,filename):

	#fs lista donde cada valor es un renglon del archivo
	#station name
	#name of fs file
	
	krs=0.18		#0.16 interior, 0.19 coast, Rs=0.7Ra-4 island
	
	j=int(filename[4:7])
	temp=data_matrix(fs)
	#print temp
	wmed=temp['med_wind']
	tmax=temp['tmax']
	tmin=temp['tmin']
	tmed=temp['tmed']
	etowind=temp['etowind']
	
	lat=float(station_name['latitude'])*3.14159265/180
	hemisf=station_name['hemisf']
	z=float(station_name['altitude'])	
	p=etowind20.atmp(z,tmed)
	

	d=etowind20.delta(tmed)
						
	g=etowind20.gamma(p)

	DT=d/(d+g*(1+0.34*wmed))

	dr(j)
	dmin(j)
	ws(j, lat)
	ext_radiation=ra(j,lat)
	N(j,lat)
	surface_rad=rs(krs,tmax,tmin,ext_radiation) #Mean surface radiation
	pot_rad=rso(z,j,lat)

	esuba=temp['eamed']
	#rnl(tmed,esuba,surface_rad,pot_rad)
	radiation=rn(pot_rad,surface_rad)
	#print radiation

	etorad=DT*(0.408*radiation*0.98)	#0.98 Estimador Gonzalo, estima perdidas por G
	if etorad<0:
		etorad=0
	
	#print "\nETO WindTODAY: " +str(etowind)+"\nETOradTODAY: " +str(etorad)+"\nETOTODAY: " +str(float(etorad)+float(etowind))+"\nEstimada: " +str(0.0023*(tmed+17.8)*ext_radiation*(tmax-tmin)**(0.5))

	return "\nETO WindTODAY: " +str(etowind)+"\nETOradTODAY: " +str(etorad)+"\nETOTODAY: " +str(float(etorad)+float(etowind))+"\nEstimada: " +str(0.0023*(tmed+17.8)*ext_radiation*(tmax-tmin)**(0.5))+ "\nTempMax: "+str(tmax)+"\nTempMin: "+str(tmin) + "\nTempMed: "+str(tmed) + "\nWindMed: "+str(wmed)
	




