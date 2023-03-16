from django.contrib import admin
from django.contrib.admin import AdminSite
from django import forms
from django.utils.safestring import mark_safe
from .models import *


# AdminSite.index_title = 'jhkjhkjhkjh'
# Register your models here.

class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}


class TagAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('ingredient', 'recipe', 'amount')
    list_display_links = ('ingredient',)
    list_filter = ('recipe',)



class ImageStepInline(admin.TabularInline):
    model = ImageStep


class StepAdmin(admin.ModelAdmin):
    list_display = ('recipe', 'num', 'content', 'get_photo')
    list_filter = ('recipe',)
    fields = ('recipe', ('num', 'content'), 'get_photo' )
    readonly_fields = ('get_photo', )
    inlines = [ImageStepInline]

    def get_photo(self, obj):
        images = [f'<img src="{i.img.url}" width="300"> ' for i in obj.images.all()]
        if images:
            return mark_safe(''.join(images))
        return '-'

class IngredientsInline(admin.TabularInline):
    model = Ingredient
    classes = ('collapse',)

# class StepAdminForm(forms.ModelForm):
#     img_step = forms.ImageField(required=False)
#     class Meta:
#         model = ImageStep
#         fields = ('img',)

class StepInline(admin.TabularInline):
    model = Step
    fields = ('num', 'content', 'get_photo')
    readonly_fields = ('get_photo',)
    show_change_link = True
    classes = ('collapse', )
    # form = StepAdminForm

    def get_photo(self, obj):
        images = [f'<p><img src="{i.img.url}" width="200"></p>' for i in obj.images.all()]
        if images:
            return mark_safe(''.join(images))
        return '-'

    get_photo.short_description = 'Фото'


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}
    list_display_links = ('title',)
    list_display = ('id', 'get_photo', 'title', 'category', 'get_tags', 'views')
    search_fields = ('title',)
    list_filter = ('category', 'tags')
    readonly_fields = ('views', 'get_photo')
    fieldsets = (
        ('Общее', {'fields': (('title', 'slug', 'category', 'description', 'video', 'photo'),)}),
        ('Теги', {'fields': (('tags', 'spices'),), 'classes': ('collapse',),}),
    )
    inlines = [StepInline, IngredientsInline]
    save_on_top = True
    @admin.display(description='Тэги')
    def get_tags(self, obj):
        return [i.title for i in obj.tags.all()]

    def get_photo(self, obj):
        if obj.photo:
            return mark_safe(f'<img src="{obj.photo.url}" width="50">')
        return '-'

admin.site.register(Category, CategoryAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Spice)
admin.site.register(Step, StepAdmin)
