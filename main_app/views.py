from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from .models import Figure, Comic, Photo
import uuid
import boto3

S3_BASE_URL = 'https://s3.us-west-1.amazonaws.com/'
BUCKET = 'action-figure-collector-bucket-of-chum'

# Create your views here.

class Home(LoginView):
  template_name = 'home.html'

def about(request):
  return render(request, 'about.html')

class FigureCreate(LoginRequiredMixin, CreateView):
  model = Figure
  fields = ['name', 'brand', 'description', 'scale']
  
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
  comics_figure_doesnt_have = Comic.objects.exclude(id__in = figure.comics.all().values_list('id'))
  return render(request, 'figures/detail.html', { 
    'figure': figure, 'comics': comics_figure_doesnt_have 
  })

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

class ComicCreate(LoginRequiredMixin, CreateView):
  model = Comic
  fields = '__all__'

class ComicList(LoginRequiredMixin, ListView):
  model = Comic

class ComicDetail(LoginRequiredMixin, DetailView):
  model = Comic

class ComicUpdate(LoginRequiredMixin, UpdateView):
  model = Comic
  fields = ['title', 'publisher']

class ComicDelete(LoginRequiredMixin, DeleteView):
  model = Comic
  success_url = '/comics/'

@login_required
def assoc_comic(request, figure_id, comic_id):
  Figure.objects.get(id=figure_id).comics.add(comic_id)
  return redirect('figures_detail', figure_id=figure_id)

@login_required
def add_photo(request, figure_id):
  photo_file = request.FILES.get('photo-file', None)
  if photo_file:
    s3 = boto3.client('s3')
    key = uuid.uuid4().hex + photo_file.name[photo_file.name.rfind('.'):]
    try:
      s3.upload_fileobj(photo_file, BUCKET, key)
      url = f"{S3_BASE_URL}{BUCKET}/{key}"
      photo = Photo(url=url, figure_id=figure_id)
      figure_photo = Photo.objects.filter(figure_id=figure_id)
      if figure_photo.first():
        figure_photo.first().delete()
      photo.save()
    except Exception as err:
      print('An error occurred uploading file to S3: %s' % err)
  return redirect('figures_detail', figure_id=figure_id)