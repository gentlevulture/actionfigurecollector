from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from .models import Figure, Comic

# Create your views here.

class Home(LoginView):
  template_name = 'home.html'

def about(request):
  return render(request, 'about.html')

class FigureCreate(LoginRequiredMixin, CreateView):
  model = Figure
  fields = '__all__'
  
  def form_valid(self, form):
    form.instance.user = self.request.user
    return super().form_valid(form)

@login_required
def figures_index(request):
  figures = Figure.objects.filter(user=request.user)
  return render(request, 'figures/index.html', { 'figures': figures })

@login_required
def figures_detail(request, figure_id):
  figure = Figure.objects.get(id=figure_id)
  return render(request, 'figures/detail.html', { 'figure': figure })

class FigureUpdate(LoginRequiredMixin, UpdateView):
  model = Figure
  fields = ['brand', 'description', 'scale']

class FigureDelete(LoginRequiredMixin, DeleteView):
  model = Figure
  success_url = '/figures/'

def signup(request):
  error_message = ''
  if request.method == 'POST':
    form = UserCreationForm(request.POST)
    if form.is_valid():
      user = form.save()
      login(request, user)
      return redirect('figures_index')
    else:
      error_message = 'Invalid sign up - try again'
  form = UserCreationForm()
  context = {'form': form, 'error_message': error_message}
  return render(request, 'signup.html', context)

class ComicCreate(CreateView):
  model = Comic
  fields = '__all__'

class ComicList(ListView):
  model = Comic

class ComicDetail(DetailView):
  model = Comic