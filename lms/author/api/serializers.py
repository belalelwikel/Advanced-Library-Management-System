from rest_framework import serializers
from ..models import Author
from lms.book.models import Book
from lms.book.api.serializers import LoadedBookSerializer
class AuthorSerializer(serializers.ModelSerializer):
    book_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Author
        fields = ['id', 'full_name', 'biography','book_count']


class LoadedAuthorSerializer(serializers.ModelSerializer):
    books = LoadedBookSerializer(many=True, source='book_set', read_only=True)

    class Meta:
        model = Author
        fields = ['id', 'full_name','biography','books']