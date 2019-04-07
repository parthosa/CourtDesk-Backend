"""
Definition of urls for CourtDesk.
"""

from datetime import datetime
from django.urls import path
from django.contrib import admin
from django.contrib.auth.views import LoginView, LogoutView
from app import forms, views

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    #path('', views.home, name='home'),
    #path('contact/', views.contact, name='contact'),
    #path('about/', views.about, name='about'),
    #path('login/',
    #     LoginView.as_view
    #     (
    #         template_name='app/login.html',
    #         authentication_form=forms.BootstrapAuthenticationForm,
    #         extra_context=
    #         {
    #             'title': 'Log in',
    #             'year' : datetime.now().year,
    #         }
    #     ),
    #     name='login'),
    #path('logout/', LogoutView.as_view(next_page='/'), name='logout'),
    path('', admin.site.urls),
    path('admin/', admin.site.urls),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
