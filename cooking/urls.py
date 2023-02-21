from django.urls import path
from .views import *

urlpatterns = [
    path('', Home.as_view(), name='home'),
    path('category/<str:slug>', RecipeByCategory.as_view(), name='category'),
    path('tag/<str:slug>', RecipeByTag.as_view(), name='tag'),
    path('resipe/<str:slug>', Single.as_view(), name='recipe'),
    path('search/', Search.as_view(), name='search'),
    path('create-recipe', CreateRecipe.as_view(), name='create_recipe'),
    # path('add_ingredients/<str:slug>', AddIngredient.as_view(), name='add_ingredients'),
    path('add_ingredients/<str:slug>', add_ingredients, name='add_ingredients')
]
