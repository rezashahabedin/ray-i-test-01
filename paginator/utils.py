from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
# Create your views here.

def paginate(request,obj,quantity=6):
    paginator = Paginator(obj, quantity)
    page = request.GET.get('page')
    try:
        obj = paginator.page(page)
    except PageNotAnInteger:
        obj = paginator.page(1)
    except EmptyPage:
        obj = paginator.page(paginator.num_pages)

    return obj
