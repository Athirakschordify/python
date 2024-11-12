from django.urls import path
from . import views

urlpatterns = [
    path('',views.index,name='index'),
    path('about/',views.aboout,name='about'),
    path('contact/',views.contact,name='contact'),
    path('event/',views.event,name='event'),
    path('booking/',views.booking,name='booking'),

]
