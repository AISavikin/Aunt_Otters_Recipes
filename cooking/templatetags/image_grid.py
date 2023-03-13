from django import template
from cooking.models import Step

register = template.Library()

@register.inclusion_tag('cooking/img_grid_tpl.html')
def get_image_grid(pk):
    images = Step.objects.get(pk=pk).images.all()
    return {'images': images}