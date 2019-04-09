from django.conf.urls import url
from app import views
from django.urls import path

urlpatterns = [
    path('login/',views.login_user,name='login_user'),
    path('get_courtrooms/',views.get_courtrooms,name='get_courtrooms'),
    path('logout/',views.logout_user,name='logout_user'),
    path('get_casefile_list/', views.get_casefile_list, name='get_casefile_list'),
    path('get_casefile/', views.get_casefile, name='get_casefile'),
    path('get_file_stream/', views.get_file_stream, name='get_file_stream')
    path('update_peshi/', views.update_peshi, name='update_peshi')
    path('update_order/', views.update_order, name='update_order')
    ]