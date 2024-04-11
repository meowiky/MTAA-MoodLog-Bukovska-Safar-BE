from django.urls import path
from . import views
from .views import create_tag

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('entries/create/', views.create_diary_entry, name='create_diary_entry'),
    path('entries/<int:entry_id>/modify/', views.modify_diary_entry, name='modify_diary_entry'),
    path('entries/<int:entry_id>/add_tag/', views.add_tag, name='add_tag'),
    path('tags/create/', create_tag, name='create_tag'),
]