from django.conf.urls import patterns, include, url

from django.contrib import admin
from accounts.forms import ExtendedAuthenticationForm

admin.autodiscover()

urlpatterns = patterns('',
                       url(r'^login/$', 'django.contrib.auth.views.login',
                           {'template_name': 'accounts/login.html', 'authentication_form': ExtendedAuthenticationForm}),
                       url(r'^logout/$', 'django.contrib.auth.views.logout', {'next_page': '/'}),
                       url(r'^password_change/$', 'django.contrib.auth.views.password_change',
                           {'template_name': 'accounts/password_change_form.html'}),
                       url(r'^password_change/done/$', 'django.contrib.auth.views.password_change_done',
                           {'template_name': 'accounts/password_change_done.html'}),
                       url(r'^signup/$', 'accounts.views.signup', {'template_name': 'accounts/signup.html',
                                                                   'email_template_name': 'accounts/signup_email.html'}),
                       url(r'^signup/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$', 'accounts.views.signup_confirm'),
                       url(r'^password_reset/$', 'django.contrib.auth.views.password_reset',
                           {'template_name': 'accounts/password_reset_form.html',
                            'email_template_name': 'accounts/password_reset_email.html'}),
                       url(r'^password_reset/done/$', 'django.contrib.auth.views.password_reset_done',
                           {'template_name': 'accounts/password_reset_done.html'}),
                       url(r'^reset/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$',
                           'django.contrib.auth.views.password_reset_confirm',
                           {'template_name': 'accounts/password_reset_confirm.html'}),
                       url(r'^reset/done/$', 'django.contrib.auth.views.password_reset_complete',
                           {'template_name': 'accounts/password_reset_complete.html'}),
                       url(r'^profile/$', 'accounts.views.profile', {'template_name': 'accounts/profile.html'}),
                       # remove this later
                       url(r'^init/$', 'accounts.views.init')
)

urlpatterns += patterns('', url(r'^admin/', include(admin.site.urls)))