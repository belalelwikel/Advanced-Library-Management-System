from django.db import models

class Author(models.Model):
    full_name = models.CharField(max_length=100)
    biography = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.full_name