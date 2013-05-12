from django.conf.urls import patterns, url


urlpatterns = patterns('readings.views',
    url('^$', 'index', name='readings-index'),
    url('^addfrompressurenet/$', 'add_from_pressurenet', name='readings-addfrompressurenet'),
    url('^add/$', 'create_reading', name='readings-create'),
    url('^conditions/add/$', 'create_condition', name='readings-create-condition'),
    url('^list/$', 'reading_list', name='readings-list'),
    url('^live/$', 'reading_live', name='readings-live'),
    url('^livestream/$', 'livestream', name='readings-livestream'),
    url('^about/$', 'about', name='readings-about'),
)
