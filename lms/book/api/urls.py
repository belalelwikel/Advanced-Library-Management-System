from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BookViewSet

router = DefaultRouter()
router.register('', BookViewSet)

app_name = "book"
urlpatterns = [

        path('', include(router.urls)),

]
