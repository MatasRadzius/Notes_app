from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from .models import Category, Note
from .forms import CategoryForm, NoteForm
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView



def register(request):
    
    return render(request, 'notes_app/register.html')


class RegisterView(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('notes_app:index')  # Redirect to welcome instead of index
    template_name = 'registration/register.html'

    def form_valid(self, form):
        response = super().form_valid(form)
        user = form.save()
        login(self.request, user)
        return response

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('notes_app:index')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

LOGIN_REDIRECT_URL = 'notes_app:index'

@login_required
def create_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            category = form.save(commit=False)
            category.user = request.user
            category.save()
            return redirect(reverse('notes_app:index'))
    else:
        form = CategoryForm()
    
    context = {'form': form}
    return render(request, 'notes_app/create_category.html', context)

@login_required
def edit_category(request, category_id):
    category = get_object_or_404(Category, id=category_id, user=request.user)
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            return redirect('notes_app:index')
    else:
        form = CategoryForm(instance=category)
    return render(request, 'notes_app/edit_category.html', {'form': form})

@login_required
def delete_category(request, category_id):
    category = get_object_or_404(Category, id=category_id, user=request.user)
    if request.method == 'POST':
        category.delete()
        return redirect('notes_app:index')
    return render(request, 'notes_app/delete_category.html', {'category': category})

@login_required
def create_note(request):
    if request.method == "POST":
        form = NoteForm(request.POST, request.FILES)  # Add request.FILES
        if form.is_valid():
            note = form.save(commit=False)
            note.user = request.user
            note.save()
            return redirect('notes_app:index')  # Redirect to welcome instead of notes
    else:
        form = NoteForm()
    return render(request, 'notes_app/create_note.html', {'form': form})


@login_required
def edit_note(request, note_id):
    note = get_object_or_404(Note, id=note_id)

    if request.method == 'POST':
        form = NoteForm(request.POST, request.FILES, instance=note)
        if form.is_valid():
            note = form.save(commit=False)
            note.user = request.user
            note.save()
            return redirect(reverse('notes_app:index')) # use reverse to generate URL
    else:
        form = NoteForm(instance=note)

    return render(request, 'notes_app/edit_note.html', {'form': form, 'note': note})

@login_required
def delete_note(request, pk):
    note = get_object_or_404(Note, pk=pk)

    if request.method == 'POST':
        note.delete()
        return redirect('notes_app:index')  # Replace 'index' with the correct namespaced view name 'notes_app:index'

    return render(request, 'notes_app/delete_note.html', {'note': note})


@login_required
def categories(request):
    categories = Category.objects.filter(user=request.user)
    context = {'categories': categories}
    return render(request, 'notes_app/categories.html', context)

@login_required
def notes(request):
    user_notes = Note.objects.filter(user=request.user)
    context = {'notes': user_notes}
    return render(request, 'notes_app/notes.html', context)

def notes(request):
    user_notes = Note.objects.filter(user=request.user)
    print("User:", request.user)
    print("Notes count:", len(user_notes))
    for note in user_notes:
        print("Note:", note.name, "-", note.text)
    context = {'notes': user_notes}
    return render(request, 'notes_app/index.html', context)

def note_detail(request, note_id):
    note = get_object_or_404(Note, id=note_id)
    context = {'note': note}
    return render(request, 'notes_app/note_detail.html', context)

@login_required
def index(request):
    search_query = request.GET.get('search', '')
    category_filter = request.GET.get('category', '')

    categories = Category.objects.filter(user=request.user)
    notes = Note.objects.filter(user=request.user)

    if search_query:
        notes = notes.filter(title__icontains=search_query)

    if category_filter:
        notes = notes.filter(category__id=category_filter)

    context = {
        'notes': notes,
        'categories': categories,
        'search_query': search_query,
        'category_filter': category_filter,
    }
    return render(request, 'notes_app/index.html', context)