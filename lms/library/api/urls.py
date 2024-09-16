from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import LibraryViewSet
router = DefaultRouter()
router.register(r'', LibraryViewSet)

app_name = "library"

urlpatterns = [

        path('', include(router.urls)),

]
