from django.conf.urls import patterns, url

urlpatterns = patterns('control.views',
                       url(r'courses/$', 'courses'),
                       url(r'courses/(?P<course_id>\d+)/approve/', 'approve'),
                       url(r'feedbacks/$', 'feedbacks'),
                       url(r'$', 'index'),
)