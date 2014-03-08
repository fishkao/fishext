from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('fishext.views',
    url(r'^$', 'dashboard'),
)