
import os,pickle

here=os.getcwd()
here=os.chdir('..')
here=os.getcwd()

config = {
	"WORKDIR"  : here,
	"TEMP_FILES_XPIRE"  : '7',
	"DATA_SERVER_IP"   : '127.0.0.1',
	"DATA_SERVER_PORT"  : '8000',
	"UI_SERVER_IP" : '',
	"UI_SERVER_NAME": '',
	"DATA_SERVER_THREADS": '20',
	"DATA_SERVER_NAME": 'peko.tk',
	"UI_SERVER_THREADS":'',
	"UI_SERVER_PORT":'',
	"DEX_FILES_EXPIRE": '400'
}

f=open('config.txt','w')
pickle.dump(config,f)
f.close()
