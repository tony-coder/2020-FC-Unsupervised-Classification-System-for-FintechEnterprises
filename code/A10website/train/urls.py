from django.conf.urls import url

from train import views

urlpatterns = [
    url(r'^/train$',views.trainView.as_view(), name='train'),
    url(r'^/predict$',views.predictView.as_view(), name='predict'),
]