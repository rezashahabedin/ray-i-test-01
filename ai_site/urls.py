"""ai_site URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.sitemaps.views import sitemap
from blog.sitemaps import PostSitemap
from website.sitemaps import StaticViewSitemap
from django.views.generic import TemplateView
from django.conf.urls import (
    handler400, handler403, handler404, handler500
)

sitemaps = {
    "posts": PostSitemap,
    "static": StaticViewSitemap,
}
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('website.urls', namespace='website')),
    path('blog/', include('blog.urls', namespace='blog')),
    

    path('ckeditor/', include('ckeditor_uploader.urls')),
    path("sitemap.xml", sitemap, {"sitemaps": sitemaps}, name="sitemap"),
    path('djga/', include('google_analytics.urls')),
    path('robots.txt', include('robots.urls')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

handler400 = 'website.views.error_400'  # bad_request
handler403 = 'website.views.error_403'  # permission_denied
handler404 = 'website.views.error_404'  # page_not_found
handler500 = 'website.views.error_500'  # server_error


