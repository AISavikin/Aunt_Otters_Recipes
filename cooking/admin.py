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





class StepInline(admin.TabularInline):
    model = Step
    fields = ('num', 'content', 'get_photo')
    readonly_fields = ('get_photo',)


    def get_photo(self, obj):
        res = ''
        for img_step in obj.images.all():

            if img_step.img_middle_url:
                res += f'<p><img src="{img_step.img_middle_url}" width="200"></p>'
        if res:
            return mark_safe(res)
        res = '-'
        return res

    get_photo.short_description = 'Фото'

class IngredientForRecipeAdmin(admin.ModelAdmin):
    list_display = ('ingredient', 'recipe', 'amount', 'unit')
    list_display_links = ('ingredient',)
    list_filter = ('recipe',)




class ImageStepAdmin(admin.ModelAdmin):
    list_display = ('get_recipe', 'get_step', 'get_photo')
    fields = ('step', 'img_middle_url', 'img_full_url', 'get_photo')
    readonly_fields = ('get_photo',)
    def get_photo(self, obj):
        if obj.img_middle_url:
            return mark_safe(f'<img src="{obj.img_middle_url}" width="400">')
        return '-'

    def get_step(self, obj):
        return obj.step.num

    def get_recipe(self, obj):
        return obj.step.recipe.title

class RecipeAdminForm(forms.ModelForm):
    # content = forms.CharField(widget=CKEditorUploadingWidget())

    class Meta:
        model = Recipe
        fields = '__all__'
class ImageStepInline(admin.TabularInline):
    model = ImageStep

class StepAdmin(admin.ModelAdmin):
    list_display = ('recipe', 'num', 'content', 'get_photo')
    list_filter = ('recipe', )
    inlines = [ImageStepInline]
    def get_photo(self, obj):
        res = ''
        imgs_url = [i.img_middle_url for i in obj.images.all()]
        for i in imgs_url:
            res += f'<img src="{i}" width="100">'
        if res:
            return mark_safe(res)
        return '-'


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}
    form = RecipeAdminForm
    list_display_links = ('title',)
    list_display = ('id', 'get_photo', 'title', 'category', 'get_tags', 'views', 'created_at')
    search_fields = ('title',)
    list_filter = ('category', 'tags')
    readonly_fields = ('views', 'created_at', 'get_photo')
    fields = [('title', 'slug', 'category'), ('description', 'photo'), ('tags', 'spices'), 'content', 'get_photo']
    inlines = [StepInline]
    @admin.display(description='Тэги')
    def get_tags(self, obj):
        return [i.title for i in obj.tags.all()]

    def get_photo(self, obj):
        if obj.photo:
            return mark_safe(f'<img src="{obj.photo.url}" width="50">')
        return '-'
admin.site.register(Category, CategoryAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(IngredientForRecipe, IngredientForRecipeAdmin)
admin.site.register(Spice)
admin.site.register(Step, StepAdmin)
admin.site.register(ImageStep, ImageStepAdmin)
