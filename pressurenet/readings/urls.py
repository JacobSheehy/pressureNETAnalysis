from django.conf.urls import patterns, include, url

urlpatterns = patterns('readings.views',
    url('^$', 'index', name='readings-index'),
    url('^list/$', 'reading_list', name='readings-list'),
    url('^live/$', 'reading_live', name='readings-live'),
    url('^addfrompressurenet/$', 'add_from_pressurenet'),
)

