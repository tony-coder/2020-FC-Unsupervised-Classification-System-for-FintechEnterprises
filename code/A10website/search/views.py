from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
from django.views import View
from rest_framework import mixins, viewsets
from rest_framework.response import Response
from rest_framework.utils import json

from dataTojson.models import CompanyBaseinfoSummary
from search.models import EntModule
from search.serializers import SearchSerializer, HotEntSerializer,EntSearchSerializer


class SearchView(mixins.ListModelMixin, viewsets.GenericViewSet):

    serializer_class = EntSearchSerializer

    def list(self, request, *args, **kwargs):

        req = json.loads(request.body.decode())
        print(req)

        searchType = req["searchType"]
        print(searchType)
        if len(searchType) == 0:
            searchType = ["1"]
        if "1" in searchType:
            keyword = ""
            if "keyword" in req.keys():
                keyword = req["keyword"]
            if keyword:
                Q_entname = Q(entname__contains=keyword)
            else:
                multiEntList = json.loads(req['multiEntList'])
                print(multiEntList)
                Q_entname = Q(entname__in=multiEntList)
            
            queryset = CompanyBaseinfoSummary.objects.filter(Q_entname)

            # print(queryset)
            if "type" in req.keys():
                type = req["type"]
                if type != "":
                    if type == "其他类型":
                        print(type)
                        Q_enttype = ~(Q(enttype__contains="有限责任公司") | Q(enttype__contains="股份有限公司") | Q(
                            enttype__contains="独资企业") | Q(enttype__contains="合伙制企业"))
                        # queryset = queryset.exclude(Q(enttype__contains="有限责任公司")).exclude( Q(enttype__contains="股份有限公司")).exclude(Q(
                        #     enttype__contains="独资企业")).exclude(Q(enttype__contains="合伙制企业"))
                    else:
                        Q_enttype = Q(enttype__contains=type)
                    queryset = queryset.filter(Q_enttype)
                    # print(queryset)
            if "enterpriseStatus" in req.keys():
                OPEN = "在营（开业）企业"
                OPENlist = ["在业","营业","开业"]
                enterpriseStatus = req["enterpriseStatus"]
                if enterpriseStatus != "":
                    if enterpriseStatus in OPENlist:
                        Q_entstatus = Q(entstatus__contains=OPEN)
                    else:
                        Q_entstatus = Q(entstatus__contains=enterpriseStatus)                
                    queryset = queryset.filter(Q_entstatus)
            if "registeredCapitalNum" in req.keys():
                registeredCapitalNum = req["registeredCapitalNum"]
                print(registeredCapitalNum)
                if registeredCapitalNum != "":
                    regcapLowerLimit = int(registeredCapitalNum.split("-")[0])
                    regcapUpperLimit = int(registeredCapitalNum.split("-")[1])
                    print(regcapLowerLimit)
                    if regcapUpperLimit==0:
                        Q_regcap = Q(regcap__gte=regcapLowerLimit)
                    else:


                        Q_regcap = Q(regcap__gte=regcapLowerLimit) & Q(regcap__lte=regcapUpperLimit)
                    queryset = queryset.filter(Q_regcap)


            if "dateOfEstablishment" in req.keys():

                dateOfEstablishment = req["dateOfEstablishment"]
                print(dateOfEstablishment)
                if dateOfEstablishment != "":
                    if len(dateOfEstablishment) <= 4:
                        yearOfEstablishment = dateOfEstablishment
                        Q_date = Q(estdate__startswith=yearOfEstablishment)
                    else:
                        yearOfEstablishmentLowerLimit = dateOfEstablishment.split("-")[0]
                        yearOfEstablishmentUpperLimit = dateOfEstablishment.split("-")[1]
                        print(yearOfEstablishmentLowerLimit,yearOfEstablishmentUpperLimit)
                        if yearOfEstablishmentLowerLimit == "0":
                            yearOfEstablishmentUpperLimit = yearOfEstablishmentUpperLimit + "/12/31"
                            Q_date = Q(estdate__lte=yearOfEstablishmentUpperLimit)
                        elif yearOfEstablishmentUpperLimit == "0":
                            yearOfEstablishmentLowerLimit = yearOfEstablishmentLowerLimit + "/1/1"
                            Q_date = Q(estdate__gte=yearOfEstablishmentLowerLimit)
                        else:
                            yearOfEstablishmentLowerLimit = yearOfEstablishmentLowerLimit + "/1/1"
                            yearOfEstablishmentUpperLimit = yearOfEstablishmentUpperLimit + "/12/31"
                        
                            Q_date = Q(estdate__gte=yearOfEstablishmentLowerLimit) & Q(estdate__lte=yearOfEstablishmentUpperLimit)
                        print(yearOfEstablishmentLowerLimit,yearOfEstablishmentUpperLimit)
                    queryset = queryset.filter(Q_date)


            page = req["page"]
            rows = req["rows"]       

            companyTotal = len(queryset)

            if page != 0 and rows != 0:
                pre_index = (page - 1) * rows
                lat_index = page * rows

                if lat_index > len(queryset):
                    lat_index = len(queryset)

                return_queryset = queryset[pre_index:lat_index]

            res = {}
            res['code'] = 2000
            res['companyTotal'] = companyTotal
            serializer = self.get_serializer(return_queryset, many=True)
            res['data'] = serializer.data

            return JsonResponse(res)


        else:
            res ={}
            res['code'] = 2000
            res['companyTotal'] = 0
            res['data'] = []

            return JsonResponse(res)



       

class HotEntView(mixins.ListModelMixin, viewsets.GenericViewSet):
    serializer_class = HotEntSerializer

    def list(self, request, *args, **kwargs):
        hotEnt = CompanyBaseinfoSummary.objects.filter(searchnum__gt=0).order_by('-searchnum')
        print(hotEnt)
        hotEntNum = len(hotEnt)
        if hotEntNum>8:
            hotEnt = hotEnt[0:8]
            hotEntNum = 8

        res = {}
        res['code'] = 2000
        serializer = self.get_serializer(hotEnt, many=True)
        data = {}
        data['total'] = hotEntNum
        data['items'] = serializer.data
        res['data'] = data

        return JsonResponse(res)
