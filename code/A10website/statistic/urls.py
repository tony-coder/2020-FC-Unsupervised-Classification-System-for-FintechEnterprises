from django.conf.urls import url

from statistic import views

urlpatterns = [
    url(r'^chart$',views.chartView.as_view(),name='chart'),
    url(r'^2Dcluster$',views.cluster2DView.as_view(),name='2Dcluster'),
    url(r'^3Dcluster$',views.cluster3DView.as_view(),name='3Dcluster'),
    url(r'^bar$',views.barView.as_view(),name='bar'),
    url(r'^quantity$',views.quantityView.as_view(),name='quantity'),
    url(r'^modelParam$',views.weightView.as_view(),name='getparam'),

]