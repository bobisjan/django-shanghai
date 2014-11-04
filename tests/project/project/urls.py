from django.conf.urls import patterns, include, url
from django.contrib import admin

from shanghai import api


urlpatterns = patterns('',
    url(r'^api/', include(api.urls)),
    url(r'^admin/', include(admin.site.urls)),
)
