from django.conf.urls.defaults import patterns, include, url
from django.contrib import admin
from views import *
import apps,settings
admin.autodiscover()

urlpatterns = patterns('',
    url(r'reading/record/', record_reading),
    
)
