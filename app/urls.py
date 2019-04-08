from django.conf.urls import url
from app import views
from django.urls import path

urlpatterns = [
    path('login/',views.login_user,name='login_user'),
    path('get_courtrooms/',views.get_courtrooms,name='get_courtrooms'),
    path('logout/',views.logout_user,name='logout_user')
    path('get_casefile_list/', views.get_casefile_list, name='get_casefile_list')
    ]