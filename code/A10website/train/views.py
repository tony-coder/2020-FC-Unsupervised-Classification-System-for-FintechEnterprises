import os
import shutil
import sys
import json
from django.http import JsonResponse
import zipfile

# Create your views here.
from rest_framework.views import APIView

from train.epoch import Epoch


def zip_file(src_dir,des_dir):
    print(sys.path)
    print(os.getcwd())
    zip_name = des_dir +'/result.zip'
    z = zipfile.ZipFile(zip_name,'w',zipfile.ZIP_DEFLATED)
    for dirpath, dirnames, filenames in os.walk(src_dir):
        fpath = dirpath.replace(src_dir,'')
        fpath = fpath and fpath + os.sep or ''
        for filename in filenames:
            z.write(os.path.join(dirpath, filename),fpath+filename)
            print ('==压缩成功==')
    z.close()

def del_file(filepath):
    """
    删除某一目录下的所有文件或文件夹
    :param filepath: 路径
    :return:
    """
    del_list = os.listdir(filepath)
    for f in del_list:
        file_path = os.path.join(filepath, f)
        if os.path.isfile(file_path):
            os.remove(file_path)
        elif os.path.isdir(file_path):
            shutil.rmtree(file_path)


class trainView(APIView):
    def get(self, request, *args, **kwargs):

        print(sys.path)
        print(request)

        pre_path = os.getcwd()

        print(os.getcwd())
        os.chdir('train')

        epoch = Epoch()
        train_path = "../data/train"

        epoch.train_all(csv_doc=train_path)

        del_file("../static/train")

        zip_file("out", "../static/train")

        start = epoch.start_time
        end = epoch.end_time

        time = round(end - start,2)
        trainTime = round(epoch.train_total_time,2)

        os.chdir(pre_path)

        res = {}
        res['code'] = 2000
        data = {}
        res['messgae'] = '模型训练成功'
        res['totlTime'] = time
        res['trainTime'] = trainTime
        res['url'] = '/static/train/result.zip'
        return JsonResponse(res)


class predictView(APIView):
    def post(self, request, *args, **kwargs):

        req = json.loads(request.body.decode())
        model = int(req['model'])
        print(sys.path)
        print(request)

        pre_path = os.getcwd()

        print(os.getcwd())
        os.chdir('train')

        epoch = Epoch()

        train_path = "../data/predict"
        if model == 1:
            epoch.predict_use_default_model(csv_doc=train_path)
        elif model == 2:
            epoch.predict_use_new_model(csv_doc=train_path)

        del_file("../static/predict")
        zip_file("out", "../static/predict")
        
        start = epoch.start_time
        end = epoch.end_time

        time = round(end - start,2)
        trainTime = round(epoch.train_total_time,2)

        os.chdir(pre_path)        

        print(os.getcwd())

        res = {}
        res['code'] = 2000
        data = {}
        res['totlTime'] = time
        res['predictTime'] = trainTime
        res['url'] = '/static/predict/result.zip'
        return JsonResponse(res)


