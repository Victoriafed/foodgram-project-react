
from django import template

register = template.Library()

@register.simple_tag
def IngredientFilter(char):
    return IngredientFilter.objects.filter(name__startswith=char)