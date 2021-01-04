"""A10website URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.conf.urls import url
from django.contrib import admin
from django.urls import path,include
from rest_framework.documentation import include_docs_urls
from rest_framework_jwt.views import obtain_jwt_token
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    # path('admin/', admin.site.urls),
    path('docs',include_docs_urls(title='A10')),
    path('api-auth/',include('rest_framework.urls')),
    url(r'^api/bfx/user/', include('user.urls')),
    url(r'^api/bfx/search/', include('search.urls')),
    url(r'^api/bfx/searchTip/', include('searchTip.urls')),
    url(r'^api/bfx/search/cluster', include('clusterSearch.urls')),
    url(r'^api/bfx/info/', include('entInfo.urls')),
    url(r'^api/bfx/info/basic', include('entInfo.urls')),
    url(r'^api/bfx/upload', include('upload.urls')),
    url(r'^api/bfx/statistic/', include('statistic.urls')),
    url(r'^api/bfx/test', include('train.urls')),
    url(r'^api/bfx/dbupload', include('dbpredict.urls')),
]+ static(settings.STATIC_URL, document_root = settings.STATIC_ROOT)
