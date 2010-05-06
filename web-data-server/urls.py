from django.conf.urls.defaults import *
from views import current_datetime, station_data_available, list_stations, publish_data, rsm_data
# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    (r'^day/$', current_datetime),						# Prints current day of the year
	(r'^station/$', list_stations),						# Lists .dex files available in a STATION directory 
    (r'^station/([A-Z]{4})(\d{0,3})/$', station_data_available),	# Lists Stations directories
	(r'^station/([A-Z]{4}(\d{0,3}))/(\d{5,7})', publish_data),
	(r'^station/([A-Z]{4}(\d{0,3}))/rsm/', rsm_data),
)

