from django.conf.urls.defaults import *
from views import current_datetime, station_data_available, list_stations, publish_data, rsm_data, raw, test
# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
  (r'^day/$', current_datetime),																# Prints current day of the year
	#(r'^station/$', list_stations),															# Lists Stations available 
  (r'^([a-z])/([A-Z]{4})(\d{0,3})/$', station_data_available),	# Lists Stations directories
	(r'^([a-z])/([A-Z]{4}(\d{0,3}))/(\d{5,7})', publish_data),		# Prints data for station & day
	(r'^([a-z])/([A-Z]{4}(\d{0,3}))/rsm/', rsm_data),							# Prints rsm file for station
	(r'^([a-z])/([A-Z]{4}(\d{0,3}))/data/', raw),									# Prints info wiindow for ui-server
	(r'^([a-z])/$', list_stations),																# Lists Stations available (x= xml, t=text) 
	(r'^([a-z])/([A-Z]{4}(\d{0,3}))/test/', test),								# testing
)

