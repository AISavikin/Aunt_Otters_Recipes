from django import forms
from .models import IngredientForRecipe, Recipe


class AddIngredientForm(forms.Form):
    ingredient = forms.CharField(label='Ингредиент', widget=forms.TextInput(attrs={'class': 'form-control'}))
    amount = forms.FloatField(label='Количество', min_value=0, required=False, widget=forms.NumberInput(attrs={'class': 'form-control', 'value': 0}))
    unit = forms.CharField(label='Единицы измерения', required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))

class CreateRecipeForm(forms.ModelForm):
    class Meta:

        model = Recipe
        fields = ['title', 'description', 'content', 'slug', 'category', 'tags']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
            'slug': forms.TextInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'tags': forms.Select(attrs={'class': 'form-select', 'size': 10}),
            'photo': forms.FileInput(attrs={'class': 'form-file form-control'})
        }


