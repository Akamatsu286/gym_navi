from django.db import models
from django.utils import timezone

class Post(models.Model):
    title = models.CharField(max_length=100)
    text = models.TextField(blank=True)
    created_at = models.DateTimeField('作成日', default=timezone.now)
    updated_at = models.DateTimeField('更新日', default=timezone.now)

    def __str__(self):
        return self.title