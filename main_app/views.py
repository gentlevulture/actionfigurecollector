from django.shortcuts import render
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.views import LoginView
from .models import Figure

# Create your views here.

class Home(LoginView):
  template_name = 'home.html'

def about(request):
  return render(request, 'about.html')

class FigureCreate(CreateView):
  model = Figure
  fields = '__all__'
  
  def form_valid(self, form):
    form.instance.user = self.request.user
    return super().form_valid(form)

def figures_index(request):
  figures = Figure.objects.all()
  return render(request, 'figures/index.html', { 'figures': figures })

def figures_detail(request, figure_id):
  figure = Figure.objects.get(id=figure_id)
  return render(request, 'figures/detail.html', { 'figure': figure })

class FigureUpdate(UpdateView):
  model = Figure
  fields = ['brand', 'description', 'scale']

class FigureDelete(DeleteView):
  model = Figure
  success_url = '/figures/'