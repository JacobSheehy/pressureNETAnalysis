from django.conf.urls import patterns, url


urlpatterns = patterns('customers.views',
    url('^livestream/$', 'create_customer_view', name='customers-livestream'),
)
