from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter


app_name = "users"

urlpatterns = [

        path('rest-auth/', include('dj_rest_auth.urls')),

]
