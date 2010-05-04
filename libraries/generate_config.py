
import os,pickle

here=os.getcwd()
here=os.chdir('..')
here=os.getcwd()

config = {
	"WORKDIR"  : here,
	"TEMP_FILES_XPIRE"  : '7',
	"DATA_SERVER_IP"   : '',
	"DATA_SERVR_PORT"  : '',
	"UI_SERVER_IP" : '',
	"UI_SERVER_PORT"  : '',
	"DATA_SERVER_THREADS": '',
	"DATA_SERVER_NAME": '',
	"UI_SERVER_THREADS":'',
	"UI_SERVER_PORT":'',
}

f=open('config.txt','w')
pickle.dump(config,f)
f.close()
