from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='my_index'),
    url(r'^signin$', views.login, name='my_signin'),
    url(r'^register$', views.register, name='my_register'),
    url(r'^logoff$', views.logoff, name='my_logoff'),
]
