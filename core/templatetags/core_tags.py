from urllib.parse import urlparse, urlunparse
from django.http import QueryDict
from django import template


register = template.Library()


@register.simple_tag
def url_replace(request, **kwargs):
    """
    This tag can help us replace or add querystring
    TO replace the page field in URL
    {% url_replace request page=page_num %}
    """
    (scheme, netloc, path, params, query, fragment) = urlparse(request.get_full_path())
    query_dict = QueryDict(query, mutable=True)
    for key, value in kwargs.items():
        query_dict[key] = value
    query = query_dict.urlencode()
    return urlunparse((scheme, netloc, path, params, query, fragment))
