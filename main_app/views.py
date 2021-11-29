from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def home(request):
  return render(request, 'home.html')

def about(request):
  return render(request, 'about.html')

class Figure:
  def __init__(self, name, brand, description, scale):
    self.name = name
    self.brand = brand
    self.description = description
    self.scale = scale

figures = [
  Figure('Medieval Spawn III', 'McFarlane', 'Missing shield.', 6),
  Figure('Grand Admiral Thrawn', 'Hasbro', 'On card.', 6),
  Figure('Boba Fett', 'Hasbro', 'On card.', 3.75),
  Figure('Batman - DC Artists Alley', 'DC Entertainment', 'Designed by nooligan. Loose.', 6)
]

def figures_index(request):
  return render(request, 'figures/index.html', { 'figures': figures })