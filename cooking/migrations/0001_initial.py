# Generated by Django 4.1.6 on 2023-03-16 07:44

import cooking.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('slug', models.SlugField(max_length=255, unique=True, verbose_name='Url')),
            ],
            options={
                'verbose_name': 'Категория',
                'verbose_name_plural': 'Категории',
                'db_table': 'categorys',
                'ordering': ['title'],
            },
        ),
        migrations.CreateModel(
            name='Recipe',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=150, verbose_name='Название')),
                ('description', models.TextField(blank=True, verbose_name='Описание')),
                ('date_added', models.DateField(auto_now_add=True)),
                ('photo', models.ImageField(blank=True, upload_to=cooking.models.recipe_step_directory_path, verbose_name='Фото')),
                ('views', models.IntegerField(default=0, verbose_name='Кол-во просмотров')),
                ('slug', models.SlugField(unique=True, verbose_name='Url')),
                ('video', models.CharField(blank=True, max_length=800, verbose_name='Видео')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='recipes', to='cooking.category', verbose_name='Категория')),
            ],
            options={
                'verbose_name': 'Рецепт',
                'verbose_name_plural': 'Рецепты',
                'db_table': 'recipes',
                'ordering': ['-date_added'],
            },
        ),
        migrations.CreateModel(
            name='Spice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=150)),
            ],
            options={
                'verbose_name': 'Специя',
                'verbose_name_plural': 'Специи',
                'db_table': 'spices',
                'ordering': ['title'],
            },
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
                ('slug', models.SlugField(unique=True, verbose_name='Url')),
            ],
            options={
                'verbose_name': 'Тег',
                'verbose_name_plural': 'Теги',
                'db_table': 'tags',
                'ordering': ['title'],
            },
        ),
        migrations.CreateModel(
            name='Step',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField(blank=True, verbose_name='Контент')),
                ('num', models.IntegerField(default=1, verbose_name='№')),
                ('recipe', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='steps', to='cooking.recipe', verbose_name='Рецепт')),
            ],
            options={
                'verbose_name': 'Шаг',
                'verbose_name_plural': 'Шаги',
                'db_table': 'steps',
                'ordering': ['num'],
            },
        ),
        migrations.AddField(
            model_name='recipe',
            name='spices',
            field=models.ManyToManyField(blank=True, to='cooking.spice'),
        ),
        migrations.AddField(
            model_name='recipe',
            name='tags',
            field=models.ManyToManyField(blank=True, related_name='recipes', to='cooking.tag', verbose_name='Тэг'),
        ),
        migrations.CreateModel(
            name='Ingredient',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ingredient', models.CharField(max_length=200, verbose_name='Ингредиент')),
                ('amount', models.CharField(max_length=200, verbose_name='Количество')),
                ('recipe', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ingredients', to='cooking.recipe', verbose_name='Рецепт')),
            ],
            options={
                'verbose_name': 'Ингредиент для рецепта',
                'verbose_name_plural': 'Ингредиенты для рецептов',
                'db_table': 'ingredients',
                'ordering': ['recipe'],
            },
        ),
        migrations.CreateModel(
            name='ImageStep',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('img', models.ImageField(blank=True, upload_to=cooking.models.image_step_directory_path, verbose_name='Фото')),
                ('step', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='cooking.step', verbose_name='Шаг')),
            ],
            options={
                'verbose_name': 'Изображение',
                'verbose_name_plural': 'Изображения',
                'db_table': 'image_steps',
            },
        ),
    ]
