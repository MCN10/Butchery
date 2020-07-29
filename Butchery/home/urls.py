from django.urls import path

from . import views

app_name = "home"


urlpatterns = [
    #Leave as empty string for base url
	path('', views.home, name="home"),
	path('contact/', views.contact, name="contact"),
	path('profile/', views.profile, name="profile"),
    ]
