from django import template
register = template.Library()
from pages.models import Message

@register.filter(name='unread_messages')
def unread_messages(user_id):

    unread_messages = Message.objects.filter(to_user_id_id=user_id, unread=1)
    if not unread_messages:
        return 0
    else:
        return len(unread_messages)