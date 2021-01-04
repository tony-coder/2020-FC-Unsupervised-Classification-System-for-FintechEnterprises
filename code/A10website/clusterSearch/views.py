from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
from rest_framework import mixins, viewsets
from rest_framework.utils import json

from clusterSearch.serializers import clusterSearchSerializer
from ent_manage.models import CompanyBaseinfoSummary


class clusterSearchView(mixins.ListModelMixin, viewsets.GenericViewSet):

    serializer_class = clusterSearchSerializer

    def list(self, request, *args, **kwargs):
        req = json.loads(request.body.decode())

        if "riskRank" in req:
            riskRank = req["riskRank"]
            riskRank_g = int(riskRank[0])
            riskRank_l = int(riskRank[1])
        
        if "investmentRank" in req:
            investmentRank = req["investmentRank"]
            investmentRank_g = int(investmentRank[0])
            investmentRank_l = int(investmentRank[1])

        if "creatityRank" in req:
            creatityRank = req["creatityRank"]
            creatityRank_g = int(creatityRank[0])
            creatityRank_l = int(creatityRank[1])

        if "brandRank" in req:
            brandRank = req["brandRank"]            
            brandRank_g = int(brandRank[0])
            brandRank_l = int(brandRank[1])

        if "recruitRank" in req:
            recruitRank = req["recruitRank"]
            recruitRank_g = int(recruitRank[0])
            recruitRank_l = int(recruitRank[1])


        if "creditRank" in req:
            creditRank = req["creditRank"]
            creditRank_g = int(creditRank[0])
            creditRank_l = int(creditRank[1])
        
        page = int(req["page"])
        rows = int(req["rows"])
        
        keyword = ""
        if "keyword" in req.keys():
            keyword = req["keyword"]
        if keyword:
            Q_all = Q(entname__contains=keyword)
        else:
            multiEntList = json.loads(req['multiEntList'])
            Q_all = Q(entname__in=multiEntList)
        
        print(keyword)
        print(riskRank)


        # Q_all = Q(entname__contains=keyword)  


        if riskRank_g or riskRank_l:
            Q_risk_g = Q(entmodule__risk_module_type__gte=riskRank_g)
            Q_risk_l = Q(entmodule__risk_module_type__lte=riskRank_l)
            Q_all = Q_all & Q_risk_g & Q_risk_l

        if investmentRank_g or investmentRank_l:
            Q_investment_g = Q(entmodule__investment_module_type__gte=investmentRank_g)
            Q_investment_l = Q(entmodule__investment_module_type__lte=investmentRank_l)
            Q_all = Q_all & Q_investment_g & Q_investment_l

        if creatityRank_g or creatityRank_l:
            Q_creativity_g = Q(entmodule__creativity_module_type__gte=creatityRank_g)
            Q_creativity_l = Q(entmodule__creativity_module_type__lte=creatityRank_l)
            Q_all = Q_all & Q_creativity_g & Q_creativity_l

        if brandRank_g or brandRank_l:
            Q_brand_g = Q(entmodule__brand_module_type__gte=brandRank_g)
            Q_brand_l = Q(entmodule__brand_module_type__lte=brandRank_l)
            Q_all = Q_all & Q_brand_g & Q_brand_l

        if recruitRank_g or recruitRank_l:
            Q_recruit_g = Q(entmodule__recruit_module_type__gte=recruitRank_g)
            Q_recruit_l = Q(entmodule__recruit_module_type__lte=recruitRank_l)
            Q_all = Q_all & Q_recruit_g & Q_recruit_l

        if creditRank_g or creditRank_l:
            Q_credit_g = Q(entmodule__credit_module_type__gte=creditRank_g)
            Q_credit_l = Q(entmodule__credit_module_type__lte=creditRank_l)
            Q_all = Q_all & Q_credit_g & Q_credit_l


        queryset = CompanyBaseinfoSummary.objects.filter(Q_all)
        print(Q_all)

        if page and rows:
            pre_index = (page-1) * rows
            lat_index = page * rows

            if lat_index > len(queryset):
                lat_index = len(queryset)

        return_queryset = queryset[pre_index:lat_index]
        # print(queryset)

        res = {}
        res['code'] = 2000
        res['clusterTotal'] = len(queryset)
        serializer = self.get_serializer(return_queryset, many=True)
        res['data'] = serializer.data

        return JsonResponse(res)