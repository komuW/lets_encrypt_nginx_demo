from django.conf import settings
from django.conf.urls import patterns, include, url

from django.contrib import admin

from lets_encrypt_demo.views import HomeView, VerifyWowsign


admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'config.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    #url(r'^$', include(admin.site.urls)),
    url(r'^$', HomeView.as_view(), name='home'),
    url(r'^haijachukuliwa.tk.html/?$', VerifyWowsign.as_view(), name='verifywowsign'),
)


admin.site.site_header = "Encrypted Demo- {0}".format(settings.STAGE)
