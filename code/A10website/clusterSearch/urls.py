from django.conf.urls import url

from clusterSearch import views

urlpatterns = [
    url(r'^$',views.clusterSearchView.as_view({'post':'list'}),name='clusterSearch'),
]