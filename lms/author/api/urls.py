from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AuthorViewSet, LoadedAuthorViewSet

router = DefaultRouter()
router.register(r'authors', AuthorViewSet,basename='authors')
router.register(r'loaded-authors', LoadedAuthorViewSet,basename='loaded-authors')
app_name = "author"

urlpatterns = [
    path('', include(router.urls)),
]
