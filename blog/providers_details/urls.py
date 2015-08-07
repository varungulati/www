from django.conf.urls import patterns, url


urlpatterns = patterns(
    'providers_details.views',
    url(r'^providers_details/$', 'providers_details', name='providers_details'),
  )