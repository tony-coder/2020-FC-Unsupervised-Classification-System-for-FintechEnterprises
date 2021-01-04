import os
import shutil
import time
import zipfile
from pathlib import Path

import pandas as pd
import numpy as np
import json
import pymysql

class MyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        else:
            return super(MyEncoder, self).default(obj)

class Evaluate:
    def __init__(self):
        self.attr_list = "risk_module_type,investment_module_type," \
                "creativity_module_type,brand_module_type," \
                "recruit_module_type,credit_module_type," \
                "company_baseinfo_module_type,ent_type," \
                "ent_inner_type".split(',')
        self.cluster_num = 15 # 簇个数
        self.attr_num = 8 # 属性个数
        self.level_num = 11 # 等级个数
        self.evaluate_matrix = np.zeros(shape=(self.cluster_num,self.attr_num,self.level_num),dtype=np.int) # 15*8*10的矩阵，对应15个簇，8个模块，10个等级
        # self.evaluate_matrix = [[[0]*self.level_num]*self.attr_num]
        self.ent_num_array = np.zeros(self.cluster_num,dtype=np.int) # 每个簇的企业数
        self.ent_level_array = np.zeros(self.level_num,dtype=np.int) # 每个等级的企业数
        self.evaluate_dict = {} # 最终数据统计的dict

    def get_each_cluster_module_value(self,df_tmp):
        df = df_tmp[self.attr_list]
        df_values = df.values
        for k in range(self.level_num):
            self.ent_level_array[k] += len(np.where(df_values[:, -2] == k)[0])

        for i in range(self.cluster_num):
            self.ent_num_array[i] += len(np.where(df_values[:,-1] == i)[0]) # 每个簇企业的个数
            for j in range(self.attr_num):
                for k in range(self.level_num):
                    self.evaluate_matrix[i][j][k] += len(np.where((df_values[:, -1] == i) & (df_values[:, j] == k))[0])


    def pd_iterator(self,df):
        for df_iterator in df:
            self.get_each_cluster_module_value(df_iterator)

    def get_evaluate_dict(self):
        attr_dict = dict(zip(
            list(range(self.attr_num)),self.attr_list[:-1]
        ))
        for i in range(self.cluster_num):
            cluster_i_dict = {str(i):{}}
            for j in range(self.attr_num):
                cluster_i_dict[str(i)]['ent_num'] = self.ent_num_array[i]
                cluster_i_dict[str(i)].update({attr_dict[j]:dict(zip(map(str,list(range(self.level_num))),list(self.evaluate_matrix[i,j,:])))})
            self.evaluate_dict.update(cluster_i_dict)

    def run(self,df):
        # self.__init__()
        self.pd_iterator(df)
        self.get_evaluate_dict()
        # print(self.evaluate_matrix)
        return self.evaluate_dict


def un_zip(file_name):
    with zipfile.ZipFile(file_name, 'r') as zf:
        os.chdir("../data/train")
        print(zf.namelist())

        for fn in zf.namelist():
            if fn.endswith('/'):
                right_fn = fn.encode('cp437').decode('gbk')
                os.mkdir((right_fn))
                continue
            right_fn = fn.encode('cp437').decode('gbk')
            with open(right_fn, 'wb') as output_file:
                with zf.open(fn, 'r') as origin_file:
                    shutil.copyfileobj(origin_file, output_file)
