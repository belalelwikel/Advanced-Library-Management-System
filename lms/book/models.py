from django.db import models
from lms.author.models import Author
from lms.category.models import Category
from lms.library.models import Library
# Create your models here.

class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    libraries = models.ManyToManyField(Library, through='BookLibrary', related_name='books')
    published_date = models.DateField()

    def __str__(self):
        return self.title

class BookLibrary(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    library = models.ForeignKey(Library, on_delete=models.CASCADE)
    available = models.BooleanField(default=True) 

    class Meta:
        unique_together = ('book', 'library')
