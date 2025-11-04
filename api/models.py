from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import uuid

# Профиль пользователя с подпиской
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    subscription_active = models.BooleanField(default=False)
    subscription_end = models.DateTimeField(null=True, blank=True)
    domain = models.CharField(max_length=255, blank=True, null=True) 

    def __str__(self):
        return self.user.username

# Тариф или план подписки
class SubscriptionPlan(models.Model):
    name = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    duration_days = models.PositiveIntegerField(default=30)  # срок действия подписки

    def __str__(self):
        return f"{self.name} - ${self.price}"

# Задача сканирования сайта
class ScanTask(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('done', 'Done'),
        ('failed', 'Failed'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='scan_tasks')
    url = models.URLField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.url} - {self.status}"

# Результаты сканирования (JSON)
class ScanResult(models.Model):
    task = models.OneToOneField(ScanTask, on_delete=models.CASCADE, related_name='result')
    result = models.JSONField()
    scanned_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Result for {self.task.url}"
