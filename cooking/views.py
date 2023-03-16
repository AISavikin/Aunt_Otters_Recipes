from django.db.models import F, Q
from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, CreateView, FormView
from django.views.generic.edit import FormMixin

from .models import *
from .forms import AddIngredientForm, CreateRecipeForm


class Home(ListView):
    model = Recipe
    template_name = 'cooking/index.html'
    paginate_by = 8
    context_object_name = 'recipes'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Главная страница'

        return context


class RecipeByCategory(ListView):
    template_name = 'cooking/index.html'
    paginate_by = 10
    context_object_name = 'recipes'

    def get_queryset(self):
        return Recipe.objects.filter(category__slug=self.kwargs['slug'])

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = Category.objects.get(slug=self.kwargs['slug'])
        return context


class RecipeByTag(ListView):
    template_name = 'cooking/index.html'
    paginate_by = 10
    context_object_name = 'recipes'

    def get_queryset(self):
        return Recipe.objects.filter(tags__slug=self.kwargs['slug'])

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = Tag.objects.get(slug=self.kwargs['slug'])
        return context


class Single(DetailView):
    model = Recipe
    template_name = 'cooking/single.html'
    context_object_name = 'recipe'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.object.title
        self.object.views = F('views') + 1
        self.object.save()
        self.object.refresh_from_db()
        return context


class CreateRecipe(CreateView):
    template_name = 'cooking/create-recipe.html'
    model = Recipe
    form_class = CreateRecipeForm


class Search(ListView):
    template_name = 'cooking/index.html'
    paginate_by = 15
    context_object_name = 'recipes'

    def get_queryset(self):
        query = self.request.GET.get('s')
        title = Recipe.objects.filter(title__icontains=query)
        ings = Recipe.objects.filter(ingredients__ingredient__icontains=query)
        step = Recipe.objects.filter(steps__content__icontains=query)
        return title.union(ings, step)
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['s'] = f's={self.request.GET.get("s")}&'
        return context


def add_ingredients(request, slug):
    recipe = Recipe.objects.get(slug=slug)
    if request.method == 'POST':
        form = AddIngredientForm(request.POST)
        if form.is_valid():
            form.cleaned_data['recipe'] = recipe
            Ingredient.objects.create(**form.cleaned_data)
            form = AddIngredientForm()
    else:
        form = AddIngredientForm()
    return render(request, 'cooking/add_ingredients.html', {'form': form, 'recipe': recipe})
