from django.conf.urls import patterns, include, url
from django.conf import settings

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    url(r'^index/(\w+)/(\d+)/$', 'webxplore.views.index', name='home'),

    url(r'^photo/(\d+)/(\w+)/$', 'webxplore.views.photo', name='photo'),

    url(r'^accounts/login/$', 'django.contrib.auth.views.login',
        {'template_name': 'accounts/login.html'},
        name='login'
    ),
    url(r'^accounts/logout/$', 'django.contrib.auth.views.logout',
        {'template_name': 'accounts/logged_out.html'},
        name='logout'
    ),
    
    # url(r'^phoxplore/', include('phoxplore.webxplore.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': settings.MEDIA_ROOT
        },
        name='media')
    )