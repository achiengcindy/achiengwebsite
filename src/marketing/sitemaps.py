from django.contrib.sitemaps import Sitemap
from django.contrib.flatpages.models import FlatPage
from blog.models import Post, Category


class PostSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.9


    def items(self):
        return Post.published.all()

    def lastmod(self, obj):
        return obj.publish

    def location(self, obj):
        return obj.get_permalink_url()


class CategorySitemap(Sitemap):
    def items(self):
        return Category.active.all()


class FlatPageSitemap(Sitemap):
    def items(self):
        return FlatPage.objects.all()

