"""
URL configuration for main project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.conf import settings
from django.urls import path, include
from django.views.static import serve
from todo.views import HealthCheckView


def my_static(prefix, view=serve, **kwargs):
    """
    My own version of static because Django thinks I am not grown enough
    to decide if I want to serve my static files from Django in production

    copied from django/conf/urls/static.py
    """
    import re

    from django.urls import re_path

    return [
        re_path(
            r"^%s(?P<path>.*)$" % re.escape(prefix.lstrip("/")),
            view,
            kwargs=kwargs,
        ),
    ]

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include('social_site.urls')),
    path('api/v1/', include('todo.urls')),
    path('health/', HealthCheckView.as_view(), name='health-check'),
]

urlpatterns += my_static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += my_static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)