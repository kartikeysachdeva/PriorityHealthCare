from django.urls import path
from newHackApp import views

urlpatterns = [
    path("", views.home, name="home"),
    #path("newHackApp/<name>", views.fronttest, name="fronttest"),
    path("submission", views.PatientDataMethod, name='PatientDataMethod'), #EDIT THIS!!!!!!
    
]

