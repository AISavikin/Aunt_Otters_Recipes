from PIL import Image
from django.db import models
from django.urls import reverse


class Category(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, verbose_name="Url")

    class Meta:
        ordering = ['title']
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        db_table = 'categorys'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('category', kwargs={'slug': self.slug})


class Tag(models.Model):
    title = models.CharField(max_length=50)
    slug = models.SlugField(max_length=50, unique=True, verbose_name="Url")

    class Meta:
        ordering = ['title']
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'
        db_table = 'tags'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('tag', kwargs={'slug': self.slug})


class Spice(models.Model):
    title = models.CharField(max_length=150)

    class Meta:
        verbose_name = 'Специя'
        verbose_name_plural = 'Специи'
        ordering = ['title']
        db_table = 'spices'

    def __str__(self):
        return self.title


def recipe_step_directory_path(instance, filename: str):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    ext = filename.split('.')[-1]
    return f'photo/{instance}/main.{ext}'


class Recipe(models.Model):
    title = models.CharField(max_length=150, verbose_name='Название')
    description = models.TextField(blank=True, verbose_name='Описание')
    date_added = models.DateField(auto_now_add=True)
    photo = models.ImageField(upload_to=recipe_step_directory_path, blank=True, verbose_name='Фото')
    views = models.IntegerField(default=0, verbose_name='Кол-во просмотров')
    slug = models.SlugField(max_length=50, unique=True, verbose_name="Url")
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name='recipes', verbose_name='Категория')
    tags = models.ManyToManyField(Tag, blank=True, related_name='recipes', verbose_name='Тэг')
    spices = models.ManyToManyField(Spice, blank=True)
    video = models.CharField(max_length=800, verbose_name='Видео', blank=True)

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'
        ordering = ['-date_added']
        db_table = 'recipes'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('recipe', kwargs={'slug': self.slug})




class Ingredient(models.Model):
    num = models.IntegerField(verbose_name='№', default=1)
    ingredient = models.CharField(max_length=200, verbose_name='Ингредиент')
    amount = models.CharField(max_length=200, verbose_name='Количество', blank=True)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='ingredients', verbose_name='Рецепт')

    def __str__(self):
        return self.ingredient

    class Meta:
        ordering = ['num', 'pk']
        verbose_name = 'Ингредиент для рецепта'
        verbose_name_plural = 'Ингредиенты для рецептов'
        db_table = 'ingredients'


class Step(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='steps', verbose_name='Рецепт')
    content = models.TextField(blank=True, verbose_name='Контент')
    num = models.IntegerField(default=1, verbose_name='№')

    def __str__(self):
        return f'{self.recipe} шаг {self.num}'

    class Meta:
        ordering = ['num']
        verbose_name = 'Шаг'
        verbose_name_plural = 'Шаги'
        db_table = 'steps'


def image_step_directory_path(instance, filename: str):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    ext = filename.split('.')[-1]
    return f'photo/{instance.step.recipe}/{instance.step}.{ext}'


class ImageStep(models.Model):
    step = models.ForeignKey(Step, on_delete=models.CASCADE, related_name='images', verbose_name='Шаг')
    img = models.ImageField(upload_to=image_step_directory_path, blank=True, verbose_name='Фото')

    class Meta:
        verbose_name = 'Изображение'
        verbose_name_plural = 'Изображения'
        db_table = 'image_steps'

    def save(self, *args, **kwargs):
        super().save()
        if self.img:
            img = Image.open(self.img.path)
            if img.height > 740 or img.width > 740:
                output_size = (740, 740)
                img.thumbnail(output_size)
                img.save(self.img.path)

    def __str__(self):
        return f'Шаг {self.step.num} для рецепта {self.step.recipe.title}'

class RecipeForModerate(models.Model):
    title = models.CharField(max_length=255, verbose_name='Название')
    description = models.TextField(blank=True, verbose_name='Описание')
    content = models.TextField(blank=True, verbose_name='Контент')

    class Meta:
        verbose_name = 'Рецепт для модерации'
        verbose_name_plural = 'Рецепт для модерации'
        db_table = 'recipes_for_moderate'

    def __str__(self):
        return self.title

