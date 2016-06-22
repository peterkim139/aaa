from django import template
register = template.Library()


@register.filter(name='user_online')
def user_online(thread):

    return thread.online(thread.email)
