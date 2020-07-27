from django.urls import path


from . import views

app_name = "account"

urlpatterns = [
    path('register/', views.registerPage, name="register"),
    path('login/', views.loginPage, name="login"),
    path('logout/', views.logout_user, name="logout"),
    path('edit_profile/', views.edit_profile, name="edit_profile"),
    path('change_password/', views.change_password, name="change_password"),
    path('profile/', views.profile, name="profile"),
]
