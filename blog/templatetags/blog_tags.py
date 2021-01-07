from django import template
from blog.models import Post,Category
from django.contrib.auth.models import User
from django.utils.html import strip_spaces_between_tags, strip_tags
from django.utils.text import Truncator
from django.utils import timezone

register = template.Library()

#@register.filter(name="cut")
def cut(value,arg):
    return value.replace(arg,"")

register.filter('cut',cut)

@register.simple_tag
def total_posts():
    return Post.objects.filter(status=1,published_date__lte=timezone.now()).count()



@register.inclusion_tag('blog/latest_posts.html')
def show_latest_posts(count=3):
    latest_posts = Post.objects.filter(status=1,published_date__lte=timezone.now()).order_by('-published_date')[:count]
    return {'latest_posts':latest_posts}


@register.inclusion_tag('blog/blog_categories.html')
def show_blog_categories():
    posts = Post.objects.filter(status=1,published_date__lte=timezone.now()).order_by('-published_date')
    categories = Category.objects.all()
    categories_dict={}
    for category in categories:
        counted = posts.filter(category__name=category.name).count()
        if counted >0:
            categories_dict[category.name] = counted

    return {'categories':categories_dict}

# use this as snippet or
# this: {{ page.body|striptags|truncatewords:50 }}
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
