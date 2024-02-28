from django.template import Library


register = Library()

@register.inclusion_tag('partials/navbar.html')
def navbar(request):
    return {'request': request}


@register.inclusion_tag('partials/navbar-authenticated.html')
def navbar_authenticated(request):
    return {'request': request}

