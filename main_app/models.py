from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User

# Create your models here.

class Comic(models.Model):
  artist = models.CharField(max_length=25)
  title = models.CharField(max_length=50)
  publisher = models.CharField(max_length=25)
  issue = models.IntegerField()

  def __str__(self):
    return self.title

  def get_absolute_url(self):
    return reverse('comics_detail', kwargs={'pk': self.id})

class Figure(models.Model):
  name = models.CharField(max_length=30)
  brand = models.CharField(max_length=30)
  description = models.TextField(max_length=100)
  scale = models.IntegerField()
  comics = models.ManyToManyField(Comic)
  user = models.ForeignKey(User, on_delete=models.CASCADE)

  def __str__(self):
    return self.name
    
  def get_absolute_url(self):
    return reverse('figures_detail', kwargs={'figure_id': self.id})

class Photo(models.Model):
  url = models.CharField(max_length=250)
  figure = models.OneToOneField(Figure, on_delete=models.CASCADE)

  def __str__(self):
    return f"Photo for figure_id: {self.figure_id} @{self.url}"