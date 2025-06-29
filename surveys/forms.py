from django import forms
from .models import Tag


class TagForm(forms.ModelForm):
    class Meta:
        model = Tag
        fields = ['name', 'category']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'w-full border border-gray-300 rounded px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent'
            }),
            'category': forms.Select(attrs={
                'class': 'w-full border border-gray-300 rounded px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent'
            })
        }
