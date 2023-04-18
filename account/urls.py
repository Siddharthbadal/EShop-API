from django.urls import path
from . import views 


urlpatterns = [
    path('register/', views.register, name='register'),
    path('myaccount/', views.get_current_user, name='get_current_user'),
    path('myaccount/update', views.update_user_info, name='update_user_info'),
    path('myaccount/update_password', views.update_user_password, name='update_user_password'),
    ]
