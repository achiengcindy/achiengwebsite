from django.conf import settings

def mysite(request):
    return {
    'site_name': settings.SITE_NAME,
    'meta_description': settings.META_DESCRIPTION,
    'request': request
    }