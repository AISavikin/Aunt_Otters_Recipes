from django.contrib import admin
from django.contrib.admin import AdminSite
from django.utils.safestring import mark_safe
from .models import *


# AdminSite.index_title = 'jhkjhkjhkjh'
# Register your models here.

class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}


class TagAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}


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


class ImageStepInline(admin.TabularInline):
    model = ImageStep


class StepAdmin(admin.ModelAdmin):
    list_display = ('recipe', 'num', 'content', 'get_photo')
    list_filter = ('recipe',)
    inlines = [ImageStepInline]

    def get_photo(self, obj):
        images = [f'<img src="{i.img_middle_url}" width="100">' for i in obj.images.all()]
        if images:
            return mark_safe(''.join(images))
        return '-'

class IngredientsInline(admin.TabularInline):
    model = IngredientForRecipe
    classes = ('collapse',)

class StepInline(admin.TabularInline):
    model = Step
    fields = ('num', 'content', 'get_photo')
    readonly_fields = ('get_photo',)
    show_change_link = True
    classes = ('collapse', )

    def get_photo(self, obj):
        images = [f'<p><img src="{i.img_middle_url}" width="200"></p>' for i in obj.images.all()]
        if images:
            return mark_safe(''.join(images))
        return '-'

    get_photo.short_description = 'Фото'


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}
    list_display_links = ('title',)
    list_display = ('id', 'get_photo', 'title', 'category', 'get_tags', 'views', 'created_at')
    search_fields = ('title',)
    list_filter = ('category', 'tags')
    readonly_fields = ('views', 'created_at', 'get_photo')
    fieldsets = (
        ('Общее', {'fields': (('title', 'slug', 'category', 'content', 'video'),)}),
        ('Теги', {'fields': (('tags', 'spices'),), 'classes': ('collapse',),}),
    )
    inlines = [StepInline, IngredientsInline]

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
