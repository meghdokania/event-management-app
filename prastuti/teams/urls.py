from django.conf.urls import url
from .import views

app_name = 'teams'

urlpatterns = [
    url(r'^$', views.teamsList, name='teamslist'),
    url(r'^register/', views.teamRegister, name='teamregister'),
    url(r'^(?P<pk>[\w-]+)/$', views.teamDetail, name = 'teamdetail'),
]