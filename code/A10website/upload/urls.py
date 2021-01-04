from django.conf.urls import url

from upload import views

urlpatterns = [
    url(r'^/train$',views.upload_file_train, name='file_train'),
    url(r'^/predict$',views.upload_file_predict, name='file_predict'),
]