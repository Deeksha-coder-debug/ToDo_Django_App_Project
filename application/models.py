from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinLengthValidator
from django.utils import timezone


class Task(models.Model):
    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='tasks',
        null=True,  # Temporary for migration, remove after data migration
    )
    title = models.CharField(
        max_length=100,
        validators=[MinLengthValidator(3, "Title must be at least 3 characters.")]
    )
    complete = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    due_date = models.DateField(null=True, blank=True)
    priority = models.CharField(
        max_length=1,
        choices=[('L', 'Low'), ('M', 'Medium'), ('H', 'High')],
        default='M'
    )
    category = models.CharField(
        max_length=50,
        choices=[('Work', 'Work'), ('Personal', 'Personal'), ('Study', 'Study')],
        default='Personal'
    )
    completed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['due_date', '-priority']
        indexes = [
            models.Index(fields=['user', 'complete']),
            models.Index(fields=['due_date']),
        ]

    def __str__(self):
        return f"{self.title} ({self.user.username if self.user else 'unassigned'})"

    def save(self, *args, **kwargs):
        if self.complete and not self.completed_at:
            self.completed_at = timezone.now()
        elif not self.complete:
            self.completed_at = None
        super().save(*args, **kwargs)

# from django.db import models

# PRIORITY_CHOICES = [
#     ('L', 'Low'),
#     ('M', 'Medium'),
#     ('H', 'High'),
# ]
# # Create your models here.
# class Task(models.Model):
#     title = models.CharField(max_length=100)
#     complete = models.BooleanField(default=False)
#     created = models.DateTimeField(auto_now_add=True)
#     due_date = models.DateField(null=True, blank=True)  # 📅 Due date for sorting
#     priority = models.CharField(
#         max_length=1,
#         choices=[('L', 'Low'), ('M', 'Medium'), ('H', 'High')],
#         default='M'
#     )  # ⭐ Priority choice
#     category = models.CharField(
#         max_length=50,
#         choices=[('Work', 'Work'), ('Personal', 'Personal'), ('Study', 'Study')],
#         default='Personal'
#     )
#     def __str__(self):
#         return self.title
