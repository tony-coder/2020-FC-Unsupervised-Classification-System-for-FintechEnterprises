# -*- coding: utf-8 -*-
# @Time    : 2020/1/29 17:48
# @Author  : Roman
# @FileName: MachineLearning.py
# @Software: PyCharm
# @Email   : 693497091@qq.com
# @Github  : czq693497091

'''
    import ML_core as MLC
    Pack the sklearn to easily split,train_utils,predit and old_evaluate the data.
'''

from collections import Iterable
from sklearn.model_selection import train_test_split
from sklearn.cluster import KMeans, DBSCAN, Birch
from sklearn.externals import joblib
from sklearn.decomposition import PCA
import sklearn.metrics as sm
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from sklearn.mixture import GaussianMixture as GMM
import os


def get_train_test_matrix(data_matrix, test_size=0.3):
    '''
    Split the origin data into trainning training data and test data.

    :param data_matrix: np_array    Origin matrix of data.
    :param test_size: float         Percent of test data.
    :return: (np_array,np_array)    Training data and test data.
    '''

    data_train, data_test = train_test_split(data_matrix, test_size=test_size)
    return data_train, data_test


def KMeans_train_predict(data_matrix, n_cluster=5, ascending_order=True, make_model=False, model_path=None,
                         default_value=0):
    '''
    Use KMeans to train_utils and predict the data.
    Attention: The dimension of data_matrix shuold be one.

    :param data_matrix: np_array    训练数据. 
    :param n_cluster: int           簇的个数，普通属性都是n_cluster=5，对于模块总分和企业总分，要10个等级.
    :param ascending_order:boolean  是否标签大小根据分值大小排序，默认选是.
    :param make_model:boolean       是否生成模型
    :param model_path:str           如果生成模型，给出模型保存路径
    :param default_value:float      缺省值的填充
    :return: labels,np_array        标签的np.array()

    '''
    origin_cluster = n_cluster
    temp_cluster_num = len(set(data_matrix))
    n_cluster = min(temp_cluster_num, n_cluster)

    km = KMeans(n_clusters=n_cluster)

    labels = km.fit_predict(data_matrix.reshape(-1, 1))

    if ascending_order == True:
        labels = get_trans_label(model=km, labels=labels)

    labels[data_matrix == default_value] = 0

    if make_model == True and model_path is not None:
        # 利用python中的sklearn.externals 模块将模型保存到本地
        joblib.dump(value=km, filename=model_path)

    labels = np.ceil(labels / np.max(labels) * origin_cluster)

    return labels


def predict(data_matrix, model, ascending_order=True, default_value=0):  # 只能用于预测打分
    '''
    输入的矩阵，可以是[1,8,9,10,...]一串数字，这样可以得到一串预测结果
    也可以是一个数字，得到一个预测结果
    :param data_matrix: np_array    Data needed to predict or just a single number.
    :param model: 
    :return: Labels of data matrix.
    '''

    data_matrix = np.array(data_matrix)
    labels = model.predict(X=data_matrix.reshape(-1, 1))
    if ascending_order == True:
        labels = get_trans_label(model=model, labels=labels)

    labels[data_matrix == default_value] = 0
    # print(model)
    max_level = 5
    if model.n_clusters > 5:
        max_level = 10

    # scatter the value between 1-max_level
    labels = np.ceil(labels / model.n_clusters * max_level)
    return np.array(labels, dtype=int)


def load_model(model_path):
    '''

    :param model_path: Path of model 
    :return: model
    '''

    return joblib.load(model_path)


def get_trans_label(model, labels, default_value=0):
    '''
    Make sure that the label is ascending with its center value.
    example:
        km.centers = [2.8 1.2 1.5]      labels = [1 2 3]

        And we can transfer it into {1.2:1,1.5:2,2.8:3}
        It means that the smaller center value with the smaller label value.
        Finally [1,2,3] => [3,1,2]


    :param model: trainning model 
    :return: transfer_label
    '''

    centers = model.cluster_centers_[:, 0]

    # number the center of model
    d = dict(zip(centers, list(range(len(centers)))))
    # sort the dictionary as the ascending order of its values
    d = dict(sorted(d.items(), key=lambda x: x[0]))
    trans_dict = dict(zip(list(d.values()), list(range(1, len(centers) + 1))))
    v_transfer = np.vectorize(dict_transfer)
    labels = v_transfer(labels, trans_dict)

    return labels


def inner_predict(data_matrix, model):
    # model = load_model(model_path=module_path)
    data_matrix = np.array(data_matrix)
    labels = model.predict(data_matrix)
    return labels


def dict_transfer(x, d):
    return d[x]


def KM(data_matrix, C, model_path=None, is_ascend=True):
    '''
    KMeans聚类
    :param data_matrix: 输入矩阵 
    :param C: 簇的个数
    :param model_path:模型存储路径
    :return: 
    '''
    km_model = KMeans(n_clusters=C)
    labels = km_model.fit_predict(data_matrix)

    if model_path is not None:
        joblib.dump(value=km_model, filename=model_path)
    if is_ascend == True:
        labels = get_trans_label(model=km_model, labels=labels)
    return labels


def DBSC(data_matrix, EPS, MS=5):
    '''
    密度聚类
    :param data_matrix: 输入矩阵 
    :param EPS: ϵϵ-邻域距离，过大簇数减少，过小簇数增多
    :param MS: 成为核心对象所需要的ϵϵ-邻域的样本数阈值,默认为5
    :return: 
    '''

    DBSCdata = DBSCAN(eps=EPS, min_samples=MS).fit_predict(data_matrix)


def BIR(data_matrix, C=None, model_path=None):
    '''
    层次聚类
    :param data_matrix: 输入矩阵 
    :param C: 簇的个数
    :return: 
    '''
    BIR_model = Birch(n_clusters=C)
    labels = BIR_model.fit_predict(data_matrix)
    if model_path is not None:
        joblib.dump(value=BIR_model, filename=model_path)
    # print(BIR_model)
    # labels = get_trans_label(model=BIR_model,labels=labels)
    return labels


def GM(data_matrix, C, model_path=None):
    '''

    :param data_matrix: 输入矩阵 
    :param C: 簇的个数
    :return: 
    '''
    GM_model = GMM(n_components=C)

    labels = GM_model.fit_predict(data_matrix)
    if model_path is not None:
        joblib.dump(value=GM_model, filename=model_path)
    return labels
