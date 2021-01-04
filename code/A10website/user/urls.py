from django.conf.urls import url
from django.urls import path, include
from rest_framework import routers
from rest_framework.routers import DefaultRouter

from rest_framework_jwt.views import obtain_jwt_token

from user import views

createUserViewRouter = routers.DefaultRouter() # 新增用户
createUserViewRouter.register('', views.createUser,)

from user.views import UserViewset

urlpatterns = [
    url(r'^login$', obtain_jwt_token),
    url('^register$',include(createUserViewRouter.urls)),
    url('^info$', views.UserViewset.as_view({'get':'retrieve'})),
    url(r'^logout$', views.logoutView.as_view())
]