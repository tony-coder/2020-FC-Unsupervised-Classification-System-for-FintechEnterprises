# -*- coding: utf-8 -*-


from train_utils.epoch import Epoch

epoch = Epoch()
epoch.init_train_enviroment() # 初始化训练、预测环境
# #
# train_data_doc = r"F:\2019计算机\大三上\服务外包\A10-浪潮-无监督分类系统训练集-Inspur\服创大赛训练集-Inspur\Data_FCDS_hashed"
# epoch.train_all(train_data_doc)
#
predict_data_doc = "../测试数据"
epoch.predict_use_default_model(predict_data_doc) # 使用默认模型预测
# # epoch.predict_use_new_model(predict_data_doc) # 使用新数据训练的模型预测