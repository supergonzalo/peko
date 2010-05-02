import wsgiserver
#This can be from cherrypy import wsgiserver if you're not running it standalone.
import sys, pickle
import os
import django.core.handlers.wsgi
from django.core.servers.basehttp import AdminMediaHandler
from translogger import TransLogger

here=os.getcwd()
os.chdir('../..')
f=open('config.txt','r')
config=pickle.load(f)
f.close
os.chdir(here)

if __name__ == "__main__":
    sys.path.append(config["WORKDIR"]+'/data-server/')
    os.environ['DJANGO_SETTINGS_MODULE'] = 'application.settings'
 
    app = AdminMediaHandler(django.core.handlers.wsgi.WSGIHandler())
    logged_app = TransLogger(app)
    server = wsgiserver.CherryPyWSGIServer(	
        (config["DATA_SERVER_IP"], config["DATA_SERVER_PORT"]),
        logged_app,
        server_name=config["DATA_SERVER_NAME"],
        numthreads = config["DATA_SERVER_THREADS"],
    )
 
    try:
        server.start()
    except KeyboardInterrupt:
        server.stop()
