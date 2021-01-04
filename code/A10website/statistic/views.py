from django.shortcuts import render

# Create your views here.
import json
import time
from dataTojson.models import UserUserprofile, EntModule
import numpy as np
import pymysql
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from statistic.models import EntModuleWeight

# Create your views here.
from rest_framework.views import APIView
import pandas as pd

from utils.pic_evaluate import Evaluate, MyEncoder

class chartView(APIView):

    def post(self, request, *args, **kwargs):

        start = time.time()
        conn = pymysql.connect(host='localhost', port=3306, user='root', password='Zjut123456!', db='entdb',
                               charset='utf8')
        sql = 'select * from ent_module'

        df = pd.read_sql(sql, conn, chunksize=2000)

        evaluate = Evaluate()
        ans_dict = evaluate.run(df)

        end = time.time()

        print(end-start)


        res = {}
        res['code'] = 2000
        res['data'] = ans_dict
        return JsonResponse(res,encoder=MyEncoder)


class cluster2DView(APIView):
    def post(self, request, *args, **kwargs):

        df = pd.read_csv("data/pos_and_labels_test1.csv")
        data  = {}
        data['code'] = 2000
        res = {}

        for i in range(15):
            tempdf = df[df['labels'] == i]
            templist = []
            for index, row in tempdf.iterrows():
                temp = []
                temp.append(row['x'])
                temp.append(row['y'])
                templist.append(temp)
            label = 'label' + str(i)
            res[label] = templist

        # print(res)
        data['data'] = res

        return JsonResponse(data)

class cluster3DView(APIView):
    def post(self, request, *args, **kwargs):

        df = pd.read_csv("data/3D_pos.csv")
        data  = {}
        data['code'] = 2000
        res = {}

        for i in range(15):
            tempdf = df[df['labels'] == i]
            templist = []
            for index, row in tempdf.iterrows():
                temp = []
                temp.append(row['x'])
                temp.append(row['y'])
                temp.append(row['z'])
                templist.append(temp)
            label = 'label' + str(i)
            res[label] = templist

        # print(res)
        data['data'] = res

        return JsonResponse(data)

class barView(APIView):
    def get(self, request, *args, **kwargs):
        start = time.time()
        conn = pymysql.connect(host='localhost', port=3306, user='root', password='Zjut123456!', db='entdb',
                               charset='utf8')
        sql = 'select * from ent_module'

        df = pd.read_sql(sql, conn, chunksize=2000)

        evaluate = Evaluate()
        ans_dict = evaluate.run(df)

        end = time.time()

        print(end-start)

        ent_level_array = np.round(evaluate.ent_level_array/np.sum(evaluate.ent_level_array) * 100,2)
        ent_num_array = np.round(evaluate.ent_num_array/np.sum(evaluate.ent_num_array) * 100,2)

        res = {}
        res['code'] = 2000
        res['leftbar'] = ent_level_array
        res['rightbar'] = ent_num_array
        return JsonResponse(res, encoder=MyEncoder)



class quantityView(APIView):
    def get(self, request, *args, **kwargs):
        user_queryset = UserUserprofile.objects.all()
        ent_queryset = EntModule.objects.all()

        res = {}

        res['code'] = 2000
        data = {}

        data['userNum'] = len(user_queryset)
        data['entNum'] = len(ent_queryset)

        res['data'] = data

        return JsonResponse(res)





class weightView(APIView):
    def get(self, request, *args, **kwargs):
        queryset = EntModuleWeight.objects.all()

        result = queryset[0]

        res = {}

        res['code'] = 2000
        data = {}
        data['risk_module_type'] = result.risk_module_type
        data['investment_module_type'] = result.investment_module_type
        data['creativity_module_type'] = result.creativity_module_type
        data['brand_module_type'] = result.brand_module_type
        data['recruit_module_type'] = result.recruit_module_type
        data['credit_module_type'] = result.credit_module_type
        data['base_module_type'] = result.base_module_type

        res['data'] = data

        return JsonResponse(res)

    def post(self, request, *args, **kwargs):

        req = json.loads(request.body.decode())

        risk_module_type = float(req['risk_module_type'])
        investment_module_type = float(req['investment_module_type'])
        creativity_module_type = float(req['creativity_module_type'])
        brand_module_type = float(req['brand_module_type'])
        recruit_module_type = float(req['recruit_module_type'])
        credit_module_type = float(req['credit_module_type'])
        base_module_type = float(req['base_module_type'])


        weight = EntModuleWeight.objects.get(id=1)
        weight.base_module_type = base_module_type
        weight.risk_module_type = risk_module_type
        weight.investment_module_type = investment_module_type
        weight.creativity_module_type = creativity_module_type
        weight.brand_module_type = brand_module_type
        weight.recruit_module_type = recruit_module_type
        weight.credit_module_type = credit_module_type

        weight.save()

        res = {}

        res['code'] = 2000
        res['message'] = '参数修改成功！将于下次训练模型时生效'

        return JsonResponse(res)



