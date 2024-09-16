from rest_framework import viewsets
from ..models import Library
from .serializers import LibrarySerializer


class LibraryViewSet(viewsets.ModelViewSet):
    queryset = Library.objects.all()
    serializer_class = LibrarySerializer
    

    def get_queryset(self):
        queryset = Library.objects.all()

        author_ids = self.request.query_params.getlist('author')
        category_ids = self.request.query_params.getlist('category')

        if author_ids:
            queryset = queryset.filter(books__author__id__in=author_ids)

        if category_ids:
            queryset = queryset.filter(books__category__id__in=category_ids)

        if author_ids or category_ids:
            queryset = queryset.prefetch_related('books__author', 'books__category')

        return queryset.distinct()
