from django import forms
from .models import RecipeForModerate


class AddIngredientForm(forms.Form):
    ingredient = forms.CharField(label='Ингредиент', widget=forms.TextInput(attrs={'class': 'form-control'}))
    amount = forms.CharField(label='Количество', required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))

class CreateRecipeForm(forms.ModelForm):
    class Meta:

        model = RecipeForModerate
        fields = ['title', 'description', 'content']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Напишите описание, пожалуйста у админа с этим сложности'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 7}),
        }


