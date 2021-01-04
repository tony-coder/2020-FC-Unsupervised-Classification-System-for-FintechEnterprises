# -*- coding: utf-8 -*-
# @Time    : 2020/1/29 12:48
# @Author  : Roman
# @FileName: Evaluate.py
# @Software: PyCharm
# @Email   : 693497091@qq.com
# @Github  : czq693497091

import os
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import MinMaxScaler
from sklearn.preprocessing import LabelBinarizer
from sklearn.preprocessing import LabelEncoder

from utils import MachineLearning as ML

import pandas as pd
import numpy as np
from collections import Iterable

'''
    x = np.array([[1., -1., 2.],
                  [2., 0., 0.],
                  [0., 1., -1.]])
'''


def data_std_scale(data_matrix):
    '''
    将数据进行标准化处理
    :param data_matrix: 输入的原始数据 
    :return: 标准化处理的数据
    '''
    scale_data = StandardScaler().fit_transform(data_matrix)
    return scale_data


def data_min_max_scale(data_matrix):
    '''
    最值缩放处理,即归一化
    
    
    在MinMaxScaler中是给定了一个明确的最大值与最小值。它的计算公式如下：
    X_std = (X - X.min(axis=0)) / (X.max(axis=0) - X.min(axis=0))
    X_scaled = X_std / (max - min) + min
    
    所以x在该方法下处理得到的结果为:
    array(
        [0.5    0       1.]
        [1      0.5     0.3333]
        [0      1       0]
    )

    :param data_matrix: 输入的原始数据
    :return: 
    '''
    scale_data = MinMaxScaler().fit_transform(data_matrix)
    return scale_data


def one_hot(data_frame, col_name):
    '''
    独热编码，一般与PCA结合使用
    
    :param data_frame: pd.DataFrame()格式的数据，要处理的数据矩阵 
    :param col_name:需要one hot编码的列 
    :return: 
    '''
    one_hot_list = LabelBinarizer().fit_transform(data_frame[col_name])
    return one_hot_list


def labencData(dataMat, colName):
    """
    将定性数据哑编码

    Args:
        dataMat: 文本数据矩阵
        colName: 需要转换的字段列名
    Returns:a
        labencDatalist: 哑编码后的数据矩阵
    """
    labencDatalist = LabelEncoder().fit_transform(dataMat[colName])
    return labencDatalist


def KM_epoch(infile, out_doc, model_doc, columns):
    '''
    KMeans的批量处理
    :param infile: 输入文件
    :param out_doc: 输出文件目录
    :param model_doc: 输出模型目录
    :param column: 要处理的列，如果就一个属性要训练，例如"is_punish"，如果有多个属性的，例如["appellant_amount","defedant_amount","declaredate"]
    :return: 
    '''
    # 读入
    data = pd.read_csv(infile).fillna(0)
    # 文件名
    file_postfix = infile.split('\\')[-1].split('.')[0]
    if model_doc.endswith('\\') == False:
        model_doc += "\\"

    if isinstance(columns, list) == False:
        columns = [columns]

    for column in columns:
        labels = ML.KMeans_train_predict(
            data_matrix=data[column].values,
            make_model=True,
            model_path=model_doc + "\\" + file_postfix + "-" + column + ".m",# 模型名称就是表名-属性名.m
        )
        data[column + "_type"] = labels

    if out_doc.endswith('\\') == False:
        out_doc += "\\"
    data.to_csv(out_doc + "dealed_" + file_postfix + ".csv", index=False) # 统一的输出新表的名称为dealed_原始表名.csv


def merge_mark(base_doc, out_file, key='entname', postfix='_type', default_value=0, is_fillna=False):
    '''
    将所有评分的文件中的评分项，以外连接的方式合并，key是entname
    :param infile_list: 输入文件所在目录 
    :param out_file: 输出文件的名称
    :return: 
    '''
    if base_doc.endswith('\\') == False:
        base_doc += "\\"
    infile_list = os.listdir(base_doc)
    for i in range(len(infile_list)):
        infile_list[i] = base_doc + infile_list[i]

    out_data_frame = pd.DataFrame()

    for i in range(len(infile_list)):
        file = infile_list[i]
        target_col_list = ['entname']
        data = pd.read_csv(file, encoding='gbk')
        for col in data.columns:
            if col.endswith(postfix):
                target_col_list.append(col)

        data = data[target_col_list]

        if i == 0:
            out_data_frame = data
        else:
            out_data_frame = pd.merge(out_data_frame, data, how='outer', left_on=key, right_on=key)

    if is_fillna == True:
        out_data_frame = out_data_frame.fillna(default_value)
    # print(out_data_frame)
    out_data_frame.to_csv(out_file, index=False)


def get_module_mark(infile, outfile, module_name='mark', weight_dict=None, is_mark=False, model_path=None, n_cluster=10):
    '''
    获取每个模块的总分,可以决定是否对总分进行再次打标分类
    
    :param infile: 输入文件
    :param outfile: 输出文件
    :param module_name: 模块名
    :param weight_dict: 权重字典 
    :param is_mark: 是否生成模型，默认不生成，如果要生成，则True
    :param model_path: 如果生成模型，给出模型生成的路径
    :param n_cluster: 簇的个数，一般属性为5，但是7个模块的总分，和最后企业的总分，都是10
    :return: 
    '''
    data_frame = pd.read_csv(infile, encoding='gbk')
    columns = list(data_frame.columns[1:]) # 获取属性列表，不包括第一个因为第一个是entanme
    if weight_dict == None: # 如果权重字典为空，就默认大家权重都是1
        weight_dict = dict(zip(columns, np.ones(len(columns), dtype=int)))

    sum_module = np.zeros(len(data_frame['entname']), dtype=float) # 声明一个总分数组
    for column in weight_dict: # 加权求和
        sum_module += weight_dict[column] * data_frame[column].values
    data_frame[module_name] = sum_module

    # 还需要用KMeans对总分进行评级打分
    if is_mark == True:
        labels = ML.KMeans_train_predict(
            data_matrix=sum_module,
            make_model=True,
            model_path=model_path,
            n_cluster=n_cluster
        )
        data_frame[module_name + "_type"] = labels
    data_frame.to_csv(outfile, index=False)
