from django.urls import path
from . import views

urlpatterns = [
  path('', views.Home.as_view(), name='home'),
  path('about/', views.about, name='about'),
  path('figures/', views.figures_index, name='figures_index'),
  path('figures/<int:figure_id>/', views.figures_detail, name='figures_detail'),
]