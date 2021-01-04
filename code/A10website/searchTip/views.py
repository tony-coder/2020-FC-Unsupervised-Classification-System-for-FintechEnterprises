from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
from rest_framework import mixins, viewsets
from rest_framework.pagination import PageNumberPagination
from rest_framework.utils import json

from ent_manage.models import CompanyBaseinfoSummary
from searchTip.serializers import TipSerializer


class searchTipView(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = CompanyBaseinfoSummary.objects.all()

    serializer_class = TipSerializer

    def list(self, request, *args, **kwargs):

        req = json.loads(request.body.decode())

        print(req)
        
        keyword = req['keyword']
        searchType = int(req['searchType'][0])
        page = int(req['page'])
        rows = int(req['rows'])

        if keyword :
            # 全部
            if searchType==0:
                print(keyword)
                condition_entname = Q(entname__startswith=keyword)
                queryset = CompanyBaseinfoSummary.objects.filter(condition_entname)
                # if len(TipList) > 10:
                #     TipList = TipList[0:10]

                if page and rows:
                    pre_index = (page - 1) * rows
                    lat_index = page * rows

                    if lat_index > len(queryset):
                        lat_index = len(queryset)

                    queryset = queryset[pre_index:lat_index]
                else:
                    if len(queryset) > 8:
                        queryset = queryset[0:8]

                res = {}

                serializer = self.get_serializer(queryset, many=True, context={"id": searchType})

                res['code'] = 2000
                res['data'] = serializer.data

                print(res)

                return JsonResponse(res)

            # 企业名
            elif searchType==1:
                print(keyword)
                condition_entname = Q(entname__startswith=keyword)
                queryset = CompanyBaseinfoSummary.objects.filter(condition_entname)
                if page and rows:
                    pre_index = (page-1)*rows
                    lat_index = page*rows

                    if lat_index > len(queryset):
                        lat_index = len(queryset)

                    queryset = queryset[pre_index:lat_index]
                else:
                    if len(queryset) > 8:
                        queryset = queryset[0:8]



                res = {}

                serializer = self.get_serializer(queryset,many=True,context={"id":searchType})


                res['code'] = 2000
                res['data'] = serializer.data

                print(res)

                return JsonResponse(res)
            else:
                res = {}
                res['code'] = 404
                return JsonResponse(res)

        else:
            res={}
            res['code'] = 404
            return JsonResponse(res)



