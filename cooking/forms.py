from django import forms
from .models import Ingredient, Recipe


class AddIngredientForm(forms.Form):
    ingredient = forms.CharField(label='Ингредиент', widget=forms.TextInput(attrs={'class': 'form-control'}))
    amount = forms.CharField(label='Количество', required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))

class CreateRecipeForm(forms.ModelForm):
    class Meta:

        model = Recipe
        fields = ['title', 'description', 'slug', 'category', 'tags']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
            'slug': forms.TextInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'tags': forms.Select(attrs={'class': 'form-select', 'size': 10}),
            'photo': forms.FileInput(attrs={'class': 'form-file form-control'})
        }


