import functools

from django.http import Http404, HttpResponseForbidden

from .baseconv import base62
from .models import Project

def valid_user_project(url_args):
    """Decorator that makes sure the project is active and valid.
    Takes a limited set of arguments ``username``, ``shortcode`` and ``uuid``

    Usage:
    @valid_user_project(url_args=['username', 'shortcode'])
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(request, *args, **kwargs):
            params = {}
            valid_args = {
                'username': 'author__username',
                'shortcode': 'pk',
                'uuid': 'uuid',
                }
            # use the args parameter to transform the arguments in
            # valid query values
            for arg in url_args:
                if not arg in valid_args:
                    raise Http404
                query_key = valid_args[arg]
                # short code needs to be converted into a valid pk
                if query_key == 'pk':
                    try:
                        params[query_key] = base62.to_decimal(kwargs.pop(arg))
                    except Exception:
                        raise Http404
                else:
                    params[query_key] = kwargs.pop(arg)
            # query with the available params
            try:
                project = (Project.objects.select_related('author', 'template')
                           .get(**params))
            except Project.DoesNotExist:
                raise Http404
            if not project.available_for(request.user):
                raise Http404
            return func(request, project=project, *args, **kwargs)
        return wrapper
    return decorator


def is_popcorn_project(func):
    """Decorator that makes sure that project was made with a
    popcorn ``Template`` """
    @functools.wraps(func)
    def wrapper(request, *args, **kwargs):
        project = kwargs.pop('project')
        if not project.template:
            raise Http404
        return func(request, project, *args, **kwargs)
    return wrapper
