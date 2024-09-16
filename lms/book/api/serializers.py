from rest_framework import serializers
from ..models import Book, BookLibrary
from lms.category.api.serializers import CategorySerializer

class BookLibrarySerializer(serializers.ModelSerializer):
    library = serializers.StringRelatedField() 
    class Meta:
        model = BookLibrary
        fields = ['library', 'available']

class BookSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField()
    category = serializers.StringRelatedField()

    availability = BookLibrarySerializer(source='booklibrary_set', many=True) 
    class Meta:
        model = Book
        fields = ['id', 'title', 'author', 'category', 'availability','published_date']


class LoadedBookSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)

    class Meta:
        model = Book
        fields = ['id', 'title', 'category']
