from django import template
from ..models import NewsUsers




register = template.Library()


@register.inclusion_tag('tags/subscribe.html')
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


