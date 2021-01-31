from django.conf.urls import url
from .import views

app_name = 'users'

urlpatterns = [
    url(r'^$', views.usersList, name='userslist'),
    url(r'^signin/', views.userSignin, name='usersignin'),
    url(r'^signup/', views.userSignup, name='usersignup'),
    url(r'^logout/', views.userLogout, name='userlogout'),
    url(r'^recovery/', views.userRecovery, name="userrecovery"),
    url(r'^activate/(?P<uidb64>[^/]+)/(?P<token>[^/]+)/$', views.activate, name='activate'),
    url(r'newpassword/(?P<uidb64>[^/]+)/(?P<token>[^/]+)/$', views.userNewpassword, name='newpassword'),
    url(r'^update/(?P<pk>[^/]+)/$', views.userUpdate, name='userupdate'),
    url(r'^(?P<email>[\w.@+-]+)/$', views.userProfile, name = 'userprofile'),
]