from django.conf.urls.defaults import patterns, url


project_pattern = '(?P<username>[\w]+)/(?P<shortcode>[-\w]+)'


urlpatterns = patterns(
    'popcorn_gallery.popcorn.views.projects',
    url(r'^projects/$', 'project_list', name='project_list'),
    url(r'^projects/category/(?P<slug>[\w-]+)/$', 'project_list',
        name='project_list_category'),
    )

urlpatterns += patterns(
    'popcorn_gallery.popcorn.views.projects',
    url(r'^templates/$', 'template_list', name='template_list'),
    url(r'^templates/category/(?P<slug>[\w-]+)/$', 'template_list',
        name='template_list_category'),
    url(r'^template/(?P<slug>[\w-]+)/$', 'template_detail',
        name='template_detail'),
    url(r'^template/(?P<slug>[\w-]+)/config$', 'template_config',
        name='template_config'),
    url(r'^template/(?P<slug>[\w-]+)/summary/$', 'template_summary',
        name='template_summary'),
    )


urlpatterns += patterns(
    'popcorn_gallery.popcorn.views.projects',
    url(r'^%s/$' % project_pattern, 'user_project', name='user_project'),
    url(r'^%s/config$' % project_pattern, 'user_project_config',
        name='user_project_config'),
    url(r'^%s/edit/$' % project_pattern, 'user_project_edit',
        name='user_project_edit'),
    url(r'^%s/meta/$' % project_pattern, 'user_project_meta',
        name='user_project_meta'),
    url(r'^%s/data/$' % project_pattern, 'user_project_data',
        name='user_project_data'),
    url(r'^%s/delete/$' % project_pattern, 'user_project_delete',
        name='user_project_delete'),
    )
