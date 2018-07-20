from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^new$', views.new, name='my_new'),
    url(r'^edit$', views.editself),
    url(r'^edit/info$', views.editselfinfo),
    url(r'^edit/password$', views.editselfpassword),
    url(r'^edit/description$', views.editselfdescription),
    url(r'^edit/(?P<user_id>\d+)$', views.editother),
    url(r'^edit/(?P<user_id>\d+)/info$', views.editotherinfo),
    url(r'^edit/(?P<user_id>\d+)/password$', views.editotherpassword),
    url(r'^show/(?P<user_id>\d+)$', views.show),
    url(r'^destroy/(?P<user_id>\d+)$', views.destroy),
]
