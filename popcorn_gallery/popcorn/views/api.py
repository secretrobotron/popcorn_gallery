import json

from django.conf import settings
from django.core.serializers.json import DjangoJSONEncoder
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST, require_GET
from django.http import HttpResponse, Http404

from ..forms import ProjectForm
from ..models import Project
from ...base.decorators import json_handler, login_required_ajax


@require_GET
@login_required_ajax
@login_required
def project_list(request):
    """List of the projects that belong to a User"""
    object_list = []
    for p in Project.objects.filter(author=request.user):
        object_list.append({'name': p.name, 'id': p.uuid})
    response = {
        'error': 'okay',
        'projects': object_list,
        }
    return HttpResponse(json.dumps(response, cls=DjangoJSONEncoder),
                        mimetype='application/json')


def save_project(json_data, user):
    """Helper to save the project"""
    form = ProjectForm(json_data)
    if form.is_valid():
        data = {
            'name': form.cleaned_data['name'],
            'metadata': form.cleaned_data['data'],
            'html': '',
            'author': user,
            'template': form.cleaned_data['template'],
            }
        project = Project.objects.create(**data)
        response = {
            'error': 'okay',
            'project': project.butter_data,
            }
    else:
        response = {'error': 'error'}
    return response


@require_POST
@json_handler
@login_required_ajax
@login_required
def project_add(request):
    """End point for adding a ``Project``"""
    response = save_project(request.JSON, request.user)
    return HttpResponse(json.dumps(response, cls=DjangoJSONEncoder),
                        mimetype='application/json')


@json_handler
@login_required_ajax
@login_required
def project_detail(request, uuid):
    """Handles the data for the Project"""
    if request.method == 'POST' and request.JSON:
        response = save_project(request.JSON, request.user)
        return HttpResponse(json.dumps(response, cls=DjangoJSONEncoder),
                            mimetype='application/json')
    try:
        project = Project.objects.get(uuid=uuid, author=request.user)
    except Project.DoesNotExist:
        return Http404()
    response = {
        'error': 'okay',
        # Butter needs the project metadata as a string that can be
        # parsed to JSON
        'url': project.get_absolute_url(),
        'project': project.metadata,
        }
    return HttpResponse(json.dumps(response, cls=DjangoJSONEncoder),
                        mimetype='application/json')


@json_handler
@login_required_ajax
@login_required
def project_publish(request, uuid):
    if request.method == 'POST':
        try:
            project = Project.objects.get(uuid=uuid, author=request.user)
        except Project.DoesNotExist:
            return Http404()
        project.is_shared = True
        response = {
            'error': 'okay',
            'url': '%s%s' % (settings.SITE_URL, project.get_absolute_url()),
            }
        return HttpResponse(json.dumps(response, cls=DjangoJSONEncoder),
                            mimetype='application/json')
    raise Http404
