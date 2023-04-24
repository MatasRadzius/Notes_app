from django import forms
from .models import Note, Category

class NoteForm(forms.ModelForm):
    title = forms.CharField(label='Title', max_length=200)
    text = forms.CharField(label='Text', widget=forms.Textarea)
    image = forms.ImageField(label='Choose Image', required=False)
    category = forms.ModelChoiceField(label='Choose Category', queryset=Category.objects.all(), required=False)

    class Meta:
        model = Note
        fields = ['title', 'text', 'image', 'category']
        widgets = {
            'category': forms.Select(attrs={'class': 'form-control'}, choices=[('', '----')] + [(c.id, c.name) for c in Category.objects.all()]),
        }

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']
