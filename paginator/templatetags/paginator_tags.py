from django import template
from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


register = template.Library()


@register.inclusion_tag('paginator/paginator.html',takes_context=True)
def paginate(context,obj):
    return {'obj':obj}