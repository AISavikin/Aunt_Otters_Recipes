from django import template
from django.db.models import Count

from cooking.models import *

register = template.Library()

@register.inclusion_tag('cooking/right_menu_tpl.html')
def show_menu_cat():
    categories = Category.objects.annotate(cnt=Count('recipes'))
    tags = Tag.objects.all()
    popular = Recipe.objects.order_by('-views')[:3]
    return {'categories': categories, 'tags': tags, 'popular': popular}

