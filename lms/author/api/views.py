from rest_framework import viewsets
from django.db.models import Count, Q
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from ..models import Author
from lms.book.models import Book
from .serializers import AuthorSerializer, LoadedAuthorSerializer


class AuthorViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer

    def get_queryset(self):
        library_id = self.request.query_params.get('library')
        category_id = self.request.query_params.get('category')

        queryset = Author.objects.all()

        filter_q = Q()

        if library_id:
            filter_q &= Q(book__libraries__id=library_id)
        if category_id:
            filter_q &= Q(book__category__id=category_id)

        queryset = queryset.annotate(
            book_count=Count('book', filter=filter_q, distinct=True)
        ).filter(book_count__gt=0)  

        return queryset

class LoadedAuthorViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Author.objects.all()
    serializer_class = LoadedAuthorSerializer

    def get_queryset(self):
        library_id = self.request.query_params.get('library')
        category_id = self.request.query_params.get('category')

        queryset = Author.objects.all()

        if library_id:
            queryset = queryset.filter(book__libraries__id=library_id)
        if category_id:
            queryset = queryset.filter(book__category__id=category_id)

        queryset = queryset.prefetch_related(
            'book_set__libraries',  
            'book_set__category'  
        )

        return queryset.distinct()