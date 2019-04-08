"""
Definition of urls for CourtDesk.
"""

from datetime import datetime
from django.urls import path
from django.conf.urls import include,url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

#from rest_framework_jwt.views import obtain_jwt_token
#from rest_framework_jwt.views import refresh_jwt_token
#from rest_framework_jwt.views import verify_jwt_token


urlpatterns = [
    path('api/',include('app.urls')),
    #path('', admin.site.urls),
    path('admin/', admin.site.urls),
    #url(r'^auth-jwt/', obtain_jwt_token),
    #url(r'^auth-jwt-refresh/', refresh_jwt_token),
    #url(r'^auth-jwt-verify/', verify_jwt_token),

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
