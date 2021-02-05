from django.urls import path
from .import views

app_name = 'events'

urlpatterns = [
    path('index',views.index,name = 'index'),
    path('<str:event>',views.event,name="event"),
]