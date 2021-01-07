from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from datetime import datetime, timedelta, timezone, tzinfo
from ckeditor_uploader.fields import RichTextUploadingField
from taggit.managers import TaggableManager
from django.urls import reverse
from io import BytesIO
from PIL import Image
from django.core.files import File
from django.utils.http import urlunquote
from imagekit.models import ImageSpecField
from pilkit.processors import Thumbnail
from django.utils import timezone
from django.utils.html import strip_spaces_between_tags, strip_tags
from django.utils.text import Truncator
from meta.models import ModelMeta


STATUS = ((0, "Draft"), (1, "Publish"))


class Ticket(models.Model):
    ticket_CHOICES = (
		(1, 'ارتباط با ما'),
		(2, 'دوره های آنلاین'),
        (3, 'سفارش پروژه'),
	)
    name = models.CharField(max_length=200)
    #family_name = models.CharField(max_length=200)
    email = models.EmailField(default=None)
    phone_number = models.CharField(max_length=200,blank=True)
    #subject =  models.CharField(max_length=200)
    ticket_type = models.PositiveSmallIntegerField(choices=ticket_CHOICES,default=1,blank=True)
    body = models.TextField()
    checked = models.BooleanField(default=False)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_date']

    def __str__(self):
        return self.name

