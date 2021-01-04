import os
import sys
import shutil
import zipfile
from pathlib import Path

from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
from django import forms


def get_project_path():
    project_path = os.path.split(os.path.abspath(os.path.realpath(__file__)))[0] + "/../"    
    return os.path.abspath(project_path)

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

def un_zip(file_name,dest_dir):

    pre_dir = os.getcwd()
    with zipfile.ZipFile(file_name, 'r') as zf:
        os.chdir(dest_dir)
        for fn in zf.namelist():
            if fn.endswith('/'):
                continue
            right_fn = fn.encode('cp437').decode('gbk').split('/')[1]
            with open(right_fn, 'wb') as output_file:
                with zf.open(fn, 'r') as origin_file:
                    shutil.copyfileobj(origin_file, output_file)
        os.chdir(pre_dir)

def upload_file_train(request):
    if request.method == 'POST':

        del_file('data/tmp')
        del_file('data/train')
        print(request)

       
        files = request.FILES.get("file")
        print(files)
        name = files.name
        if name.find('"') != -1:
            name = name[:-1]
        dest = open('data/tmp/' + name, 'wb+')
        for chunk in files.chunks():
            dest.write(chunk)
        dest.close()

        file_name = 'data/tmp/'+ name
        dest_dir = 'data/train'


        un_zip(file_name,dest_dir)

        res = {}
        res['code'] = 2000
        data = {}
        data['message'] = '上传成功'
        res['data'] = data
        return JsonResponse(res)

def upload_file_predict(request):
    if request.method == 'POST':

        del_file('data/tmp')
        del_file('data/predict')

        print(request)
        files = request.FILES.get("file")
        print(files)
        name = files.name
        if name.find('"') != -1:
            name = name[:-1]
        dest = open('data/tmp/' + name, 'wb+')
        for chunk in files.chunks():
            dest.write(chunk)
        dest.close()

        file_name = 'data/tmp/' + name
        dest_dir = 'data/predict'

        un_zip(file_name, dest_dir)

        res = {}
        res['code'] = 2000
        data = {}
        data['message'] = '上传成功'
        res['data'] = data
        return JsonResponse(res)
