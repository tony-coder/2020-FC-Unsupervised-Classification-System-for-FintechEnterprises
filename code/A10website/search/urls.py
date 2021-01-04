from django.conf.urls import url

from search import views

urlpatterns = [
    url(r'^$',views.SearchView.as_view({'post':'list'}),name='search'),
    url(r'^hot/$',views.HotEntView.as_view({'get':'list'}),name='hotEnt'),
]