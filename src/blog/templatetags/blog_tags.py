from django import template
from django.utils.safestring import mark_safe
from ..models import Post
import markdown


from django.contrib.flatpages.models import FlatPage

register = template.Library()

@register.simple_tag
def total_posts():
    return Post.published.count()
    
@register.inclusion_tag('blog/post/latest_posts.html')
def show_latest_posts(count=5):
    latest_posts = Post.published.order_by('-publish')[:count]
    return {'latest_posts': latest_posts}

@register.inclusion_tag("tags/footer.html")
def footer_links():
    flatpage_list = FlatPage.objects.all()
    return {'flatpage_list': flatpage_list }


@register.filter(name='markdown')
def markdown_format(text):
    return mark_safe(markdown.markdown(text))



