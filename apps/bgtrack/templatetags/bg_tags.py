from django import template
register = template.Library()

@register.filter(name='bg_average')
def bg_average(user,days=None):
    return user.get_average(days=days)