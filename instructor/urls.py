from django.conf.urls import patterns, include, url

urlpatterns = patterns('instructor.views',
                       url(r'^courses/new/$', 'add_course'),
                       url(r'^courses/(?P<course_id>\d+)/$', 'course'),
                       url(r'^courses/(?P<course_id>\d+)/tab/(?P<tab>\w+)/$', 'course'),
                       url(r'^courses/(?P<course_id>\d+)/edit/$', 'edit_course'),
                       url(r'^courses/(?P<course_id>\d+)/delete/$', 'delete_course'),
                       url(r'^courses/$', 'courses'),

                       url(r'^courses/(?P<course_id>\d+)/materials/news/add/$', 'add_news'),
                       url(r'^courses/(?P<course_id>\d+)/materials/news/(?P<info_id>\d+)/edit/$', 'edit_news'),
                       url(r'^courses/(?P<course_id>\d+)/materials/news/(?P<info_id>\d+)/delete/$', 'delete_news'),

                       url(r'^courses/(?P<course_id>\d+)/materials/videos/add/$', 'add_video'),
                       url(r'^courses/(?P<course_id>\d+)/materials/videos/(?P<video_id>\d+)/edit/$', 'edit_video'),
                       url(r'^courses/(?P<course_id>\d+)/materials/videos/(?P<video_id>\d+)/delete/$', 'delete_video'),

                       url(r'^courses/(?P<course_id>\d+)/materials/files/add/$', 'add_file'),
                       url(r'^courses/(?P<course_id>\d+)/materials/files/(?P<file_id>\d+)/edit/$', 'edit_file'),
                       url(r'^courses/(?P<course_id>\d+)/materials/files/(?P<file_id>\d+)/delete/$', 'delete_file'),
                       )