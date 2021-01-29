"""climanevada URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path

from django.views.generic import RedirectView
from django.conf import settings
from django.conf.urls import url, include
from django.conf.urls.static import static

from django.views.static import serve

from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from core import views as core


def staticfiles_urlpatterns(prefix=None):
    """
    Helper function to return a URL pattern for serving static files.
    """
    if prefix is None:
        prefix = settings.STATIC_URL
    return static(prefix, view=serve)

urlpatterns = [
    path('select2/', include('django_select2.urls')),
    path('admin/', admin.site.urls),
    path('', core.ClimateDataApp),
    path('stations/', core.ClimateDataApp),
    path('about/', core.About),
    path('variables-metadata/', core.metadata),
    path('stations-metadata/', core.metadata),
    path('networks-metadata/', core.metadata),
    path('favicon.ico',RedirectView.as_view(url='/static/images/favicon.ico')),
    path('stations-autocomplete/', core.StationsAutocomplete.as_view(), name='stations-autocomplete',),
    path('variables-autocomplete/', core.VariablesAutocomplete.as_view(), name='variables-autocomplete',),
    path('variable-type-autocomplete/', core.VariableTypeAutocomplete.as_view(), name='variable-type-autocomplete',),
    path('stations-leaflet-autocomplete/', core.StationsLeafletAutocomplete.as_view(), name='stations-leaflet-autocomplete',),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)  

urlpatterns += staticfiles_urlpatterns()