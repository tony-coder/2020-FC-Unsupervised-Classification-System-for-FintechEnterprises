from django.contrib.auth import logout
from django.http import JsonResponse
#from rest_framework import mixins, viewsets, serializers, permissions, authentication
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework import mixins, viewsets, serializers, permissions, authentication, status
from rest_framework.response import Response
from user import models
from user.models import UserProfile
from rest_framework.views import APIView
from rest_framework.utils import json

def jwt_response_payload_error_handler(serializer, request = None):
    
    results = {
        "msg": "用户名或者密码错误",
        "code": 401,
        "detail": serializer.errors
    }
    return {'data': results}

class UserSerializer(serializers.ModelSerializer):

    def to_representation(self, instance):
        ROLE_CHOICES = {0: ["admin"], 1: ["dataManager"], 2: ["user"]}
        user_dict = super().to_representation(instance)
        user_dict["roles"] = ROLE_CHOICES[user_dict["roles"]]
        return user_dict

    class Meta:
        model = models.UserProfile
        fields = ["username","password","introduction","avatar","name","roles"]
    def create(self, validated_data):
        user= models.UserProfile.objects.create_user(**validated_data) # 这里新增玩家必须用create_user,否则密码不是秘文
        return user

from rest_framework.viewsets import GenericViewSet


class createUser(mixins.CreateModelMixin,GenericViewSet):
    queryset = models.UserProfile.objects.all()
    serializer_class = UserSerializer


    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        res = {}
        res['code'] = 2000
        return Response(res,status=status.HTTP_201_CREATED, headers=headers)

class UserDetailSerializer(serializers.ModelSerializer):

    def to_representation(self, instance):
        ROLE_CHOICES = {0: ["admin"], 1: ["dataManager"], 2: ["user"]}
        user_dict = super().to_representation(instance)
        new_dict = {}

        new_dict['introductoin'] = user_dict['introduction']
        new_dict['avatar'] = 'http://121.36.13.179' + user_dict['avatar'][33:]
        new_dict['name'] = user_dict['username']
        new_dict['roles'] = ROLE_CHOICES[user_dict["roles"]]

        del user_dict
        return new_dict

    class Meta:
        model = models.UserProfile
        fields = ["username","introduction","avatar","name","roles"]

class UserViewset(mixins.CreateModelMixin, mixins.UpdateModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    serializer_class = UserDetailSerializer
    queryset = UserProfile.objects.all()
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (JSONWebTokenAuthentication, )

   
    def get_object(self):
        return self.request.user

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        res = {}
        res['code'] = 2000
        res['data'] = serializer.data
        return JsonResponse(res)


class logoutView(APIView):
    def post(self, request, *args, **kwargs):
        logout(request)
        res = {}
        res['code'] = 2000
        res['message'] = 'success'

        return JsonResponse(res)

