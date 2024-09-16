from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BorrowingViewSet, ReturnAPIView

router = DefaultRouter()
router.register(r'', BorrowingViewSet)
app_name = "borrow"

urlpatterns = [

        path('', include(router.urls)),
         path('returns/<int:pk>/', ReturnAPIView.as_view(), name='return_book'),

]
