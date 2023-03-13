from django.contrib import admin
from django import forms
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django.contrib.admin import AdminSite
from django.utils.safestring import mark_safe
from .models import *

# AdminSite.index_title = 'jhkjhkjhkjh'
# Register your models here.

class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}


class TagAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}


class RecipeAdminForm(forms.ModelForm):
    # content = forms.CharField(widget=CKEditorUploadingWidget())

    class Meta:
        model = Recipe
        fields = '__all__'

@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}
    form = RecipeAdminForm
    list_display_links = ('title',)
    list_display = ('id', 'get_photo', 'title', 'category', 'get_tags', 'views', 'created_at')
    search_fields = ('title',)
    list_filter = ('category', 'tags')
    readonly_fields = ('views', 'created_at', 'get_photo')
    fields = ['title', 'content', 'slug', ('get_photo', 'tags', 'spices'), 'category', 'description']

    @admin.display(description='Тэги')
    def get_tags(self, obj):
        return [i.title for i in obj.tags.all()]

    def get_photo(self, obj):
        if obj.photo:
            return mark_safe(f'<img src="{obj.photo.url}" width="50">')
        return '-'



    get_photo.short_description = 'Фото'

class IngredientForRecipeAdmin(admin.ModelAdmin):
    list_display = ('ingredient', 'recipe', 'amount', 'unit')
    list_display_links = ('ingredient',)
    list_filter = ('recipe',)


class SpiceAdmin(admin.ModelAdmin):
    pass

class StepAdmin(admin.ModelAdmin):
    list_display = ('recipe', 'num', 'content')

class ImageStepAdmin(admin.ModelAdmin):
    list_display = ('get_recipe', 'get_step')

    def get_step(self, obj):
        return obj.step.num

    def get_recipe(self, obj):
        return obj.step.recipe.title

admin.site.register(Category, CategoryAdmin)
admin.site.register(Tag, TagAdmin)
# admin.site.register(Recipe, RecipeAdmin)
admin.site.register(IngredientForRecipe, IngredientForRecipeAdmin)
admin.site.register(Spice, SpiceAdmin)
admin.site.register(Step, StepAdmin)
admin.site.register(ImageStep, ImageStepAdmin)
