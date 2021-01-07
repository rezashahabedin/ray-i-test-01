from django import template
from blog.models import Post
import random
from django.utils.html import strip_spaces_between_tags, strip_tags
from django.utils.text import Truncator
from django.contrib.auth.models import User
from ipaddress import IPv4Network,IPv4Address
from django.utils import timezone

register = template.Library()

@register.inclusion_tag('website/latest_posts.html')
def show_latest_posts(count=4):
    latest_posts = Post.objects.filter(status=1, published_date__lte=timezone.now()).order_by('-published_date')[:count]
    return {'latest_posts':latest_posts}


@register.filter(name='excerpt')
def excerpt_with_ptag_spacing(value, arg):
    try:
        limit = int(arg)
    except ValueError:
        return 'Invalid literal for int().'

    # remove spaces between tags
    value = strip_spaces_between_tags(value)

    # add space before each P end tag (</p>)
    value = value.replace("</p>"," </p>")
    value = value.replace("&quot","  ")
    # strip HTML tags
    value = strip_tags(value)

    # other usage: return Truncator(value).words(length, html=True, truncate=' see more')
    return Truncator(value).words(limit)

