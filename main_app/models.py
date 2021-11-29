from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User

# Create your models here.

class Figure(models.Model):
  name = models.CharField(max_length=30)
  brand = models.CharField(max_length=30)
  description = models.TextField(max_length=100)
  scale = models.IntegerField()
  user = models.ForeignKey(User, on_delete=models.CASCADE)

  def __str__(self):
    return self.name
    
  def get_absolute_url(self):
    return reverse('figures_detail', kwargs={'figure_id': self.id})