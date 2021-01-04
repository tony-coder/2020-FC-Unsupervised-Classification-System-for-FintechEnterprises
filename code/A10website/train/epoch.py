import sys
import os

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import json
import math
import tqdm
import shutil
import time
import string
dir2=os.path.dirname(os.path.dirname(__file__))
sys.path.append(dir2)
import utils.MachineLearning as ML


# os.chdir(sys.path[0]);
# dir_name = os.path.abspath(os.path.join(os.getcwd(),"."));
# print(dir_name)
def to_percent(temp, position):
    return '%1.0f' % (100 * temp) + '%'

def get_attr_bar(infile, module_name, level_num=6):
    '''

    :param infile: 输入待统计文件
    :param weight_dict: 数据权重
    :param module_name: 模块名称
    :param 属性等级，一般为5，算上空为6;只有总模块10个等级，算上空为11
    :returns 统计矩阵，
    '''
    df = pd.read_csv(infile)
    cols = df.columns
    target_cols = []
    for col in cols:
        if col.endswith("_module_type"):
            target_cols.append(col)
    attr_cols = target_cols[:-1].copy()
    target_cols.extend([module_name + "_module_type", module_name + '_inner_type'])
    inner_type_array = df[module_name + '_inner_type']
    n_cluster = len(set(inner_type_array))

    df = df[target_cols]

    attr_num = len(attr_cols)+1
    df_values = df.values

    bar_matrix = np.zeros(shape=(n_cluster, attr_num, level_num), dtype=int)

    for i in range(n_cluster):
        for j in range(attr_num):
            for k in range(level_num):
                bar_matrix[i][j][k] = len(np.where((df_values[:, -1] == i) & (df_values[:, j] == k))[0])

    return bar_matrix, target_cols

def draw_bar_pic(bar_matrix, pic_doc, module_name, cols):
    '''
    生成每个模块占比的统计矩阵
    :param bar_matrix: 矩阵三维数组
    :param pic_doc: 图片输出目录
    :param module_name: 模块名称
    :param cols: 目标列
    :return:
    '''
    if pic_doc.endswith("/") is False:
        pic_doc += "/"

    shape = bar_matrix.shape
    print(shape)
    inner_num = shape[0]
    attr_num = shape[1]
    level_num = shape[2]

    alpha_list = string.ascii_lowercase

    x = list(range(level_num))
    print("正在生成图片...")
    for i in tqdm.tqdm(range(inner_num)):
        inner_type_sum = np.sum(bar_matrix[i, -1, :])
        plt.rc('font', family='Times New Roman')
        plt.figure(figsize=(18 * 1.0, 6 * 1.0))
        plt.subplots_adjust(wspace=0.25, hspace=0.55)
        plt.xticks(fontsize=14)
        plt.yticks(fontsize=14)

        for attr in range(attr_num):
            plt.subplot(2, 4, attr + 1)
            plt.ylim(0, 1.0)
            title = cols[attr]
            if True:  # 只有企业总评的时候，用了10个等级
                plt.xticks(list(range(level_num)))
                y = bar_matrix[i, attr, :]
                if attr != attr_num - 1:
                    plt.bar(x, y / inner_type_sum)
                else:
                    plt.bar(x, y / inner_type_sum, color='red')

            plt.xlabel('level\n(' + alpha_list[attr] + ')', fontsize=14)

            plt.title("Percent of " + title[:title.rfind('_')].capitalize(), fontsize=14)
            plt.gca().yaxis.set_major_formatter(plt.FuncFormatter(to_percent))

        pic_path = pic_doc + module_name + "_inner_type=" + str(i) + ".png"
        plt.savefig(pic_path, dpi=150, bbox_inches='tight')
        plt.close()

def ent_bar(in_file,pic_doc):
    '''
    plt.figure(figsize=(18 * 1.0, 6 * 1.0))
        plt.subplots_adjust(wspace=0.25, hspace=0.5)
    :return:
    '''
    bar_matrix, target_cols = get_attr_bar(
        infile=in_file,
        # pic_doc=r'F:\2019计算机\大三上\服务外包\服务外包算法集成\预处理第二版\all\new_evaluate\pic\bar',

        module_name='ent',
        level_num=11
    )
    draw_bar_pic(
        bar_matrix=bar_matrix,
        pic_doc=pic_doc,
        module_name='ent_module',
        cols=target_cols
    )

def get_json(file_path):
    p = open(file_path, encoding='utf-8')
    j = json.load(p)
    p.close()
    return j

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

