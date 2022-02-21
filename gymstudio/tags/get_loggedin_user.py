from django import template
register = template.Library()

from ..models import User

@register.simple_tag
def fetch_user(user_id=24):
    user = User.objects
    auth = user.get(id=user_id)
    return auth