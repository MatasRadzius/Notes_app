from django.urls import path
from django.contrib.auth import views as auth_views
from .views import RegisterView, index
from . import views


app_name = 'notes_app'

urlpatterns = [
    path('', auth_views.LoginView.as_view(template_name='notes_app/login.html'), name='login'),\
    path('index/', index, name='index'),
    path('create_note/', views.create_note, name='create_note'),
    
   
    
    # Category URL patterns
    path('category/create/', views.create_category, name='create_category'),
    path('category/edit/<int:category_id>/', views.edit_category, name='edit_category'),
    path('category/delete/<int:category_id>/', views.delete_category, name='delete_category'),
    path('categories/', views.categories, name='categories'),
    
    # Note URL patterns
    path('note/create/', views.create_note, name='create_note'),
    path('note/edit/<int:note_id>/', views.edit_note, name='edit_note'),
    path('notes/', views.notes, name='notes'),
    path('note/<int:note_id>/', views.note_detail, name='note_detail'),
    path('note/delete/<int:pk>/', views.delete_note, name='delete_note'),
   path('note/list/', views.index, name='note_list'),

    # Authentication URL patterns
    path('logout/', auth_views.LogoutView.as_view(next_page='notes_app:login'), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),

    
]