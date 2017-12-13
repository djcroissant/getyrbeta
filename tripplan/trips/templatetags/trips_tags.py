from django import template

register = template.Library()

@register.filter(name="get_quantity")
def get_quantity(queryset, user):
    if queryset.filter(owner=user).count() > 0:
        return queryset.get(owner=user).quantity
    else:
        return 0
