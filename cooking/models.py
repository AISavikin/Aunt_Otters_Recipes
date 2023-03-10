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

    def __str__(self):
        return self.title


class Recipe(models.Model):
    title = models.CharField(max_length=150, verbose_name='Название')
    description = models.TextField(blank=True, verbose_name='Описание')
    content = models.TextField(blank=True, verbose_name='Контент')
    date_added = models.DateField(auto_now_add=True)
    photo = models.ImageField(upload_to='photo/%Y/%m', blank=True, verbose_name='Фото')
    views = models.IntegerField(default=0, verbose_name='Кол-во просмотров')
    slug = models.SlugField(max_length=50, unique=True, verbose_name="Url")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата публикации')
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name='recipes', verbose_name='Категория')
    tags = models.ManyToManyField(Tag, blank=True, related_name='recipes', verbose_name='Тэг')
    spices = models.ManyToManyField(Spice, blank=True)
    video = models.CharField(max_length=800, verbose_name='Видео', blank=True)

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('recipe', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        super().save()
        if self.photo:
            img = Image.open(self.photo.path)

            if img.height > 700 or img.width > 700:
                output_size = (700, 700)
                img.thumbnail(output_size)
                img.save(self.photo.path)


class IngredientForRecipe(models.Model):
    ingredient = models.CharField(max_length=200, verbose_name='Ингредиент')
    amount = models.FloatField(default=0, verbose_name='Количество')
    unit = models.CharField(max_length=100, blank=True, verbose_name='Единица измерения')
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='ingredients', verbose_name='Рецепт')

    def __str__(self):
        return self.ingredient

    class Meta:
        ordering = ['recipe']
        verbose_name = 'Ингредиент для рецепта'
        verbose_name_plural = 'Ингредиенты для рецептов'


class Step(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='steps', verbose_name='Рецепт')
    content = models.TextField(blank=True, verbose_name='Контент')
    num = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.recipe} шаг {self.num}'

    class Meta:
        ordering = ['num']
        verbose_name = 'Шаг'
        verbose_name_plural = 'Шаги'


class ImageStep(models.Model):
    step = models.ForeignKey(Step, on_delete=models.CASCADE, related_name='images', verbose_name='Шаг')
    img_full_url = models.CharField(max_length=255, verbose_name='Url Полного изображения')
    img_middle_url = models.CharField(max_length=255, verbose_name='Url среднего изображения ')

    def __str__(self):
        return f'Шаг {self.step.num} для рецепта {self.step.recipe.title}'
