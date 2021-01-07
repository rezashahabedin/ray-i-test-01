from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from ckeditor_uploader.fields import RichTextUploadingField
from taggit.managers import TaggableManager
from django.utils.http import urlunquote
from imagekit.models import ImageSpecField
from pilkit.processors import Thumbnail
from django.utils import timezone
from django.utils.html import strip_spaces_between_tags, strip_tags
from django.utils.text import Truncator
from meta.models import ModelMeta

STATUS = ((0, "Draft"), (1, "Publish"))


class Category(models.Model):
    name = models.CharField(max_length=200, unique=True)

    def __str__(self):
        return self.name

class Post(ModelMeta,models.Model):
    title = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True, allow_unicode=True,
                            help_text="The name of the page as it will appear in URLs e.g http://domain.com/blog/[my-slug]/")
    image = models.ImageField(upload_to='Images/blog_thumbs',
                              default='Images/blog_thumbs/default.png', blank=True)
    image_alt = models.CharField(max_length=200, blank=True)
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='blog_posts')
    content = RichTextUploadingField()

    category = models.ManyToManyField(Category)
    tags = TaggableManager()
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    published_date = models.DateTimeField(blank=True,default=timezone.now)
    status = models.IntegerField(choices=STATUS, default=0)

    image_large = ImageSpecField(source='image',
                                  processors=[Thumbnail(750, 440)],
                                  format='JPEG',
                                  options={'quality': 60})
    image_medium = ImageSpecField(source='image',
                                  processors=[Thumbnail(200, 200)],
                                  format='JPEG',
                                  options={'quality': 60})
    image_small = ImageSpecField(source='image',
                                 processors=[Thumbnail(150, 150)],
                                 format='JPEG',
                                 options={'quality': 60})


    _metadata = {
    'title': 'title',
    'description': 'get_meta_content',
    'image': 'get_meta_image',
    'published_time': 'published_date',
    'modified_time': 'updated_date',
    'url': 'get_absolute_url',
    'locale': 'fa_IR',
    'keywords':'get_meta_keywords'

    }
    
    def get_meta_content(self):
        value = strip_spaces_between_tags(self.content)
        value = value.replace("</p>"," </p>")
        value = value.replace("&quot","  ")
        value = strip_tags(value)
        return Truncator(value).words(40)

    def get_meta_image(self):
        if self.image:
            return self.image.url

    class Meta:
        ordering = ['-created_date']

    def __str__(self):
        return self.slug

    def snippet(self):
        return self.content[:100]+" ..."

    def get_meta_keywords(self):
        return [tag.name for tag in self.tags.all()]

    def get_absolute_url(self):
        return urlunquote(reverse("blog:single", kwargs={"slug": str(self.slug)}))
        # return reverse("blog:single", kwargs={"pk": self.pk})


