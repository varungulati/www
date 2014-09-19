from django.conf.urls import patterns, include, url

from django.contrib import admin
from dajaxice.core import dajaxice_autodiscover, dajaxice_config
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

dajaxice_autodiscover()
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'sampleapp.views.home', name='home'),
    url(dajaxice_config.dajaxice_url, include('dajaxice.urls')),
    url(r'^register/$', 'trafficUser.views.TrafficUserRegistration'),
    url(r'^profile/$', 'trafficUser.views.Profile'),
    url(r'^profile/(?P<username>\w+)$', 'trafficUser.views.Profile'),
    url(r'^execute_c/$', 'sampleapp.views.executeC'),
    url(r'^food_cart/$', 'foodCart.views.foodCart'),
    url(r'^broken_urls/$', 'sampleapp.views.brokenURLs'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
)

urlpatterns += staticfiles_urlpatterns()