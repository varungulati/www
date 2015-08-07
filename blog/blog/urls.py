from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'blog.views.index', name='index'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^testing/', include('testing.urls')),
    url(r'^api/', include('api.urls')),
    url(r'^providers_details/', include('providers_details.urls')),
)

