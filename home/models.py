from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'name'],
                                    name='unique_category_per_user')
        ]

    def __str__(self):
        return self.name


class Expense(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    title = models.CharField(max_length=50, blank=True, default="")
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.amount} | {self.title}"


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=20, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    google_table_id = models.CharField(max_length=100, blank=True, default="")
