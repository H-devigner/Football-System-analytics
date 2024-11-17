from django.db import models


class Messages(models.Model):
  message = models.TextField(max_length=255)
