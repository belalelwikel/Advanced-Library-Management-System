from rest_framework import viewsets
from ..models import Book
from .serializers import BookSerializer
from django_filters.rest_framework import DjangoFilterBackend

class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all().select_related('author').prefetch_related('category', 'libraries')
    serializer_class = BookSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['author', 'category', 'libraries'] 