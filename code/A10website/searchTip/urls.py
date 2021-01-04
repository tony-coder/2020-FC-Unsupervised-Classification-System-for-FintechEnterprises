from django.conf.urls import url

from searchTip import views

urlpatterns = [
    url(r'^$',views.searchTipView.as_view({'post':'list'}),name='searchTip'),
]