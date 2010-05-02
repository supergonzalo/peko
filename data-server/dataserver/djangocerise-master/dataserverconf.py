import os, glob,re,pickle,sys

here=os.getcwd()
os.chdir('../../..')
f=open('config.txt','r')
config=pickle.load(f)
f.close
os.chdir(here)

os.chdir('..')
sys.path.append(os.getcwd())
os.chdir(here)


###########################################################################
# Configuration
#
# Django settings
DJANGO_SETTINGS = 'dataserver.settings'
DJANGO_SERVE_ADMIN = False # Serve admin files

# Server settings
IP_ADDRESS = config["DATA_SERVER_IP"]
PORT = int(config["DATA_SERVER_PORT"])
SERVER_NAME = config["DATA_SERVER_NAME"]
SERVER_THREADS = config["DATA_SERVER_THREADS"]
# Change it to True if you want it to run as daemon, if you use a
# daemon.sh file you should also change it to True
RUN_AS_DAEMON = False
DAEMON_RUN_DIR = '/' # The daemon will change directory to this one
                     # this is needed to prevent unmounting your
                     # disk.

# Log settings
LOGFILE = '/tmp/webserver.log'
LOGLEVEL = 'INFO' # if DEBUG is True, overwritten to DEBUG
DEBUG = True

# It must match with the path given in your daemon.sh file if you are
# using a daemon.sh file to control the server.
PIDFILE = '/var/run/django-myproject.pid'

# Launch as root to dynamically chown
SERVER_USER = 'nobody'
SERVER_GROUP = 'nobody'

# Enable SSL, if enabled, the certificate and private key must
# be provided.
SSL = False
SSL_CERTIFICATE = '/full/path/to/certificate'
SSL_PRIVATE_KEY = '/full/path/to/private_key'

#
###########################################################################
