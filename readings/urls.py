from django.conf.urls import patterns, include, url


urlpatterns = patterns('readings.views',
    url('^$', 'index', name='readings-index'),
    url('^addfrompressurenet/$', 'add_from_pressurenet', name='readings-addfrompressurenet'),
    url('^add/$', 'create_reading', name='readings-create'),
    url('^list/$', 'reading_list', name='readings-list'),
    url('^live/$', 'reading_live', name='readings-live'),
    url('^livestream/$', 'livestream', name='readings-livestream'),
    url('^about/$', 'about', name='readings-about'),
)
