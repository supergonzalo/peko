from operator import itemgetter, attrgetter
import pickle

def manh_distance(lat1,long1,lat2,long2):
	return abs(lat1-lat2)+abs(long1-long2)

f=open("./Doc/stations.lib",'r')
stats=pickle.load(f)
f.close

base=[0.0,0.0]
sorted_list=list()

for element in stats:
	
	sorted_list.append([element,manh_distance(base[0],base[1],stats[element]['latrad'],stats[element]['longrad'])])
result=sorted(sorted_list, key=itemgetter(1))
