from django.conf.urls import patterns, include, url

urlpatterns = patterns('instructor.views',
                       url(r'^courses/new/$', 'add_course', name='add_course'),
                       url(r'^courses/(?P<course_id>\d+)/$', 'course', name='course'),
                       url(r'^courses/(?P<course_id>\d+)/tab/(?P<tab>\w+)/$', 'course', name='course'),
                       url(r'^courses/(?P<course_id>\d+)/edit/$', 'edit_course', name='edit_course'),
                       url(r'^courses/(?P<course_id>\d+)/delete/$', 'delete_course', name='delete_course'),
                       url(r'^courses/(?P<course_id>\d+)/materials/information/add/$', 'add_information', name='add_information'),
                       url(r'^courses/(?P<course_id>\d+)/materials/information/(?P<info_id>\d+)/edit/$', 'edit_information', name='edit_information'),
                       url(r'^courses/(?P<course_id>\d+)/materials/information/(?P<info_id>\d+)/delete/$', 'delete_information', name='delete_information'),
                       url(r'^courses/$', 'courses', name='courses'),
                       )