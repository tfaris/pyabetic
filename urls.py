from django.conf.urls.defaults import patterns, include, url
from django.contrib import admin
from views import *
import apps,settings
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    url(r'^$',HomeView.as_view()),
    url(r'^login/$', LoginView.as_view()),
    url(r'^logout/$', LogoutView.as_view()),
    url(r'^register/$', RegisterView.as_view()),
    url(r'^bg/', include(apps.bgtrack.site.urls)),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^reading/record/$', RecordReadingView.as_view())
)
