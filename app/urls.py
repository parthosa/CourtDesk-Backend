from django.conf.urls import url
from app import views
from django.urls import path

urlpatterns = [
    path('login/',views.login_user,name='login_user'),
    path('get_courtrooms/',views.get_courtrooms,name='get_courtrooms'),
    path('logout/',views.logout_user,name='logout_user'),
    path('get_casefile_list/', views.get_casefile_list, name='get_casefile_list'),
    path('get_casefile/', views.get_casefile, name='get_casefile'),
    path('get_file_stream/', views.get_file_stream, name='get_file_stream'),
    path('update_peshi/', views.update_peshi, name='update_peshi'),
    path('update_order/', views.update_order, name='update_order'),
    path('update_is_urgent/', views.update_is_urgent, name='update_is_urgent'),
    path('update_casefile_details/', views.update_casefile_details, name='update_casefile_details'),
    path('update_notes/', views.update_notes, name='update_notes'),
    path('update_order_status/', views.update_order_status, name='update_order_status'),
    path('add_file/', views.add_file, name='add_file')
    ]