from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound, Http404
from django.shortcuts import render, get_object_or_404
from .models import Post
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.conf import settings
from django.contrib.auth.decorators import login_required
from taggit.models import Tag
from django.utils.http import urlunquote
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone
from meta.views import Meta
from paginator.utils import paginate

def PostIndex(request, tag_slug=None, cat_slug=None, author_user=None):
    meta = Meta(
        title="وبلاگ",
        description='پست های هفتگی انواع پروژه های مختلف اینترنت اشیا و هوش مصنوعی و طراحی سایت به همراه آموزش با پایتون ',
        keywords=['طراحی سایت', 'هوش مصنوعی', 'اینترنت اشیا'],
        locale= 'fa_IR'
    )
    posts = Post.objects.filter(
        status=1, published_date__lte=timezone.now()).order_by('-published_date')
    tag = None
    msg = None

    if tag_slug:
        tag = get_object_or_404(Tag, slug=urlunquote(tag_slug))
        posts = posts.filter(tags__in=[tag])
        msg = f"فیلتر شده بر اساس تگ: \"{urlunquote(tag_slug)}\""

    if cat_slug:
        posts = posts.filter(category__name=urlunquote(cat_slug))
        msg = f"فیلتر شده بر اساس دسته بندی: \"{urlunquote(cat_slug)}\""

    posts = paginate(request,posts,5)
    context = {"posts": posts,'tag': tag, "msg": msg, 'cat': cat_slug, "meta": meta}
    return render(request, "blog/blog_index.html", context)


def PostDetail(request, slug):
    post = get_object_or_404(Post, slug=urlunquote(
        slug), published_date__lte=timezone.now())
    context = {"post": post, "meta": post.as_meta()}
    return render(request, "blog/blog_single.html", context)
