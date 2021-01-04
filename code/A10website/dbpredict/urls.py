from django.conf.urls import url

from dbpredict import views

urlpatterns = [
    url(r'^$',views.dbpredict,name='dbpredict'),
]