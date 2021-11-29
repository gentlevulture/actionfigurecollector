from django.urls import path
from . import views

urlpatterns = [
  path('', views.Home.as_view(), name='home'),
  path('about/', views.about, name='about'),
  path('figures/', views.figures_index, name='figures_index'),
  path('figures/<int:figure_id>/', views.figures_detail, name='figures_detail'),
  path('figures/create/', views.FigureCreate.as_view(), name='figures_create'),
  path('figures/<int:pk>/update/', views.FigureUpdate.as_view(), name='figures_update'),
  path('figures/<int:pk>/delete/', views.FigureDelete.as_view(), name='figures_delete'),
  path('accounts/signup/', views.signup, name='signup'),
  path('comics/create/', views.ComicCreate.as_view(), name='comics_create'),
  path('comics/<int:pk>/', views.ComicDetail.as_view(), name='comics_detail'),
  path('comics/', views.ComicList.as_view(), name='comics_index'),
  path('comics/<int:pk>/update/', views.ComicUpdate.as_view(), name='comics_update'),
  path('comics/<int:pk>/delete/', views.ComicDelete.as_view(), name='comics_delete'),
  path('figures/<int:figure_id>/assoc_comic/<int:comic_id>/', views.assoc_comic, name='assoc_comic'),
  path('figures/<int:figure_id>/add_photo/', views.add_photo, name='add_photo'),
]