def get_MD5(file_path):
    files_md5 = os.popen('md5 %s' % file_path).read().strip()
    file_md5 = files_md5.replace('MD5 (%s) = ' % file_path, '')
    return file_md5

def cpdoc(path, out):
    for files in os.listdir(path):
        name = os.path.join(path, files)
        back_name = os.path.join(out, files)
        if os.path.isfile(name):
            if os.path.isfile(back_name):
                if get_MD5(name) != get_MD5(back_name):
                    shutil.copy(name, back_name)
            else:
                shutil.copy(name, back_name)
        else:
            if not os.path.isdir(back_name):
                os.makedirs(back_name)
            cpdoc(name, back_name)



def f(s):
    # print(s)
    s = s.replace(',', '')
    return float(s)


class Epoch:
    def __init__(self):

        self.risk_module_file_list = [
            'administrative_punishment.csv', 'business_risk_abnormal.csv', 'business_risk_all_punish.csv',
            'business_risk_rightpledge.csv', 'business_risk_taxunpaid.csv', 'ent_social_security.csv',
            'exception_list.csv', 'justice_credit.csv', 'justice_credit_aic.csv',
            'justice_declare.csv', 'justice_enforced.csv', 'justice_judge_new.csv'
        ]
        self.investment_module_file_list = [
            'enterprise_insurance.csv', 'ent_bid.csv', 'ent_branch.csv',
            'ent_contribution.csv', 'ent_contribution_year.csv', 'ent_guarantee.csv',
            'ent_investment.csv', 'ent_onlineshop.csv'
        ]
        self.creativity_module_file_list = [
            'intangible_brand.csv', 'intangible_copyright.csv',
            'intangible_patent.csv', 'web_record_info.csv'
        ]
        self.brand_module_file_list = [
            'jn_special_new_info.csv', 'jn_tech_center.csv', 'product_checkinfo_connect.csv',
            'trademark_i nfoa.csv', 'trademark_infob.csv'
        ]
        self.recruit_module_file_list = [
            'recruit_qcwy.csv', 'recruit_zhyc.csv', 'recruit_zlzp.csv'
        ]
        self.credit_module_file_list = [
            'enterprise_keep_contract.csv', 'jn_credit_info.csv'
        ]

        self.base_module_file_list = [
            'change_info.csv', 'company_baseinfo.csv'
        ]

        self.module_list = ['risk', 'investment', 'creativity', 'brand', 'recruit', 'credit', 'base']
        self.out_file_list = []

        self.default_model_doc = "default_model_doc"
        self.new_model_doc = "new_model_doc"
        self.weight_dict = get_json("weight.json")

        self.model_doc = None

        self.start_time = time.time()
        self.end_time = 0

        self.train_total_time = 0
        self.predict_total_time = 0
        self.mode = None  # 确定是在训练还是在预测，训练则等于self.TRAIN,否则等于self.PREDICT
        self.TRAIN = "train_data/"
        self.PREDICT = "predict_data/"

    def load_data(self, doc, mode="train"):
        '''
        将指定目录的csv，加载到对应的环境下
        :param doc: csv所在目录
        :return: 
        '''
        print("# -----------------  正在装载数据  --------------------- #")
        file_dict = {
            'risk': self.risk_module_file_list,
            'investment': self.investment_module_file_list,
            'creativity': self.creativity_module_file_list,
            'brand': self.brand_module_file_list,
            'recruit': self.recruit_module_file_list,
            'credit': self.credit_module_file_list,
            'base': self.base_module_file_list
        }

        if doc.endswith("/") is False:
            doc += "/"

        file_list = os.listdir(doc)
        for file in file_list:
            for key in file_dict:
                if file in file_dict[key]:
                    shutil.copyfile(doc + file, mode + "_data/" + key + "/origin/" + file)

        print("# -----------------  数据装载完毕  --------------------- #")

    def pic_copy(self,src_doc,dst_doc):

        file_list = os.listdir(src_doc)
        for file in file_list:
            shutil.copyfile(src_doc+"/"+file,dst_doc+"/"+file)

    def init_doc(self, doc):
        if os.path.exists(doc):
            shutil.rmtree(doc)
        os.mkdir(doc)
        cpdoc(os.getcwd()+"/env/" + doc, doc)

    def init_train_enviroment(self):
        '''
        初始化训练运行环境，即清空原目录下的文件
        :return: 
        '''

        DEFAULT_MODEL_DOC = "default_model_doc"
        NEW_MODEL_DOC = "new_model_doc"
        TRAIN_DATA_DOC = "train_data"
        PREDICT_DATA_DOC = "predict_data"
        OUT_DATA_DOC = "out"
        print("# -----------------  初始化训练环境  --------------------- #")
        self.init_doc(DEFAULT_MODEL_DOC)
        self.init_doc(NEW_MODEL_DOC)
        self.init_doc(TRAIN_DATA_DOC)
        self.init_doc(PREDICT_DATA_DOC)
        del_file(OUT_DATA_DOC)
        print("# -----------------  环境初始化成功  --------------------- #")

    def init_predict_enviroment(self):
        DEFAULT_MODEL_DOC = "default_model_doc"
        NEW_MODEL_DOC = "new_model_doc"
        TRAIN_DATA_DOC = "train_data"
        PREDICT_DATA_DOC = "predict_data"
        OUT_DATA_DOC = "out"
        print("# -----------------  初始化预测环境  --------------------- #")
        self.init_doc(PREDICT_DATA_DOC)
        del_file(OUT_DATA_DOC)
        print("# -----------------  环境初始化成功  --------------------- #")
    def merge_df(self, df_list, post_fix=None):
        '''
        将所有的df根据entname外连接在一起
        :param df_list: dataframe的list
        :param post_fix: 合并属性后缀名
        :return: 
        '''
        if post_fix is not None:
            for i in range(len(df_list)):
                target_cols = ['entname']
                for col in df_list[i].columns:
                    if col.endswith(post_fix):
                        target_cols.append(col)
                df_list[i] = df_list[i][target_cols]

        out_df = pd.DataFrame()
        index = 0
        for df in df_list:
            if index == 0:
                index += 1
                out_df = df
            else:
                out_df = pd.merge(out_df, df, how='outer', left_on='entname', right_on='entname')

        return out_df.fillna(0)

    def get_attr_type(self, filename, module_name, attr_name_list=None, level=5):
        df = None
        if self.mode == self.TRAIN:
            df = self.train_attr_type(filename=filename, module_name=module_name, attr_name_list=attr_name_list,
                                      level=level)
        else:
            # print()
            df = self.predict_attr_type(filename=filename, module_name=module_name, attr_name_list=attr_name_list)

        return df

    def train_attr_type(self, filename, module_name, attr_name_list=None, level=5):
        '''
        获得属性的等级
        :param filename: 文件名 
        :param module_name: 模块名
        :param attr_name_list: 待训练属性列表
        :param level: 等级
        :return: 
        '''

        df = pd.read_csv(filename, encoding='gbk')
        if attr_name_list is None:
            attr_name_list = df.columns[1:]

        # print(filename.split("/"))
        real_file_name = filename.split("/")[-1].split('.')[0]
        for attr in attr_name_list:
            model_path = self.new_model_doc + "/" + module_name + "/" + real_file_name + "-" + attr + ".m"
            values = df[attr].values.flatten()

            a = time.time()
            labels = ML.KMeans_train_predict(
                data_matrix=values,
                n_cluster=level,
                make_model=True,
                model_path=model_path
            )
            self.train_total_time += time.time() - a
            df[attr + "_type"] = labels

        return df

    def predict_attr_type(self, filename, module_name, attr_name_list=None):
        real_file_name = filename.split("/")[-1].split(".")[0]
        # print(real_file_name)
        df = pd.read_csv(filename, encoding='gbk')
        if len(df) == 0:
            return False
        if attr_name_list is None:
            attr_name_list = df.columns[1:]
        # print(len(attr_name_list))
        # print(df)
        for attr in attr_name_list:
            model_path = self.model_doc + module_name + "/" + real_file_name + "-" + attr + ".m"

            model = ML.load_model(model_path)
            labels = ML.predict(df[attr].values.flatten(), model)
            df[attr + "_type"] = labels

        return df

    def get_module_total_mark_and_get_type(self, df, module_name):
        out_df = None
        if self.mode == self.TRAIN:
            out_df = self.train_module_total_mark_and_get_type(df, module_name)
        else:
            out_df = self.predict_module_total_mark_and_get_type(df, module_name)
        return out_df

    def train_module_total_mark_and_get_type(self, df, module_name):
        '''
        获取该模块汇总的总分，以及对应的总分等级
        :param df: 输入dataframe 
        :param module_name: 模块名称
        :return: 
        '''
        attr_cols = df.columns[1:]
        df[module_name + "_module"] = np.zeros(shape=len(df), dtype=float)

        # print(attr_cols)
        # print(self.weight_dict[module_name + "_module"])
        if self.weight_dict[module_name + "_module"] is None or len(self.weight_dict[module_name + "_module"]) == 0:
            for attr in attr_cols:
                df[module_name + "_module"] += df[attr]
        else:
            for attr in attr_cols:
                df[module_name + "_module"] += self.weight_dict[module_name + "_module"][attr] * df[attr]
        model_path = self.new_model_doc + "/" + module_name + "/" + module_name + "_module_mark.m"
        # print(df[module_name + "_module"].values.flatten())
        a = time.time()
        labels = ML.KMeans_train_predict(
            data_matrix=df[module_name + "_module"].values.flatten(),
            n_cluster=10,
            make_model=True,
            model_path=model_path
        )
        self.train_total_time += time.time() - a
        df[module_name + "_module_type"] = labels
        return df

    def predict_module_total_mark_and_get_type(self, df, module_name):
        '''
        获取该模块汇总的总分，以及对应的总分等级
        :param df: 输入dataframe 
        :param module_name: 模块名称
        :return: 
        '''
        attr_cols = df.columns[1:]
        df[module_name + "_module"] = np.zeros(shape=len(df), dtype=float)

        # print(attr_cols)
        # print(self.weight_dict[module_name + "_module"])
        if self.weight_dict[module_name + "_module"] is None or len(self.weight_dict[module_name + "_module"]) == 0:
            for attr in attr_cols:
                df[module_name + "_module"] += df[attr]
        else:
            for attr in attr_cols:
                df[module_name + "_module"] += self.weight_dict[module_name + "_module"][attr] * df[attr]
        model_path = self.model_doc + module_name + "/" + module_name + "_module_mark.m"
        # print(df[module_name + "_module"].values.flatten())
        a = time.time()
        model = ML.load_model(model_path)
        labels = ML.predict(
            data_matrix=df[module_name + "_module"].values.flatten(),
            model=model
        )
        self.train_total_time += time.time() - a
        df[module_name + "_module_type"] = labels
        return df

    # -----------------  risk  --------------------- #

    def risk_deal_taxunpaidnum(self, in_file, out_file):

        df = pd.read_csv(in_file).fillna(0)
        df['taxunpaidnum'] = df['taxunpaidnum'].apply(f)
        tmp_df = df.groupby("entname").sum().reset_index()
        tmp_df.to_csv(out_file, index=False)

    def risk_deal_social_security(self, in_file, out_file):

        cols = "entname,unpaidsocialins_so110,unpaidsocialins_so210,unpaidsocialins_so310,unpaidsocialins_so410,unpaidsocialins_so510".split(",")
        df = pd.read_csv(in_file,usecols=cols)
        df['unpaid_sum'] = df['unpaidsocialins_so110'] + df['unpaidsocialins_so210'] + df[
            'unpaidsocialins_so310'] + df['unpaidsocialins_so410'] + df['unpaidsocialins_so510']
        df = df.loc[df['unpaid_sum'] != 0]
        df = df.drop(cols[1:], axis=1)
        tmp_df = df.groupby("entname").sum().reset_index()
        tmp_df.to_csv(out_file, index=False)

    def risk_deal_enforced(self, in_file, out_file):
        df = pd.read_csv(in_file, usecols=['entname', 'enforce_amount'], encoding='gbk')
        # 统计每个公司被执行总金额
        tmp_df = df.groupby("entname").sum().reset_index()
        tmp_df.to_csv(out_file, index=False)

    def risk_deal_judge_new(self, in_file, out_file):
        df = pd.read_csv(in_file, usecols=['entname'])
        df['judge_new_count'] = np.zeros(len(df),dtype=int)
        tmp_df = df.groupby("entname").count().reset_index()
        tmp_df.to_csv(out_file, index=False)

    def risk_deal_justice_declare(self, in_file, out_file):
        usecols = "entname,appellant,defendant".split(",")
        df = pd.read_csv(in_file, usecols=usecols)
        tmp_df = df.groupby("entname").sum().reset_index()
        tmp_df.rename(inplace=True,columns={"appellant":"appellant_amount","defendant":"defendant_amount"})
        tmp_df.to_csv(out_file, index=False)

    def deal_risk(self):
        '''
        统一处理风险模块下的所有文件，训练部分
        :return: 
        '''
        print("# -----------------  risk  --------------------- #")
        module_name = "risk"
        origin_data_doc = self.mode + module_name + "/origin/"
        middle_data_doc = self.mode + module_name + "/middle/"
        dealed_data_doc = self.mode + module_name + "/dealed/dealed_"
        module_data_doc = self.mode + module_name + "/module/"

        file_list = os.listdir(origin_data_doc)
        if len(file_list) == 0:
            return

        df_list = []

        for file in file_list:
            print(file)
            if file == "business_risk_taxunpaid.csv":
                self.risk_deal_taxunpaidnum(in_file=origin_data_doc + file,
                                            out_file=middle_data_doc + file)
                df = self.get_attr_type(
                    filename=middle_data_doc + file,
                    module_name=module_name,
                    attr_name_list=None
                )

            elif file == "ent_social_security.csv":
                self.risk_deal_social_security(in_file=origin_data_doc + file,
                                               out_file=middle_data_doc + file)
                df = self.get_attr_type(
                    filename=middle_data_doc + file,
                    module_name=module_name,
                    attr_name_list=None
                )
                if df is False:
                    continue

            elif file == "justice_enforced.csv":
                self.risk_deal_enforced(in_file=origin_data_doc + file,
                                        out_file=middle_data_doc + file)

                df = self.get_attr_type(
                    filename=middle_data_doc + file,
                    module_name=module_name,
                    attr_name_list=None
                )

            elif file == "justice_judge_new.csv":
                self.risk_deal_judge_new(in_file=origin_data_doc + file,
                                         out_file=middle_data_doc + file)
                df = self.get_attr_type(
                    filename=middle_data_doc + file,
                    module_name=module_name,
                    attr_name_list=None
                )
            elif file == "justice_declare.csv":
                self.risk_deal_justice_declare(in_file=origin_data_doc + file,
                                               out_file=middle_data_doc + file)
                df = self.get_attr_type(
                    filename=middle_data_doc + file,
                    module_name=module_name,
                    attr_name_list=["appellant_amount", "defendant_amount"]
                )
            else:
                df = self.get_attr_type(
                    filename=origin_data_doc + file,
                    module_name=module_name,
                    attr_name_list=None
                )
            df_list.append(df.copy())
            df.to_csv(dealed_data_doc + file, index=False)

        print("Merge " + module_name + " module...")
        module_df = self.merge_df(df_list, post_fix="_type")
        module_df = self.get_module_total_mark_and_get_type(df=module_df, module_name=module_name)
        module_df.to_csv(module_data_doc + module_name + "_module.csv", index=False)
        self.out_file_list.append(module_data_doc + module_name + "_module.csv")
        df_list.clear()

    # -----------------  investment  --------------------- #
    def investment_deal_ent_contribution(self, in_file, out_file):
        df = pd.read_csv(in_file, usecols=['entname', 'subconam']).fillna(0)
        tmp_df = df.groupby("entname").sum().reset_index()
        tmp_df.rename(inplace=True,columns={"subconam":"subconam_total"})
        tmp_df.to_csv(out_file, index=False)

    def investment_deal_ent_contribution_year(self, in_file, out_file):
        usecols = "entname,liacconam,lisubconam".split(",")
        df = pd.read_csv(in_file, usecols=usecols).fillna(0)
        tmp_df = df.groupby("entname").sum().reset_index()
        tmp_df.rename(inplace=True,columns={"liacconam":"liacconam_total","lisubconam":"lisubconam_total"})
        tmp_df.to_csv(out_file, index=False)

    def deal_investment(self):
        '''
        统一处理风险模块下的所有文件，训练部分
        :return: 
        '''
        print("# -----------------  investment  --------------------- #")
        module_name = "investment"
        origin_data_doc = self.mode + module_name + "/origin/"
        middle_data_doc = self.mode + module_name + "/middle/"
        dealed_data_doc = self.mode + module_name + "/dealed/dealed_"
        module_data_doc = self.mode + module_name + "/module/"

        file_list = os.listdir(origin_data_doc)
        if len(file_list) == 0:
            return
        df_list = []
        for file in file_list:
            print(file)
            if file == "ent_contribution.csv":
                self.investment_deal_ent_contribution(in_file=origin_data_doc + file,
                                                      out_file=middle_data_doc + file)
                df = self.get_attr_type(
                    filename=middle_data_doc + file,
                    module_name=module_name,
                    attr_name_list=None
                )
                # df_list.append(df.copy())
                # df.to_csv(dealed_data_doc + file, index=False)

            elif file == "ent_contribution_year.csv":
                # pass
                self.investment_deal_ent_contribution_year(in_file=origin_data_doc + file,
                                                           out_file=middle_data_doc + file)
                df = self.get_attr_type(
                    filename=middle_data_doc + file,
                    module_name=module_name,
                    attr_name_list=None
                )

            elif file == "enterprise_insurance.csv":  # 保险的不处理
                continue
            elif file == "ent_guarantee.csv":  # 债权不处理
                continue
            else:
                df = self.get_attr_type(
                    filename=origin_data_doc + file,
                    module_name=module_name,
                    attr_name_list=None
                )
            df_list.append(df.copy())
            df.to_csv(dealed_data_doc + file, index=False)

        print("Merge " + module_name + " module...")
        module_df = self.merge_df(df_list, post_fix="_type")
        module_df = self.get_module_total_mark_and_get_type(df=module_df, module_name=module_name)
        module_df.to_csv(module_data_doc + module_name + "_module.csv", index=False)
        self.out_file_list.append(module_data_doc + module_name + "_module.csv")
        df_list.clear()

    # -----------------  creativity  --------------------- #
    def deal_creativity(self):
        print("# -----------------  creativity  --------------------- #")
        module_name = "creativity"
        origin_data_doc = self.mode + module_name + "/origin/"
        middle_data_doc = self.mode + module_name + "/middle/"
        dealed_data_doc = self.mode + module_name + "/dealed/dealed_"
        module_data_doc = self.mode + module_name + "/module/"

        file_list = os.listdir(origin_data_doc)
        if len(file_list) == 0:
            return
        df_list = []
        for file in file_list:
            print(file)
            df = self.get_attr_type(
                filename=origin_data_doc + file,
                module_name=module_name,
                attr_name_list=None
            )
            df_list.append(df.copy())
            df.to_csv(dealed_data_doc + file, index=False)

        print("Merge " + module_name + " module...")
        module_df = self.merge_df(df_list, post_fix="_type")
        module_df = self.get_module_total_mark_and_get_type(df=module_df, module_name=module_name)
        module_df.to_csv(module_data_doc + module_name + "_module.csv", index=False)
        self.out_file_list.append(module_data_doc + module_name + "_module.csv")
        df_list.clear()

    # -----------------  brand  --------------------- #

    def brand_deal_jn_tech_center(self, in_file, out_file):
        df = pd.read_csv(in_file, encoding='gbk')
        d = {"市级": 1, "省级": 2}
        df['level_rank'] = df['level_rank'].map(d)
        print(df)

        df.to_csv(out_file, index=False)

    def deal_brand(self):
        print("# -----------------  brand  --------------------- #")
        module_name = "brand"
        origin_data_doc = self.mode + module_name + "/origin/"
        middle_data_doc = self.mode + module_name + "/middle/"
        dealed_data_doc = self.mode + module_name + "/dealed/dealed_"
        module_data_doc = self.mode + module_name + "/module/"

        file_list = os.listdir(origin_data_doc)
        if len(file_list) == 0:
            return
        df_list = []
        for file in file_list:
            print(file)
            if file == "jn_tech_center.csv":
                self.brand_deal_jn_tech_center(in_file=origin_data_doc + file,
                                               out_file=middle_data_doc + file)
                df = self.get_attr_type(
                    filename=middle_data_doc + file,
                    module_name=module_name,
                    attr_name_list=None
                )
            else:
                df = self.get_attr_type(
                    filename=origin_data_doc + file,
                    module_name=module_name,
                    attr_name_list=None
                )
            df_list.append(df.copy())
            df.to_csv(dealed_data_doc + file, index=False)

        print("Merge " + module_name + " module...")
        module_df = self.merge_df(df_list, post_fix="_type")
        module_df = self.get_module_total_mark_and_get_type(df=module_df, module_name=module_name)
        module_df.to_csv(module_data_doc + module_name + "_module.csv", index=False)
        self.out_file_list.append(module_data_doc + module_name + "_module.csv")
        df_list.clear()

    # -----------------  recruit  --------------------- #
    def deal_recruit(self):
        print("# -----------------  recruit  --------------------- #")
        module_name = "recruit"
        origin_data_doc = self.mode + module_name + "/origin/"
        middle_data_doc = self.mode + module_name + "/middle/"
        dealed_data_doc = self.mode + module_name + "/dealed/dealed_"
        module_data_doc = self.mode + module_name + "/module/"

        file_list = os.listdir(origin_data_doc)
        if len(file_list) == 0:
            return
        df_list = []
        for file in file_list:
            print(file)
            df = pd.read_csv(origin_data_doc + file)
            df_list.append(df.copy())
            # df.to_csv(dealed_data_doc + file, index=False)

        print("Merge " + module_name + " module...")
        module_df = self.merge_df(df_list, post_fix=None)
        # print(module_df)
        module_df = self.get_module_total_mark_and_get_type(df=module_df, module_name=module_name)
        module_df.to_csv(module_data_doc + module_name + "_module.csv", index=False)
        self.out_file_list.append(module_data_doc + module_name + "_module.csv")
        df_list.clear()

    # -----------------  credit  --------------------- #
    def credit_deal_jn_credit_info(self, in_file, out_file):
        print("# -----------------  credit  --------------------- #")
        credit_dict = {
            'C': 0, 'B-': 1, 'A-': 2,
            'A': 3, 'N': 4, 'N+': 5
        }
        df = pd.read_csv(in_file)
        df['credit_grade_num'] = df['credit_grade'].map(credit_dict)
        df.to_csv(out_file, index=False)

    def deal_credit(self):
        module_name = "credit"
        origin_data_doc = self.mode + module_name + "/origin/"
        middle_data_doc = self.mode + module_name + "/middle/"
        dealed_data_doc = self.mode + module_name + "/dealed/dealed_"
        module_data_doc = self.mode + module_name + "/module/"

        file_list = os.listdir(origin_data_doc)
        if len(file_list) == 0:
            return
        df_list = []
        for file in file_list:

            print(file)
            if file == "jn_credit_info.csv":
                self.credit_deal_jn_credit_info(in_file=origin_data_doc + file,
                                                out_file=middle_data_doc + file)
                df = self.get_attr_type(
                    filename=middle_data_doc + file,
                    module_name=module_name,
                    attr_name_list=['credit_grade_num']
                )
                df_list.append(df.copy())
                df.to_csv(dealed_data_doc + file, index=False)
            else:
                df = self.get_attr_type(
                    filename=origin_data_doc + file,
                    module_name=module_name,
                    attr_name_list=None
                )
                df_list.append(df.copy())
                df.to_csv(dealed_data_doc + file, index=False)

        print("Merge " + module_name + " module...")
        module_df = self.merge_df(df_list, post_fix="_type")
        module_df = self.get_module_total_mark_and_get_type(df=module_df, module_name=module_name)
        module_df.to_csv(module_data_doc + module_name + "_module.csv", index=False)
        self.out_file_list.append(module_data_doc + module_name + "_module.csv")
        df_list.clear()

    # -----------------  base  --------------------- #
    def deal_base(self):
        print("# -----------------  base  --------------------- #")
        module_name = "base"
        origin_data_doc = self.mode + module_name + "/origin/"
        middle_data_doc = self.mode + module_name + "/middle/"
        dealed_data_doc = self.mode + module_name + "/dealed/dealed_"
        module_data_doc = self.mode + module_name + "/module/"

        file = "company_baseinfo.csv"
        if os.path.exists(origin_data_doc + file) is False:
            return
        df = pd.read_csv(origin_data_doc + file, usecols=['entname', 'regcap', 'enttype'], encoding='gbk').fillna(0)

        farm_df = df.loc[df['enttype'] == "农民专业合作经济组织"]
        farm_df['regcap'] = farm_df['regcap'].values.flatten() / 10000
        other_df = df.loc[df['enttype'] != "农民专业合作经济组织"]
        df = pd.concat([farm_df, other_df])
        df.drop(columns=['enttype'])
        # print(df)

        labels = None
        a = time.time()
        if self.mode == self.TRAIN:
            model_path = self.new_model_doc + "/" + module_name + "/" + module_name + "_module_mark.m"
            labels = ML.KMeans_train_predict(
                data_matrix=df['regcap'].values.flatten(),
                n_cluster=10,
                make_model=True,
                model_path=model_path
            )
        else:

            model_path = self.model_doc + "/" + module_name + "/" + module_name + "_module_mark.m"
            model = ML.load_model(model_path)
            labels = ML.predict(
                data_matrix=df['regcap'].values.flatten(),
                model=model
            )
        self.train_total_time += time.time() - a
        df['regcap_type'] = labels
        df['base_module_type'] = labels
        df.to_csv(module_data_doc + module_name + "_module.csv",
                  columns=['entname', 'regcap', 'regcap_type', 'base_module_type'], index=False)
        self.out_file_list.append(module_data_doc + module_name + "_module.csv")

    def out_file(self):
        for file in self.out_file_list:
            out_file = "out/"+file.split("/")[-1]
            shutil.copyfile(file,out_file)

    def merge_mark(self):

        base_doc = self.mode
        module_name = "ent"
        # print(module_name)
        file_list = []
        for mo in self.module_list:
            filename = base_doc + mo + "/module/" + mo + "_module.csv"
            file_list.append(filename)

        df_list = []
        for i in range(len(self.module_list)):
            file = file_list[i]
            mo = self.module_list[i]
            if os.path.exists(file) is False:
                continue
            print(file.split("/")[-1])
            df_list.append(pd.read_csv(file, usecols=['entname', mo + "_module_type"]))
        if len(df_list) == 0:
            return

        out_df = self.merge_df(df_list)
        # print(out_df)
        data_matrix = out_df[out_df.columns[1:]].values
        model_path = self.new_model_doc + "/" + module_name + "/ent_inner_C15.m"
        a = time.time()
        if self.mode == self.TRAIN:
            inner_labels = ML.KM(data_matrix=data_matrix, C=15, is_ascend=False,
                                 model_path=model_path)  # 内部聚簇
        else:
            model = ML.load_model(model_path)
            inner_labels = ML.inner_predict(data_matrix=data_matrix, model=model)

        self.train_total_time = time.time() - a

        out_df = self.get_module_total_mark_and_get_type(df=out_df, module_name=module_name)  # 获取总分，总分等级
        out_df['ent_inner_type'] = inner_labels
        out_df.to_csv(self.mode + module_name + "/module/ent_module.csv", index=False)
        print(self.mode + module_name + "/module/ent_module.csv")
        self.out_file_list.append(self.mode + module_name + "/module/ent_module.csv")

    def generate_inner_describe_pic(self):
        doc = "out/pic"
        os.mkdir(doc)
        ent_bar(in_file=self.out_file_list[-1],pic_doc=doc)
        file_list = os.listdir(doc)
        del_file("env/new_pic") # 先清空目录下的图片
        for file in file_list:
            src = doc+"/"+file
            shutil.copyfile(src,"env/new_pic/"+file) # 复制到env中

    def run(self, mode="train", model_mode="old"):
        self.out_file_list.clear()
        if mode == "train":
            self.mode = "train_data/"
        else:
            self.mode = "predict_data/"

        print(self.mode)
        if model_mode == "old" or "default":
            self.model_doc = "default_model_doc/"
        else:
            self.model_doc = "new_model_doc/"

        print("# -----------------  " + mode + "  --------------------- #")
        self.deal_risk()
        self.deal_investment()
        self.deal_creativity()
        self.deal_brand()
        self.deal_recruit()
        self.deal_credit()
        self.deal_base()
        self.merge_mark()
        self.out_file()
        self.end_time = time.time()
        print("# -----------------  over  --------------------- #")
        print("所有要返回给前端的csv的相对目录：", self.out_file_list)
        print("系統总运行时间：", self.end_time - self.start_time)
        print("训练或预测总时间：", self.train_total_time)
        print("数据预处理时间：",self.end_time - self.start_time - self.train_total_time)
        # if self.mode == "train_data/":
        #
        # else:
        if self.mode == self.TRAIN:
            self.generate_inner_describe_pic()
        else:
            os.mkdir("out/pic")
            # print(model_mode)
            if model_mode == "old" or model_mode == "default":
                # print("!!!!!!!!!!!")
                self.pic_copy("env/default_pic","out/pic")
            else:
                # print("????????????????")
                self.pic_copy("env/new_pic", "out/pic")





    def train_all(self,csv_doc):
        self.init_train_enviroment()
        self.load_data(doc=csv_doc,mode='train')
        self.run(mode="train",model_mode="old")

    def predict_use_default_model(self,csv_doc):
        self.init_predict_enviroment()
        self.load_data(doc=csv_doc,mode="predict")
        self.run(mode="predict",model_mode="old")

    def predict_use_new_model(self,csv_doc):
        self.init_predict_enviroment()
        self.load_data(doc=csv_doc, mode="predict")
        self.run(mode="predict", model_mode="new")
