from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth import get_user_model
from lms.book.models import BookLibrary
User = get_user_model()
class Borrowing(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(BookLibrary,on_delete=models.CASCADE)
    borrow_date = models.DateField(auto_now_add=True)
    return_date = models.DateField()
    returned = models.BooleanField(default=False)
    overdue_penalty = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)

    def calculate_penalty(self):
        if self.returned:
            return 0.0
        today = timezone.now().date()
        if self.return_date < today:
            overdue_days = (today - self.return_date).days
            penalty = overdue_days * 1.00  
            self.overdue_penalty = penalty
            self.save()
            return penalty
        return 0.0
