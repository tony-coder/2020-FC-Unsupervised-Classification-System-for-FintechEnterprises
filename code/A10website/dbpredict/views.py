import shutil

import pandas as pd
import numpy as np
import time

from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from tqdm import tqdm

from dataTojson.models import *
from search.models import EntModule
from upload.views import un_zip
from utils.MachineLearning import predict, load_model, inner_predict

# credit

credit_level_dict = {
    'C-': 0, 'C': 1, 'C+': 2,
    'B-': 3, 'B': 4, 'B+': 5,
    'A-': 6, 'A': 7, 'A+': 8,
    'A-': 9, 'A': 10, 'N+': 11
}


# N+,N,A,A-,B,C
credit_dict = {
    'C': 0, 'B-': 1, 'A-': 2,
    'A': 3, 'N': 4, 'N+': 5
}


risk_weight_dict = {
    "is_punish_type": 1,
    "is_bra_type": 1,
    "is_brap_type": 1,
    "pledgenum_type": 1,
    "taxunpaidnum_type": 1.5,
    "unpaid_sum_type": 0.7,
    "is_except_type": 1,
    "declaredate_type": 0.2,
    "appellant_amount_type": 0.3,
    "defendant_amount_type": 0.6,
    "record_date_type": 0.3,
    "enforce_amount_type": 1.8,
    "judge_new_count_type": 0.5,
    "is_justice_credit_type": 1,
    "is_justice_creditaic_type": 0.6
}

investment_weight_dict = {
    "insurance_num_type": 0.3,
    "bidnum_type": 2,
    "branchnum_type": 2,
    "subconam_total_type": 1,
    "liacconam_total_type": 0.4,
    "lisubconam_total_type": 0.4,
    "investnum_type": 2,
    "shopnum_type": 2
}

creativity_weight_dict = {
    "ibrand_num_type": 1,
    "icopy_num_type": 1,
    "ipat_num_type": 1,
    "idom_num_type": 1
}

brand_weight_dict = {
    "is_jnsn_type": 1.3,
    "level_rank_type": 1.5,
    "is_infoa_type": 1.5,
    "is_infob_type": 1,
    "passpercent_type": 0.7
}

credit_weight_dict = {
    'is_kcont_type': 1.3,
    'credit_grade_num_type': 0.9
}

ent_weight_dict = {
    "risk_module_type": -1.11,
    "investment_module_type": 1,
    "creativity_module_type": 1,
    "brand_module_type": 1,
    "recruit_module_type": 1,
    "credit_module_type": 1,
    "company_baseinfo_module_type": 1
  }


def get_module_mark(module,weigh_dict):
    sum = 0
    for key, value in weigh_dict.items():
        attr = getattr(module,key)
        if attr == None:
            attr = 0
        sum += attr * value
    return sum





def recruit_predict(file_path,model_path):

    df = pd.read_csv(file_path,sep=',')
    file_postfix = file_path.split('/')[-1].split('.')[0][-4:]

    key = file_postfix + 'num'
    ent_model_path = model_path + '/ent/ent_module_mark.m'
    ent_inner_model_path = model_path + '/ent/ent_inner_C15.m'
    model_path = model_path + '/recruit/recruit_module_mark.m'
    model = load_model(model_path)
    ent_model = load_model(ent_model_path)
    ent_inner_model = load_model(ent_inner_model_path)

    newEntList = []
    newEntList_entmodule = []
    count_ent_module = 0
    count = 0

    for row in tqdm(df.iterrows()):
        entname = row[1]['entname']
        key_value = row[1][key]

        oldEnt = RecruitModule.objects.filter(entname__exact=entname)
        oldEntModule = EntModule.objects.filter(entname__exact=entname)

        if len(oldEnt):
            if key == 'qcwynum':
                oldEnt[0].qcwynum += key_value
            elif key == 'zhycnum':
                oldEnt[0].zhycnum += key_value
            else:
                oldEnt[0].zlzpnum += key_value

            oldEnt[0].recruit_module += key_value

            recruit_module_type = predict(np.array(oldEnt[0].recruit_module), model)[0]
            oldEnt[0].recruit_module_type = recruit_module_type
            oldEnt[0].save()

            if len(oldEntModule):
                oldEntModule[0].recruit_module_type = recruit_module_type
                ent_mark = get_module_mark(oldEntModule[0], ent_weight_dict)
                oldEntModule[0].ent = ent_mark

                oldEntModule[0].ent_type = predict(ent_mark, model=ent_model)
                ent_type_list = get_ent_module_type_list(entmodule=oldEntModule[0], weight_dict=ent_weight_dict)
                oldEntModule[0].ent_inner_type = inner_predict(ent_type_list, ent_inner_model)

                oldEntModule[0].save()

            else:
                newEntModule = EntModule(entname=entname, company_baseinfo_module_type=0,
                                         risk_module_type=0, investment_module_type=0, creativity_module_type=0,
                                         brand_module_type=0, recruit_module_type=recruit_module_type, credit_module_type=0)
                ent_mark = get_module_mark(newEntModule, ent_weight_dict)
                newEntModule.ent = ent_mark
                newEntModule.ent_type = predict(ent_mark, model=ent_model)
                ent_type_list = get_ent_module_type_list(entmodule=newEntModule, weight_dict=ent_weight_dict)
                newEntModule.ent_inner_type = inner_predict(ent_type_list, ent_inner_model)

                newEntList_entmodule.append(newEntModule)
                count_ent_module += 1

                if count_ent_module / 5000 == 1:
                    EntModule.objects.bulk_create(newEntList_entmodule)
                    newEntList_entmodule = []
                    count_ent_module = 0

        else:
            recruit_module_type = predict(np.array(key_value), model)[0]

            if len(oldEntModule):
                oldEntModule[0].recruit_module_type = recruit_module_type
                ent_mark = get_module_mark(oldEntModule[0], ent_weight_dict)
                oldEntModule[0].ent = ent_mark

                oldEntModule[0].ent_type = predict(ent_mark, model=ent_model)
                ent_type_list = get_ent_module_type_list(entmodule=oldEntModule[0], weight_dict=ent_weight_dict)
                oldEntModule[0].ent_inner_type = inner_predict(ent_type_list, ent_inner_model)

                oldEntModule[0].save()

            else:
                newEntModule = EntModule(entname=entname, company_baseinfo_module_type=0,
                                         risk_module_type=0, investment_module_type=0, creativity_module_type=0,
                                         brand_module_type=0, recruit_module_type=recruit_module_type,
                                         credit_module_type=0)
                ent_mark = get_module_mark(newEntModule, ent_weight_dict)
                newEntModule.ent = ent_mark
                newEntModule.ent_type = predict(ent_mark, model=ent_model)
                ent_type_list = get_ent_module_type_list(entmodule=newEntModule, weight_dict=ent_weight_dict)
                newEntModule.ent_inner_type = inner_predict(ent_type_list, ent_inner_model)

                newEntList_entmodule.append(newEntModule)
                count_ent_module += 1

                if count_ent_module / 5000 == 1:
                    EntModule.objects.bulk_create(newEntList_entmodule)
                    newEntList_entmodule = []
                    count_ent_module = 0



            if key == 'qcwynum':
                newEnt = RecruitModule(entname=entname, qcwynum=key_value, zhycnum=0, zlzpnum=0,recruit_module=key_value,recruit_module_type=recruit_module_type)
            elif key == 'zhycnum':
                newEnt = RecruitModule(entname=entname, qcwynum=0, zhycnum=key_value, zlzpnum=0,recruit_module=key_value,recruit_module_type=recruit_module_type)
            else:
                newEnt = RecruitModule(entname=entname, qcwynum=0, zhycnum=0, zlzpnum=key_value,recruit_module=key_value,recruit_module_type=recruit_module_type)
            newEntList.append(newEnt)
            count += 1

            if count / 5000 == 1:
                EntModule.objects.bulk_create(newEntList)
                newEntList = []
                count = 0

    RecruitModule.objects.bulk_create(newEntList)
    EntModule.objects.bulk_create(newEntList_entmodule)

# credit
# def get_credit_module_mark(credit_module,credit_weight_dict):
#     credit_module_mark = credit_module.is_kcont_type * credit_weight_dict['is_kcont_type'] +  credit_module.credit_grade_type * credit_weight_dict['credit_grade_type']
#     return credit_module_mark


def deal_level(file_path):
    data = pd.read_csv(file_path,sep=',')
    data['credit_grade_num'] = data['credit_grade'].map(credit_dict)
    data.fillna(1)

    print(data.isnull().sum())

    for row in data.iterrows():
        entname = row[1]['entname']
        credit_grade = row[1]['credit_grade']
        credit_grade_num = row[1]['credit_grade_num']

        if credit_grade_num == None:
            print(entname)
            print(credit_grade)
            print(credit_grade_num)
    return data

def jn_credit_info_predict(file_path,model_path):
    data_matrix = deal_level(file_path)
    print(data_matrix)

    ent_model_path = model_path + '/ent/ent_module_mark.m'
    ent_inner_model_path = model_path + '/ent/ent_inner_C15.m'
    ent_credit_model_path = model_path + '/credit/credit_module_mark.m'
    model_path = model_path + '/credit/jn_credit_info-credit_grade_num.m'
    model = load_model(model_path)
    ent_model = load_model(ent_model_path)
    ent_inner_model = load_model(ent_inner_model_path)
    ent_credit_model = load_model(ent_credit_model_path)


    newEntList = []
    newEntList_credit_module = []
    newEntList_ent_module = []

    count = 0
    count_credit_module = 0
    count_ent_module = 0

    for row in tqdm(data_matrix.iterrows()):
        entname = row[1]['entname']
        credit_grade = row[1]['credit_grade']
        credit_grade_num = row[1]['credit_grade_num']

        oldEnt = JnCreditInfo.objects.filter(entname__exact=entname)
        oldEnt_credit_module = CreditModule.objects.filter(entname__exact=entname)
        oldEnt_ent_module = EntModule.objects.filter(entname__exact=entname)

        credit_grade_num_type = 0

        # 本表
        if len(oldEnt):
            oldEnt[0].credit_grade = credit_grade
            oldEnt[0].credit_grade_num = credit_grade_num
            credit_grade_num_type = predict(np.array(oldEnt[0].credit_grade_num), model)[0]
            oldEnt[0].credit_grade_num_type = credit_grade_num_type

            oldEnt[0].save()
        else:
            credit_grade_num_type = predict(np.array(credit_grade_num), model)[0]
            newEnt = JnCreditInfo(entname=entname,credit_grade=credit_grade,credit_grade_num=credit_grade_num,credit_grade_num_type=credit_grade_num_type)
            newEntList.append(newEnt)
            count += 1

            if count / 5000 == 1:
                JnCreditInfo.objects.bulk_create(newEntList)
                newEntList = []
                count = 0

        credit_module_type = 0

        # credit_module
        if len(oldEnt_credit_module):
            oldEnt_credit_module[0].credit_grade_num_type = credit_grade_num_type
            ent_credit_module_mark = get_module_mark(oldEnt_credit_module[0], credit_weight_dict)
            oldEnt_credit_module[0].credit_module = ent_credit_module_mark
            credit_module_type = predict(ent_credit_module_mark, model=ent_credit_model)
            oldEnt_credit_module[0].credit_module_type = credit_module_type

            oldEnt_credit_module[0].save()

        else:
            new_credit_module = CreditModule(entname=entname, is_kcont_type=0, credit_grade_num_type=credit_grade_num_type)
            ent_credit_module_mark = get_module_mark(new_credit_module, credit_weight_dict)
            new_credit_module.credit_module = ent_credit_module_mark
            credit_module_type = predict(ent_credit_module_mark,model=ent_credit_model)
            new_credit_module.credit_module_type = credit_module_type
            newEntList_credit_module.append(new_credit_module)

            count_credit_module += 1
            if count_credit_module / 5000 == 1:
                CreditModule.objects.bulk_create(newEntList_credit_module)
                newEntList_credit_module = []
                count_credit_module = 0


        # ent_module
        if len(oldEnt_ent_module):
            oldEnt_ent_module[0].credit_module_type = credit_module_type
            ent_mark = get_module_mark(oldEnt_ent_module[0], ent_weight_dict)
            oldEnt_ent_module[0].ent = ent_mark

            oldEnt_ent_module[0].ent_type = predict(ent_mark, model=ent_model)
            ent_type_list = get_ent_module_type_list(entmodule=oldEnt_ent_module[0], weight_dict=ent_weight_dict)
            oldEnt_ent_module[0].ent_inner_type = inner_predict(ent_type_list, ent_inner_model)

            oldEnt_ent_module[0].save()



        else:
            newEntModule = EntModule(entname=entname, company_baseinfo_module_type=0,
                                     risk_module_type=0, investment_module_type=0, creativity_module_type=0,
                                     brand_module_type=0, recruit_module_type=0,
                                     credit_module_type=credit_module_type)
            ent_mark = get_module_mark(newEntModule, ent_weight_dict)
            newEntModule.ent = ent_mark
            newEntModule.ent_type = predict(ent_mark, model=ent_model)
            ent_type_list = get_ent_module_type_list(entmodule=newEntModule, weight_dict=ent_weight_dict)
            newEntModule.ent_inner_type = inner_predict(ent_type_list, ent_inner_model)

            newEntList_ent_module.append(newEntModule)
            count_ent_module += 1

            if count_ent_module / 5000 == 1:
                EntModule.objects.bulk_create(newEntList_ent_module)
                newEntList_ent_module = []
                count_ent_module = 0


    JnCreditInfo.objects.bulk_create(newEntList)
    CreditModule.objects.bulk_create(newEntList_credit_module)
    EntModule.objects.bulk_create(newEntList_ent_module)



def enterprise_keep_contract_predict(file_path,model_path):
    data_matrix = pd.read_csv(file_path,sep=',')

    ent_model_path = model_path + '/ent/ent_module_mark.m'
    ent_inner_model_path = model_path + '/ent/ent_inner_C15.m'
    ent_credit_model_path = model_path + '/credit/credit_module_mark.m'
    model_path = model_path + '/credit/enterprise_keep_contract-is_kcont.m'
    model = load_model(model_path)
    ent_model = load_model(ent_model_path)
    ent_inner_model = load_model(ent_inner_model_path)
    ent_credit_model = load_model(ent_credit_model_path)

    newEntList = []
    newEntList_credit_module = []
    newEntList_ent_module = []

    count = 0
    count_credit_module = 0
    count_ent_module = 0

    for row in tqdm(data_matrix.iterrows()):
        entname = row[1]['entname']
        is_kont = row[1]['is_kcont']

        oldEnt = EnterpriseKeepContract.objects.filter(entname__exact=entname)
        oldEnt_credit_module = CreditModule.objects.filter(entname__exact=entname)
        oldEnt_ent_module = EntModule.objects.filter(entname__exact=entname)

        # enterprise_keep_contract

        is_kcont_type = 0

        if len(oldEnt):
            oldEnt[0].is_kcont += is_kont
            is_kcont_type = predict(np.array(oldEnt[0].is_kcont), model)[0]
            oldEnt[0].is_kcont_type = is_kcont_type
            oldEnt[0].save()

        else:
            is_kcont_type = predict(np.array(is_kont), model)[0]
            newEnt = EnterpriseKeepContract(entname=entname, is_kcont=is_kont, is_kcont_type=is_kcont_type)
            newEntList.append(newEnt)
            count += 1

            if count / 5000 == 1:
                EnterpriseKeepContract.objects.bulk_create(newEntList)
                newEntList = []
                count = 0

        # credit_module

        credit_module_type = 0

        if len(oldEnt_credit_module):
            oldEnt_credit_module[0].is_kcont_type = is_kcont_type
            ent_credit_module_mark = get_module_mark(oldEnt_credit_module[0], credit_weight_dict)
            oldEnt_credit_module[0].credit_module = ent_credit_module_mark
            credit_module_type = predict(ent_credit_module_mark, model=ent_credit_model)
            oldEnt_credit_module[0].credit_module_type = credit_module_type

            oldEnt_credit_module[0].save()

        else:
            new_credit_module = CreditModule(entname=entname, is_kcont_type=is_kcont_type,
                                             credit_grade_num_type=0)
            ent_credit_module_mark = get_module_mark(new_credit_module, credit_weight_dict)
            new_credit_module.credit_module = ent_credit_module_mark
            credit_module_type = predict(ent_credit_module_mark, model=ent_credit_model)
            new_credit_module.credit_module_type = credit_module_type
            newEntList_credit_module.append(new_credit_module)

            count_credit_module += 1
            if count_credit_module / 5000 == 1:
                CreditModule.objects.bulk_create(newEntList_credit_module)
                newEntList_credit_module = []
                count_credit_module = 0


        # ent_module
        if len(oldEnt_ent_module):
            oldEnt_ent_module[0].credit_module_type = credit_module_type
            ent_mark = get_module_mark(oldEnt_ent_module[0], ent_weight_dict)
            oldEnt_ent_module[0].ent = ent_mark

            oldEnt_ent_module[0].ent_type = predict(ent_mark, model=ent_model)
            ent_type_list = get_ent_module_type_list(entmodule=oldEnt_ent_module[0], weight_dict=ent_weight_dict)
            oldEnt_ent_module[0].ent_inner_type = inner_predict(ent_type_list, ent_inner_model)

            oldEnt_ent_module[0].save()
        else:
            newEntModule = EntModule(entname=entname, company_baseinfo_module_type=0,
                                     risk_module_type=0, investment_module_type=0, creativity_module_type=0,
                                     brand_module_type=0, recruit_module_type=0,
                                     credit_module_type=credit_module_type)
            ent_mark = get_module_mark(newEntModule, ent_weight_dict)
            newEntModule.ent = ent_mark
            newEntModule.ent_type = predict(ent_mark, model=ent_model)
            ent_type_list = get_ent_module_type_list(entmodule=newEntModule, weight_dict=ent_weight_dict)
            newEntModule.ent_inner_type = inner_predict(ent_type_list, ent_inner_model)

            newEntList_ent_module.append(newEntModule)
            count_ent_module += 1

            if count_ent_module / 5000 == 1:
                EntModule.objects.bulk_create(newEntList_ent_module)
                newEntList_ent_module = []
                count_ent_module = 0

    EnterpriseKeepContract.objects.bulk_create(newEntList)
    CreditModule.objects.bulk_create(newEntList_credit_module)
    EntModule.objects.bulk_create(newEntList_ent_module)




# brand
def jn_special_new_info_predict(file_path,model_path):
    try:
        data_matrix = pd.read_csv(file_path, sep=',')
    except:
        data_matrix = pd.read_csv(file_path, sep=',',encoding='gbk')



    print(data_matrix)

    ent_model_path = model_path + '/ent/ent_module_mark.m'
    ent_inner_model_path = model_path + '/ent/ent_inner_C15.m'
    ent_brand_model_path = model_path + '/brand/brand_module_mark.m'
    model_path = model_path + '/brand/jn_special_new_info-is_jnsn.m'
    model = load_model(model_path)
    ent_model = load_model(ent_model_path)
    ent_inner_model = load_model(ent_inner_model_path)
    ent_brand_model = load_model(ent_brand_model_path)

    newEntList = []
    newEntList_brand_module = []
    newEntList_ent_module = []

    count = 0
    count_brand_module = 0
    count_ent_module = 0

    for row in tqdm(data_matrix.iterrows()):
        entname = row[1]['entname']
        is_jnsn = row[1]['is_jnsn']

        oldEnt = JnSpecialNewInfo.objects.filter(entname__exact=entname)
        oldEnt_brand_module = BrandModule.objects.filter(entname__exact=entname)
        oldEnt_ent_module = EntModule.objects.filter(entname__exact=entname)


        # jn_special_new_info

        is_jnsn_type = 0

        if len(oldEnt):
            oldEnt[0].is_jnsn += is_jnsn
            is_jnsn_type = predict(np.array(oldEnt[0].is_jnsn), model)[0]
            oldEnt[0].is_jnsn_type = is_jnsn_type

            oldEnt[0].save()
        else:
            is_jnsn_type = predict(np.array(is_jnsn), model)[0]
            newEnt = JnSpecialNewInfo(entname=entname, is_jnsn=is_jnsn, is_jnsn_type=is_jnsn_type)
            newEntList.append(newEnt)
            count += 1

            if count / 5000 == 1:
                JnSpecialNewInfo.objects.bulk_create(newEntList)
                newEntList = []
                count = 0

        # barnd_module
        brand_module_type = 0

        if len(oldEnt_brand_module):
            oldEnt_brand_module[0].is_jnsn_type = is_jnsn_type
            ent_brand_module_mark = get_module_mark(oldEnt_brand_module[0], brand_weight_dict)
            oldEnt_brand_module[0].brand_module = ent_brand_module_mark
            brand_module_type = predict(ent_brand_module_mark, model=ent_brand_model)
            oldEnt_brand_module[0].brand_module_type = brand_module_type


            oldEnt_brand_module[0].save()

        else:
            new_brand_module = BrandModule(entname=entname, is_jnsn_type=is_jnsn_type,level_rank_type=0,is_infoa_type=0,is_infob_type=0,passpercent_type=0)
            ent_brand_module_mark = get_module_mark(new_brand_module, brand_weight_dict)
            new_brand_module.brand_module = ent_brand_module_mark
            brand_module_type = predict(ent_brand_module_mark, model=ent_brand_model)
            new_brand_module.brand_module_type = brand_module_type

            newEntList_brand_module.append(new_brand_module)
            count_brand_module += 1

            if count_brand_module / 5000 == 1:
                BrandModule.objects.bulk_create(newEntList_brand_module)
                newEntList_brand_module = []
                count_brand_module = 0

        # ent_module
        if len(oldEnt_ent_module):
            oldEnt_ent_module[0].brand_module_type = brand_module_type
            ent_mark = get_module_mark(oldEnt_ent_module[0], ent_weight_dict)
            oldEnt_ent_module[0].ent = ent_mark

            oldEnt_ent_module[0].ent_type = predict(ent_mark, model=ent_model)
            ent_type_list = get_ent_module_type_list(entmodule=oldEnt_ent_module[0], weight_dict=ent_weight_dict)
            oldEnt_ent_module[0].ent_inner_type = inner_predict(ent_type_list, ent_inner_model)

            oldEnt_ent_module[0].save()
        else:
            newEntModule = EntModule(entname=entname, company_baseinfo_module_type=0,
                                     risk_module_type=0, investment_module_type=0, creativity_module_type=0,
                                     brand_module_type=brand_module_type, recruit_module_type=0,
                                     credit_module_type=0)
            ent_mark = get_module_mark(newEntModule, ent_weight_dict)
            newEntModule.ent = ent_mark
            newEntModule.ent_type = predict(ent_mark, model=ent_model)
            ent_type_list = get_ent_module_type_list(entmodule=newEntModule, weight_dict=ent_weight_dict)
            newEntModule.ent_inner_type = inner_predict(ent_type_list, ent_inner_model)

            newEntList_ent_module.append(newEntModule)
            count_ent_module += 1

            if count_ent_module / 5000 == 1:
                EntModule.objects.bulk_create(newEntList_ent_module)
                newEntList_ent_module = []
                count_ent_module = 0

    JnSpecialNewInfo.objects.bulk_create(newEntList)
    BrandModule.objects.bulk_create(newEntList_brand_module)
    EntModule.objects.bulk_create(newEntList_ent_module)



def jn_tech_center_predict(file_path,model_path):
    try:
        data_matrix = pd.read_csv(file_path, sep=',')
    except:
        data_matrix = pd.read_csv(file_path, sep=',',encoding='gbk')

    d = {"市级": 1, "省级": 2}
    data_matrix['level_rank'] = data_matrix['level_rank'].map(d)

    ent_model_path = model_path + '/ent/ent_module_mark.m'
    ent_inner_model_path = model_path + '/ent/ent_inner_C15.m'
    ent_brand_model_path = model_path + '/brand/brand_module_mark.m'
    model_path = model_path + '/brand/jn_tech_center-level_rank.m'
    model = load_model(model_path)
    ent_model = load_model(ent_model_path)
    ent_inner_model = load_model(ent_inner_model_path)
    ent_brand_model = load_model(ent_brand_model_path)

    newEntList = []
    newEntList_brand_module = []
    newEntList_ent_module = []

    count = 0
    count_brand_module = 0
    count_ent_module = 0

    for row in tqdm(data_matrix.iterrows()):
        entname = row[1]['entname']
        level_rank = row[1]['level_rank']

        oldEnt = JnTechCenter.objects.filter(entname__exact=entname)
        oldEnt_brand_module = BrandModule.objects.filter(entname__exact=entname)
        oldEnt_ent_module = EntModule.objects.filter(entname__exact=entname)

        if len(oldEnt):
            oldEnt[0].level_rank = level_rank
            level_rank_type = predict(np.array(oldEnt[0].level_rank), model)[0]
            oldEnt[0].level_rank_type = level_rank_type
            oldEnt[0].save()

        else:
            level_rank_type = predict(np.array(level_rank), model)[0]
            newEnt = JnTechCenter(entname=entname, level_rank=level_rank, level_rank_type=level_rank_type)
            newEntList.append(newEnt)
            count += 1

            if count / 5000 == 1:
                JnTechCenter.objects.bulk_create(newEntList)
                newEntList = []
                count = 0

        # barnd_module
        brand_module_type = 0

        if len(oldEnt_brand_module):
            oldEnt_brand_module[0].level_rank_type = level_rank_type
            ent_brand_module_mark = get_module_mark(oldEnt_brand_module[0], brand_weight_dict)
            oldEnt_brand_module[0].brand_module = ent_brand_module_mark
            brand_module_type = predict(ent_brand_module_mark, model=ent_brand_model)
            oldEnt_brand_module[0].brand_module_type = brand_module_type


            oldEnt_brand_module[0].save()

        else:
            new_brand_module = BrandModule(entname=entname, is_jnsn_type=0, level_rank_type=level_rank_type,
                                           is_infoa_type=0, is_infob_type=0, passpercent_type=0)
            ent_brand_module_mark = get_module_mark(new_brand_module, brand_weight_dict)
            new_brand_module.brand_module = ent_brand_module_mark
            brand_module_type = predict(ent_brand_module_mark, model=ent_brand_model)
            new_brand_module.brand_module_type = brand_module_type

            newEntList_brand_module.append(new_brand_module)
            count_brand_module += 1

            if count_brand_module / 5000 == 1:
                BrandModule.objects.bulk_create(newEntList_brand_module)
                newEntList_brand_module = []
                count_brand_module = 0

        # ent_module
        if len(oldEnt_ent_module):
            oldEnt_ent_module[0].brand_module_type = brand_module_type
            ent_mark = get_module_mark(oldEnt_ent_module[0], ent_weight_dict)
            oldEnt_ent_module[0].ent = ent_mark

            oldEnt_ent_module[0].ent_type = predict(ent_mark, model=ent_model)
            ent_type_list = get_ent_module_type_list(entmodule=oldEnt_ent_module[0], weight_dict=ent_weight_dict)
            oldEnt_ent_module[0].ent_inner_type = inner_predict(ent_type_list, ent_inner_model)

            oldEnt_ent_module[0].save()
        else:
            newEntModule = EntModule(entname=entname, company_baseinfo_module_type=0,
                                     risk_module_type=0, investment_module_type=0, creativity_module_type=0,
                                     brand_module_type=brand_module_type, recruit_module_type=0,
                                     credit_module_type=0)
            ent_mark = get_module_mark(newEntModule, ent_weight_dict)
            newEntModule.ent = ent_mark
            newEntModule.ent_type = predict(ent_mark, model=ent_model)
            ent_type_list = get_ent_module_type_list(entmodule=newEntModule, weight_dict=ent_weight_dict)
            newEntModule.ent_inner_type = inner_predict(ent_type_list, ent_inner_model)

            newEntList_ent_module.append(newEntModule)
            count_ent_module += 1

            if count_ent_module / 5000 == 1:
                EntModule.objects.bulk_create(newEntList_ent_module)
                newEntList_ent_module = []
                count_ent_module = 0

    JnTechCenter.objects.bulk_create(newEntList)
    BrandModule.objects.bulk_create(newEntList_brand_module)
    EntModule.objects.bulk_create(newEntList_ent_module)


def trademark_info_predict(file_path,model_path):
    data_matrix = pd.read_csv(file_path, sep=',')

    file_postfix = file_path.split('/')[-1].split('.')[0][-1:]
    is_info_key = 'is_info' + file_postfix

    ent_model_path = model_path + '/ent/ent_module_mark.m'
    ent_inner_model_path = model_path + '/ent/ent_inner_C15.m'
    ent_brand_model_path = model_path + '/brand/brand_module_mark.m'
    ent_model = load_model(ent_model_path)
    ent_inner_model = load_model(ent_inner_model_path)
    ent_brand_model = load_model(ent_brand_model_path)

    if file_postfix == 'a':
        model_path = model_path + '/brand/trademark_infoa-is_infoa.m'
        model = load_model(model_path)
    else:
        model_path = model_path + '/brand/trademark_infob-is_infob.m'
        model = load_model(model_path)

    newEntList = []
    newEntList_brand_module = []
    newEntList_ent_module = []

    count = 0
    count_brand_module = 0
    count_ent_module = 0

    for row in tqdm(data_matrix.iterrows()):
        entname = row[1]['entname']
        is_info = row[1][is_info_key]


        oldEnt_brand_module = BrandModule.objects.filter(entname__exact=entname)
        oldEnt_ent_module = EntModule.objects.filter(entname__exact=entname)

        if file_postfix == 'a':
            oldEnt = TrademarkInfoa.objects.filter(entname__exact=entname)

            is_infoa_type = 0

            if len(oldEnt):
                oldEnt[0].is_infoa += is_info
                is_infoa_type = predict(np.array(oldEnt[0].is_infoa), model)[0]
                oldEnt[0].is_infoa_type = is_infoa_type

                oldEnt[0].save()

            else:
                is_infoa_type = predict(np.array(is_info), model)[0]
                newEnt = TrademarkInfoa(entname=entname, is_infoa=is_info, is_infoa_type=is_infoa_type)
                newEntList.append(newEnt)
                count += 1

                if count / 5000 == 1:
                    TrademarkInfoa.objects.bulk_create(newEntList)
                    newEntList = []
                    count = 0

        elif file_postfix == 'b':
            oldEnt = TrademarkInfob.objects.filter(entname__exact=entname)

            is_infob_type = 0

            if len(oldEnt):
                oldEnt[0].is_infob += is_info
                is_infob_type = predict(np.array(oldEnt[0].is_infob), model)[0]
                oldEnt[0].is_infob_type = is_infob_type

                oldEnt[0].save()

            else:
                is_infob_type = predict(np.array(is_info), model)[0]
                newEnt = TrademarkInfob(entname=entname, is_infob=is_info, is_infob_type=is_infob_type)
                newEntList.append(newEnt)
                count += 1

                if count / 5000 == 1:
                    TrademarkInfob.objects.bulk_create(newEntList)
                    newEntList = []
                    count = 0
        # barnd_module
        brand_module_type = 0

        if len(oldEnt_brand_module):

            if file_postfix == 'a':
                oldEnt_brand_module[0].is_infoa_type = is_infoa_type

            elif file_postfix == 'b':
                oldEnt_brand_module[0].is_infob_type = is_infob_type

            ent_brand_module_mark = get_module_mark(oldEnt_brand_module[0], brand_weight_dict)
            oldEnt_brand_module[0].brand_module = ent_brand_module_mark
            brand_module_type = predict(ent_brand_module_mark, model=ent_brand_model)
            oldEnt_brand_module[0].brand_module_type = brand_module_type

            oldEnt_brand_module[0].save()

        else:

            if file_postfix == 'a':
                new_brand_module = BrandModule(entname=entname, is_jnsn_type=0, level_rank_type=0,
                                               is_infoa_type=is_infoa_type, is_infob_type=0, passpercent_type=0)

            elif file_postfix == 'b':
                new_brand_module = BrandModule(entname=entname, is_jnsn_type=0, level_rank_type=0,
                                               is_infoa_type=is_infob_type, is_infob_type=0, passpercent_type=0)

            ent_brand_module_mark = get_module_mark(new_brand_module, brand_weight_dict)
            new_brand_module.brand_module = ent_brand_module_mark
            brand_module_type = predict(ent_brand_module_mark, model=ent_brand_model)
            new_brand_module.brand_module_type = brand_module_type

            newEntList_brand_module.append(new_brand_module)
            count_brand_module += 1

            if count_brand_module / 5000 == 1:
                BrandModule.objects.bulk_create(newEntList_brand_module)
                newEntList_brand_module = []
                count_brand_module = 0
        # ent_module
        if len(oldEnt_ent_module):
            oldEnt_ent_module[0].brand_module_type = brand_module_type
            ent_mark = get_module_mark(oldEnt_ent_module[0], ent_weight_dict)
            oldEnt_ent_module[0].ent = ent_mark

            oldEnt_ent_module[0].ent_type = predict(ent_mark, model=ent_model)
            ent_type_list = get_ent_module_type_list(entmodule=oldEnt_ent_module[0], weight_dict=ent_weight_dict)
            oldEnt_ent_module[0].ent_inner_type = inner_predict(ent_type_list, ent_inner_model)

            oldEnt_ent_module[0].save()
        else:
            newEntModule = EntModule(entname=entname, company_baseinfo_module_type=0,
                                     risk_module_type=0, investment_module_type=0, creativity_module_type=0,
                                     brand_module_type=brand_module_type, recruit_module_type=0,
                                     credit_module_type=0)
            ent_mark = get_module_mark(newEntModule, ent_weight_dict)
            newEntModule.ent = ent_mark
            newEntModule.ent_type = predict(ent_mark, model=ent_model)
            ent_type_list = get_ent_module_type_list(entmodule=newEntModule, weight_dict=ent_weight_dict)
            newEntModule.ent_inner_type = inner_predict(ent_type_list, ent_inner_model)

            newEntList_ent_module.append(newEntModule)
            count_ent_module += 1

            if count_ent_module / 5000 == 1:
                EntModule.objects.bulk_create(newEntList_ent_module)
                newEntList_ent_module = []
                count_ent_module = 0

    if file_postfix == 'a':
        TrademarkInfoa.objects.bulk_create(newEntList)
    elif file_postfix == 'b':
        TrademarkInfob.objects.bulk_create(newEntList)

    BrandModule.objects.bulk_create(newEntList_brand_module)
    EntModule.objects.bulk_create(newEntList_ent_module)


def product_checkinfo_connect_predict(file_path,model_path):
    data_matrix = pd.read_csv(file_path, sep=',')

    ent_model_path = model_path + '/ent/ent_module_mark.m'
    ent_inner_model_path = model_path + '/ent/ent_inner_C15.m'
    ent_brand_model_path = model_path + '/brand/brand_module_mark.m'
    model_path = model_path + '/brand/product_checkinfo_connect-passpercent.m'
    model = load_model(model_path)
    ent_model = load_model(ent_model_path)
    ent_inner_model = load_model(ent_inner_model_path)
    ent_brand_model = load_model(ent_brand_model_path)

    newEntList = []
    newEntList_brand_module = []
    newEntList_ent_module = []

    count = 0
    count_brand_module = 0
    count_ent_module = 0

    for row in tqdm(data_matrix.iterrows()):
        entname = row[1]['entname']
        passpercent = row[1]['passpercent']

        oldEnt = ProductCheckinfoConnect.objects.filter(entname__exact=entname)
        oldEnt_brand_module = BrandModule.objects.filter(entname__exact=entname)
        oldEnt_ent_module = EntModule.objects.filter(entname__exact=entname)

        # product_checkinfo_connect

        passpercent_type = 0
        if len(oldEnt):
            oldEnt[0].passpercent = passpercent
            passpercent_type = predict(np.array(oldEnt[0].passpercent), model)[0]
            oldEnt[0].passpercent_type = passpercent_type
            oldEnt[0].save()

        else:
            passpercent_type = predict(np.array(passpercent), model)[0]
            newEnt = ProductCheckinfoConnect(entname=entname, passpercent=passpercent, passpercent_type=passpercent_type)
            newEntList.append(newEnt)
            count += 1

            if count / 5000 == 1:
                ProductCheckinfoConnect.objects.bulk_create(newEntList)
                newEntList = []
                count = 0

        # barnd_module
        brand_module_type = 0

        if len(oldEnt_brand_module):
            oldEnt_brand_module[0].passpercent_type = passpercent_type
            ent_brand_module_mark = get_module_mark(oldEnt_brand_module[0], brand_weight_dict)
            oldEnt_brand_module[0].brand_module = ent_brand_module_mark
            brand_module_type = predict(ent_brand_module_mark, model=ent_brand_model)
            oldEnt_brand_module[0].brand_module_type = brand_module_type


            oldEnt_brand_module[0].save()

        else:
            new_brand_module = BrandModule(entname=entname, is_jnsn_type=0, level_rank_type=0,
                                           is_infoa_type=0, is_infob_type=0, passpercent_type=passpercent_type)
            ent_brand_module_mark = get_module_mark(new_brand_module, brand_weight_dict)
            new_brand_module.brand_module = ent_brand_module_mark
            brand_module_type = predict(ent_brand_module_mark, model=ent_brand_model)
            new_brand_module.brand_module_type = brand_module_type

            newEntList_brand_module.append(new_brand_module)
            count_brand_module += 1

            if count_brand_module / 5000 == 1:
                BrandModule.objects.bulk_create(newEntList_brand_module)
                newEntList_brand_module = []
                count_brand_module = 0

        # ent_module
        if len(oldEnt_ent_module):
            oldEnt_ent_module[0].brand_module_type = brand_module_type
            ent_mark = get_module_mark(oldEnt_ent_module[0], ent_weight_dict)
            oldEnt_ent_module[0].ent = ent_mark

            oldEnt_ent_module[0].ent_type = predict(ent_mark, model=ent_model)
            ent_type_list = get_ent_module_type_list(entmodule=oldEnt_ent_module[0], weight_dict=ent_weight_dict)
            oldEnt_ent_module[0].ent_inner_type = inner_predict(ent_type_list, ent_inner_model)

            oldEnt_ent_module[0].save()
        else:
            newEntModule = EntModule(entname=entname, company_baseinfo_module_type=0,
                                     risk_module_type=0, investment_module_type=0, creativity_module_type=0,
                                     brand_module_type=brand_module_type, recruit_module_type=0,
                                     credit_module_type=0)
            ent_mark = get_module_mark(newEntModule, ent_weight_dict)
            newEntModule.ent = ent_mark
            newEntModule.ent_type = predict(ent_mark, model=ent_model)
            ent_type_list = get_ent_module_type_list(entmodule=newEntModule, weight_dict=ent_weight_dict)
            newEntModule.ent_inner_type = inner_predict(ent_type_list, ent_inner_model)

            newEntList_ent_module.append(newEntModule)
            count_ent_module += 1

            if count_ent_module / 5000 == 1:
                EntModule.objects.bulk_create(newEntList_ent_module)
                newEntList_ent_module = []
                count_ent_module = 0

    ProductCheckinfoConnect.objects.bulk_create(newEntList)
    BrandModule.objects.bulk_create(newEntList_brand_module)
    EntModule.objects.bulk_create(newEntList_ent_module)

# creativity





def intangible_brand_predict( file_path,model_path):
    try:
        data_matrix = pd.read_csv(file_path, sep=',')
    except:
        data_matrix = pd.read_csv(file_path, sep=',',encoding='gbk')
    data_matrix.fillna(0, inplace=True)

    ent_model_path = model_path + '/ent/ent_module_mark.m'
    ent_inner_model_path = model_path + '/ent/ent_inner_C15.m'
    ent_creativity_model_path = model_path + '/creativity/creativity_module_mark.m'
    model_path = model_path + '/creativity/intangible_brand-ibrand_num.m'
    model = load_model(model_path)
    ent_model = load_model(ent_model_path)
    ent_inner_model = load_model(ent_inner_model_path)
    ent_creativity_model = load_model(ent_creativity_model_path)

    newEntList = []
    newEntList_creativity_module = []
    newEntList_ent_module = []

    count = 0
    count_creativity_module = 0
    count_ent_module = 0

    for row in tqdm(data_matrix.iterrows()):
        print(row)
        entname = row[1]['entname']
        ibrand_num = row[1]['ibrand_num']

        oldEnt = IntangibleBrand.objects.filter(entname__exact=entname)
        oldEnt_creativity_module = CreativityModule.objects.filter(entname__exact=entname)
        oldEnt_ent_module = EntModule.objects.filter(entname__exact=entname)

        ibrand_num_type = 0

        if len(oldEnt):
            oldEnt[0].ibrand_num += ibrand_num
            ibrand_num_type = predict(np.array(oldEnt[0].ibrand_num), model)[0]
            oldEnt[0].ibrand_num_type = ibrand_num_type
            oldEnt[0].save()

        else:
            ibrand_num_type = predict(np.array(ibrand_num), model)[0]
            newEnt = IntangibleBrand(entname=entname, ibrand_num=ibrand_num, ibrand_num_type=ibrand_num_type)
            newEntList.append(newEnt)
            count += 1

            if count / 5000 == 1:
                JnSpecialNewInfo.objects.bulk_create(newEntList)
                newEntList = []
                count = 0

        # barnd_module
        creativity_module_type = 0

        if len(oldEnt_creativity_module):
            oldEnt_creativity_module[0].ibrand_num_type = ibrand_num_type
            ent_creativity_module_mark = get_module_mark(oldEnt_creativity_module[0], creativity_weight_dict)
            oldEnt_creativity_module[0].creativity_module = ent_creativity_module_mark
            creativity_module_type = predict(ent_creativity_module_mark, model=ent_creativity_model)
            oldEnt_creativity_module[0].creativity_module_type = creativity_module_type


            oldEnt_creativity_module[0].save()

        else:
            new_creativity_module = CreativityModule(entname=entname, ibrand_num_type=ibrand_num_type, icopy_num_type=0, ipat_num_type=0,
                                                     idom_num_type=0)
            ent_creativity_module_mark = get_module_mark(new_creativity_module, creativity_weight_dict)
            new_creativity_module.creativity_module = ent_creativity_module_mark
            creativity_module_type = predict(ent_creativity_module_mark, model=ent_creativity_model)
            new_creativity_module.creativity_module_type = creativity_module_type

            newEntList_creativity_module.append(new_creativity_module)
            count_creativity_module += 1

            if count_creativity_module / 5000 == 1:
                CreativityModule.objects.bulk_create(newEntList_creativity_module)
                newEntList_creativity_module = []
                count_creativity_module = 0

        # ent_module
        if len(oldEnt_ent_module):
            oldEnt_ent_module[0].creativity_module_type = creativity_module_type
            ent_mark = get_module_mark(oldEnt_ent_module[0], ent_weight_dict)
            oldEnt_ent_module[0].ent = ent_mark

            oldEnt_ent_module[0].ent_type = predict(ent_mark, model=ent_model)
            ent_type_list = get_ent_module_type_list(entmodule=oldEnt_ent_module[0], weight_dict=ent_weight_dict)
            oldEnt_ent_module[0].ent_inner_type = inner_predict(ent_type_list, ent_inner_model)

            oldEnt_ent_module[0].save()
        else:
            newEntModule = EntModule(entname=entname, company_baseinfo_module_type=0,
                                     risk_module_type=0, investment_module_type=0, creativity_module_type=creativity_module_type,
                                     brand_module_type=0, recruit_module_type=0,
                                     credit_module_type=0)
            ent_mark = get_module_mark(newEntModule, ent_weight_dict)
            newEntModule.ent = ent_mark
            newEntModule.ent_type = predict(ent_mark, model=ent_model)
            ent_type_list = get_ent_module_type_list(entmodule=newEntModule, weight_dict=ent_weight_dict)
            newEntModule.ent_inner_type = inner_predict(ent_type_list, ent_inner_model)

            newEntList_ent_module.append(newEntModule)
            count_ent_module += 1

            if count_ent_module / 5000 == 1:
                EntModule.objects.bulk_create(newEntList_ent_module)
                newEntList_ent_module = []
                count_ent_module = 0

    IntangibleBrand.objects.bulk_create(newEntList)
    CreativityModule.objects.bulk_create(newEntList_creativity_module)
    EntModule.objects.bulk_create(newEntList_ent_module)

# 处理

def intangible_copyright_predict(file_path,model_path):
    data_matrix = pd.read_csv(file_path, sep=',')

    ent_model_path = model_path + '/ent/ent_module_mark.m'
    ent_inner_model_path = model_path + '/ent/ent_inner_C15.m'
    ent_creativity_model_path = model_path + '/creativity/creativity_module_mark.m'
    model_path = model_path + '/creativity/intangible_copyright-icopy_num.m'
    model = load_model(model_path)
    ent_model = load_model(ent_model_path)
    ent_inner_model = load_model(ent_inner_model_path)
    ent_creativity_model = load_model(ent_creativity_model_path)

    newEntList = []
    newEntList_creativity_module = []
    newEntList_ent_module = []

    count = 0
    count_creativity_module = 0
    count_ent_module = 0

    for row in tqdm(data_matrix.iterrows()):
        entname = row[1]['entname']
        icpoy_num = row[1]['icopy_num']

        oldEnt = IntangibleCopyright.objects.filter(entname__exact=entname)
        oldEnt_creativity_module = CreativityModule.objects.filter(entname__exact=entname)
        oldEnt_ent_module = EntModule.objects.filter(entname__exact=entname)

        icopy_num_type = 0

        if len(oldEnt):
            oldEnt[0].icopy_num += icpoy_num
            icopy_num_type = predict(np.array(oldEnt[0].icopy_num), model)[0]
            oldEnt[0].icopy_num_type = icopy_num_type
            oldEnt[0].save()

        else:
            icpoy_num_type = predict(np.array(icpoy_num), model)[0]
            newEnt = IntangibleCopyright(entname=entname, icopy_num=icpoy_num, icopy_num_type=icpoy_num_type)
            newEntList.append(newEnt)
            count += 1

            if count / 5000 == 1:
                IntangibleCopyright.objects.bulk_create(newEntList)
                newEntList = []
                count = 0

        # barnd_module
        creativity_module_type = 0

        if len(oldEnt_creativity_module):
            oldEnt_creativity_module[0].icopy_num_type = icopy_num_type
            ent_creativity_module_mark = get_module_mark(oldEnt_creativity_module[0],creativity_weight_dict)
            oldEnt_creativity_module[0].creativity_module = ent_creativity_module_mark
            creativity_module_type = predict(ent_creativity_module_mark, model=ent_creativity_model)
            oldEnt_creativity_module[0].creativity_module_type = creativity_module_type

            oldEnt_creativity_module[0].save()

        else:
            new_creativity_module = CreativityModule(entname=entname, ibrand_num_type=0,
                                                     icopy_num_type=icopy_num_type, ipat_num_type=0,
                                                     idom_num_type=0)
            ent_creativity_module_mark = get_module_mark(new_creativity_module,creativity_weight_dict)
            new_creativity_module.creativity_module = ent_creativity_module_mark
            creativity_module_type = predict(ent_creativity_module_mark, model=ent_creativity_model)
            new_creativity_module.creativity_module_type = creativity_module_type

            newEntList_creativity_module.append(new_creativity_module)
            count_creativity_module += 1

            if count_creativity_module / 5000 == 1:
                CreativityModule.objects.bulk_create(newEntList_creativity_module)
                newEntList_creativity_module = []
                count_creativity_module = 0

        # ent_module
        if len(oldEnt_ent_module):
            oldEnt_ent_module[0].creativity_module_type = creativity_module_type
            ent_mark = get_module_mark(oldEnt_ent_module[0], ent_weight_dict)
            oldEnt_ent_module[0].ent = ent_mark

            oldEnt_ent_module[0].ent_type = predict(ent_mark, model=ent_model)
            ent_type_list = get_ent_module_type_list(entmodule=oldEnt_ent_module[0], weight_dict=ent_weight_dict)
            oldEnt_ent_module[0].ent_inner_type = inner_predict(ent_type_list, ent_inner_model)

            oldEnt_ent_module[0].save()
        else:
            newEntModule = EntModule(entname=entname, company_baseinfo_module_type=0,
                                     risk_module_type=0, investment_module_type=0,
                                     creativity_module_type=creativity_module_type,
                                     brand_module_type=0, recruit_module_type=0,
                                     credit_module_type=0)
            ent_mark = get_module_mark(newEntModule, ent_weight_dict)
            newEntModule.ent = ent_mark
            newEntModule.ent_type = predict(ent_mark, model=ent_model)
            ent_type_list = get_ent_module_type_list(entmodule=newEntModule, weight_dict=ent_weight_dict)
            newEntModule.ent_inner_type = inner_predict(ent_type_list, ent_inner_model)

            newEntList_ent_module.append(newEntModule)
            count_ent_module += 1

            if count_ent_module / 5000 == 1:
                EntModule.objects.bulk_create(newEntList_ent_module)
                newEntList_ent_module = []
                count_ent_module = 0

    IntangibleCopyright.objects.bulk_create(newEntList)
    CreativityModule.objects.bulk_create(newEntList_creativity_module)
    EntModule.objects.bulk_create(newEntList_ent_module)


def intangible_patent_predict( file_path,model_path):
    data_matrix = pd.read_csv(file_path, sep=',')

    ent_model_path = model_path + '/ent/ent_module_mark.m'
    ent_inner_model_path = model_path + '/ent/ent_inner_C15.m'
    ent_creativity_model_path = model_path + '/creativity/creativity_module_mark.m'
    model_path = model_path + '/creativity/intangible_patent-ipat_num.m'
    model = load_model(model_path)
    ent_model = load_model(ent_model_path)
    ent_inner_model = load_model(ent_inner_model_path)
    ent_creativity_model = load_model(ent_creativity_model_path)

    newEntList = []
    newEntList_creativity_module = []
    newEntList_ent_module = []

    count = 0
    count_creativity_module = 0
    count_ent_module = 0

    for row in tqdm(data_matrix.iterrows()):
        entname = row[1]['entname']
        ipat_num = row[1]['ipat_num']

        oldEnt = IntangiblePatent.objects.filter(entname__exact=entname)
        oldEnt_creativity_module = CreativityModule.objects.filter(entname__exact=entname)
        oldEnt_ent_module = EntModule.objects.filter(entname__exact=entname)

        ipat_num_type = 0

        if len(oldEnt):
            oldEnt[0].ipat_num += ipat_num
            ipat_num_type = predict(np.array(oldEnt[0].ipat_num), model)[0]
            oldEnt[0].ipat_num_type = ipat_num_type
            oldEnt[0].save()

        else:
            ipat_num_type = predict(np.array(ipat_num), model)[0]
            newEnt = IntangiblePatent(entname=entname, ipat_num=ipat_num, ipat_num_type=ipat_num_type)
            newEntList.append(newEnt)
            count += 1

            if count / 5000 == 1:
                IntangiblePatent.objects.bulk_create(newEntList)
                newEntList = []
                count = 0

        # barnd_module
        creativity_module_type = 0

        if len(oldEnt_creativity_module):
            oldEnt_creativity_module[0].ipat_num_type = ipat_num_type
            ent_creativity_module_mark = get_module_mark(oldEnt_creativity_module[0],creativity_weight_dict)
            oldEnt_creativity_module[0].creativity_module = ent_creativity_module_mark
            creativity_module_type = predict(ent_creativity_module_mark, model=ent_creativity_model)
            oldEnt_creativity_module[0].creativity_module_type = creativity_module_type


            oldEnt_creativity_module[0].save()

        else:
            new_creativity_module = CreativityModule(entname=entname, ibrand_num_type=0,
                                                     icopy_num_type=0, ipat_num_type=ipat_num_type,
                                                     idom_num_type=0)
            ent_creativity_module_mark = get_module_mark(new_creativity_module,creativity_weight_dict)
            new_creativity_module.creativity_module = ent_creativity_module_mark
            creativity_module_type = predict(ent_creativity_module_mark, model=ent_creativity_model)
            new_creativity_module.creativity_module_type = creativity_module_type

            newEntList_creativity_module.append(new_creativity_module)
            count_creativity_module += 1

            if count_creativity_module / 5000 == 1:
                CreativityModule.objects.bulk_create(newEntList_creativity_module)
                newEntList_creativity_module = []
                count_creativity_module = 0

        # ent_module
        if len(oldEnt_ent_module):
            oldEnt_ent_module[0].creativity_module_type = creativity_module_type
            ent_mark = get_module_mark(oldEnt_ent_module[0], ent_weight_dict)
            oldEnt_ent_module[0].ent = ent_mark

            oldEnt_ent_module[0].ent_type = predict(ent_mark, model=ent_model)
            ent_type_list = get_ent_module_type_list(entmodule=oldEnt_ent_module[0], weight_dict=ent_weight_dict)
            oldEnt_ent_module[0].ent_inner_type = inner_predict(ent_type_list, ent_inner_model)

            oldEnt_ent_module[0].save()
        else:
            newEntModule = EntModule(entname=entname, company_baseinfo_module_type=0,
                                     risk_module_type=0, investment_module_type=0,
                                     creativity_module_type=creativity_module_type,
                                     brand_module_type=0, recruit_module_type=0,
                                     credit_module_type=0)
            ent_mark = get_module_mark(newEntModule, ent_weight_dict)
            newEntModule.ent = ent_mark
            newEntModule.ent_type = predict(ent_mark, model=ent_model)
            ent_type_list = get_ent_module_type_list(entmodule=newEntModule, weight_dict=ent_weight_dict)
            newEntModule.ent_inner_type = inner_predict(ent_type_list, ent_inner_model)

            newEntList_ent_module.append(newEntModule)
            count_ent_module += 1

            if count_ent_module / 5000 == 1:
                EntModule.objects.bulk_create(newEntList_ent_module)
                newEntList_ent_module = []
                count_ent_module = 0

    IntangiblePatent.objects.bulk_create(newEntList)
    CreativityModule.objects.bulk_create(newEntList_creativity_module)
    EntModule.objects.bulk_create(newEntList_ent_module)


def web_record_info_predict( file_path,model_path):
    data_matrix = pd.read_csv(file_path, sep=',')

    ent_model_path = model_path + '/ent/ent_module_mark.m'
    ent_inner_model_path = model_path + '/ent/ent_inner_C15.m'
    ent_creativity_model_path = model_path + '/creativity/creativity_module_mark.m'
    model_path = model_path + '/creativity/web_record_info-idom_num.m'
    model = load_model(model_path)
    ent_model = load_model(ent_model_path)
    ent_inner_model = load_model(ent_inner_model_path)
    ent_creativity_model = load_model(ent_creativity_model_path)

    newEntList = []
    newEntList_creativity_module = []
    newEntList_ent_module = []

    count = 0
    count_creativity_module = 0
    count_ent_module = 0

    for row in tqdm(data_matrix.iterrows()):
        entname = row[1]['entname']
        idom_num = row[1]['idom_num']

        oldEnt = WebRecordInfo.objects.filter(entname__exact=entname)
        oldEnt_creativity_module = CreativityModule.objects.filter(entname__exact=entname)
        oldEnt_ent_module = EntModule.objects.filter(entname__exact=entname)

        idom_num_type = 0

        if len(oldEnt):
            oldEnt[0].idom_num += idom_num
            idom_num_type = predict(np.array(oldEnt[0].idom_num), model)[0]
            oldEnt[0].idom_num_type = idom_num_type
            oldEnt[0].save()

        else:
            idom_num_type = predict(np.array(idom_num), model)[0]
            newEnt = WebRecordInfo(entname=entname, idom_num=idom_num, idom_num_type=idom_num_type)
            newEntList.append(newEnt)
            count += 1

            if count / 5000 == 1:
                WebRecordInfo.objects.bulk_create(newEntList)
                newEntList = []
                count = 0

        # creativity_module
        creativity_module_type = 0

        if len(oldEnt_creativity_module):
            oldEnt_creativity_module[0].idom_num_type = idom_num_type
            ent_creativity_module_mark = get_module_mark(oldEnt_creativity_module[0],creativity_weight_dict)
            oldEnt_creativity_module[0].creativity_module = ent_creativity_module_mark
            creativity_module_type = predict(ent_creativity_module_mark, model=ent_creativity_model)
            oldEnt_creativity_module[0].creativity_module_type = creativity_module_type


            oldEnt_creativity_module[0].save()

        else:
            new_creativity_module = CreativityModule(entname=entname, ibrand_num_type=0,
                                                     icopy_num_type=0, ipat_num_type=0,
                                                     idom_num_type=idom_num_type)
            ent_creativity_module_mark = get_module_mark(new_creativity_module,creativity_weight_dict)
            new_creativity_module.creativity_module = ent_creativity_module_mark
            creativity_module_type = predict(ent_creativity_module_mark, model=ent_creativity_model)
            new_creativity_module.creativity_module_type = creativity_module_type

            newEntList_creativity_module.append(new_creativity_module)
            count_creativity_module += 1

            if count_creativity_module / 5000 == 1:
                CreativityModule.objects.bulk_create(newEntList_creativity_module)
                newEntList_creativity_module = []
                count_creativity_module = 0

        # ent_module
        if len(oldEnt_ent_module):
            oldEnt_ent_module[0].creativity_module_type = creativity_module_type
            ent_mark = get_module_mark(oldEnt_ent_module[0], ent_weight_dict)
            oldEnt_ent_module[0].ent = ent_mark

            oldEnt_ent_module[0].ent_type = predict(ent_mark, model=ent_model)
            ent_type_list = get_ent_module_type_list(entmodule=oldEnt_ent_module[0], weight_dict=ent_weight_dict)
            oldEnt_ent_module[0].ent_inner_type = inner_predict(ent_type_list, ent_inner_model)

            oldEnt_ent_module[0].save()
        else:
            newEntModule = EntModule(entname=entname, company_baseinfo_module_type=0,
                                     risk_module_type=0, investment_module_type=0,
                                     creativity_module_type=creativity_module_type,
                                     brand_module_type=0, recruit_module_type=0,
                                     credit_module_type=0)
            ent_mark = get_module_mark(newEntModule, ent_weight_dict)
            newEntModule.ent = ent_mark
            newEntModule.ent_type = predict(ent_mark, model=ent_model)
            ent_type_list = get_ent_module_type_list(entmodule=newEntModule, weight_dict=ent_weight_dict)
            newEntModule.ent_inner_type = inner_predict(ent_type_list, ent_inner_model)

            newEntList_ent_module.append(newEntModule)
            count_ent_module += 1

            if count_ent_module / 5000 == 1:
                EntModule.objects.bulk_create(newEntList_ent_module)
                newEntList_ent_module = []
                count_ent_module = 0

    WebRecordInfo.objects.bulk_create(newEntList)
    CreativityModule.objects.bulk_create(newEntList_creativity_module)
    EntModule.objects.bulk_create(newEntList_ent_module)

# weight_dict = {
#     'risk_module_type': -1.11,  # 保留两位小数点，是为了避免出现加减后0分的情况，与空数据混淆
#     'investment_module_type': 1,
#     'creativity_module_type': 1,
#     'brand_module_type': 1,
#     'recruit_module_type': 1,
#     'credit_module_type': 1,
#     'company_baseinfo_module_type': 1
# }

#
# def get_module_mark(module,weigh_dict):
#     sum = 0
#     for key, value in weigh_dict.items():
#         attr = getattr(module,key)
#         if attr == None:
#             attr = 0
#         sum += attr * value
#     return sum

#
# def get_module_mark(entmodule,weight_dict):
#     return entmodule.risk_module_type * weight_dict['risk_module_type'] + entmodule.investment_module_type * weight_dict['investment_module_type'] \
#            + entmodule.creativity_module_type * weight_dict['creativity_module_type'] + entmodule.brand_module_type * weight_dict['brand_module_type'] \
#            + entmodule.recruit_module_type * weight_dict['recruit_module_type'] + entmodule.credit_module_type * weight_dict['credit_module_type'] \
#            + entmodule.company_baseinfo_module_type * weight_dict['company_baseinfo_module_type']

def get_ent_module_type_list(entmodule,weight_dict):
    type_list = []

    if entmodule.risk_module_type == None:
        entmodule.risk_module_type = 0

    if entmodule.investment_module_type == None:
        entmodule.investment_module_type = 0

    if entmodule.creativity_module_type == None:
        entmodule.creativity_module_type = 0

    if entmodule.brand_module_type == None:
        entmodule.brand_module_type = 0

    if entmodule.recruit_module_type == None:
        entmodule.recruit_module_type = 0

    if entmodule.credit_module_type == None:
        entmodule.credit_module_type = 0

    if entmodule.company_baseinfo_module_type == None:
        entmodule.company_baseinfo_module_type = 0


    type_list.append(entmodule.risk_module_type * weight_dict['risk_module_type'])
    type_list.append(entmodule.investment_module_type * weight_dict['investment_module_type'])
    type_list.append(entmodule.creativity_module_type * weight_dict['creativity_module_type'])
    type_list.append(entmodule.brand_module_type * weight_dict['brand_module_type'])
    type_list.append(entmodule.recruit_module_type * weight_dict['recruit_module_type'])
    type_list.append(entmodule.credit_module_type * weight_dict['credit_module_type'])
    type_list.append(entmodule.company_baseinfo_module_type * weight_dict['company_baseinfo_module_type'])
    final_list = []
    final_list.append(type_list)

    return np.array(final_list)




# baseinfo
def company_baseinfo_predict(file_path,model_path):
    try:
        data_matrix = pd.read_csv(file_path, sep=',')
    except:
        data_matrix = pd.read_csv(file_path, sep=',',encoding='gbk')
    data_matrix.fillna('',inplace=True)

    ent_model_path = model_path + '/ent/ent_module_mark.m'
    ent_model_inner_path = model_path + '/ent/ent_inner_C15.m'
    model_path = model_path + '/base/base_module_mark.m'
    model = load_model(model_path)
    ent_model = load_model(ent_model_path)
    ent_model_inner = load_model(ent_model_inner_path)

    newEntList = []
    newEntList_entmodule = []
    count = 0
    count_ent_module = 0
    for row in tqdm(data_matrix.iterrows()):
        entname = row[1]['entname']
        regcap = row[1]['regcap']
        if regcap == '':
            regcap = 0
        empnum = row[1]['empnum']
        if empnum == '':
            empnum = 0
        estdate = row[1]['estdate']
        candate = row[1]['candate']
        revdate = row[1]['revdate']
        entstatus = row[1]['entstatus']
        opto = row[1]['opto']
        enttype = row[1]['enttype']
        entcat = row[1]['entcat']
        industryphy = row[1]['industryphy']
        regcapcur = row[1]['regcapcur']
        industryco = row[1]['industryco']
        opfrom = row[1]['opfrom']

        oldEnt = CompanyBaseinfoSummary.objects.filter(entname__exact=entname)
        oldEnt1 = EntModule.objects.filter(entname__exact=entname)
        if len(oldEnt):
            oldEnt[0].regcap = regcap
            oldEnt[0].empnum = empnum
            oldEnt[0].estdate = estdate
            oldEnt[0].candate = candate
            oldEnt[0].revdate = revdate
            oldEnt[0].entstatus = entstatus
            oldEnt[0].opto = opto
            oldEnt[0].enttype = enttype
            oldEnt[0].entcat = entcat
            oldEnt[0].industryphy = industryphy
            oldEnt[0].regcapcur = regcapcur
            oldEnt[0].industryco = industryco
            oldEnt[0].opfrom = opfrom

            oldEnt[0].regcap_type = predict(np.array(oldEnt[0].regcap), model)[0]
            oldEnt[0].company_baseinfo_module = oldEnt[0].regcap_type
            oldEnt[0].rank = oldEnt[0].regcap_type
            oldEnt[0].save()

            if len(oldEnt1):
                oldEnt1[0].company_baseinfo_module_type = oldEnt[0].regcap_type
                ent_mark = get_module_mark(oldEnt1[0], ent_weight_dict)
                oldEnt1[0].ent = ent_mark
                oldEnt1[0].ent_type = predict(ent_mark,model=ent_model)
                ent_type_list = get_ent_module_type_list(entmodule=oldEnt1[0], weight_dict=ent_weight_dict)
                oldEnt1[0].ent_inner_type = inner_predict(ent_type_list, ent_model_inner)

                oldEnt1[0].save()
            else:
                newEntModule = EntModule(entname=entname, company_baseinfo_module_type=oldEnt[0].regcap_type, risk_module_type=0,
                                         investment_module_type=0, creativity_module_type=0, brand_module_type=0,
                                         recruit_module_type=0, credit_module_type=0)
                ent_mark = get_module_mark(oldEnt1[0], ent_weight_dict)
                newEntModule.ent = ent_mark
                newEntModule.ent_type = predict(ent_mark, model=ent_model)
                ent_type_list = get_ent_module_type_list(entmodule=newEntModule, weight_dict=ent_weight_dict)
                newEntModule.ent_inner_type = inner_predict(ent_type_list, ent_model_inner)

                newEntList_entmodule.append(newEntModule)
                count_ent_module += 1

                if count_ent_module / 5000 == 1:
                    EntModule.objects.bulk_create(newEntList_entmodule)
                    newEntList_entmodule = []
                    count_ent_module = 0

        else:
            regcap_type = predict(np.array(regcap), model)[0]

            if len(oldEnt1):
                oldEnt1[0].company_baseinfo_module_type = regcap_type
                ent_mark = get_module_mark(oldEnt1[0],ent_weight_dict)
                oldEnt1[0].ent = ent_mark
                oldEnt1[0].ent_type = predict(ent_mark, model=ent_model)
                ent_type_list = get_ent_module_type_list(entmodule=oldEnt1[0], weight_dict=ent_weight_dict)
                oldEnt1[0].ent_inner_type = inner_predict(ent_type_list, ent_model_inner)

                oldEnt1[0].save()

            else:
                newEntModule = EntModule(entname=entname, company_baseinfo_module_type=regcap_type, risk_module_type=0,  investment_module_type=0,creativity_module_type=0,brand_module_type=0,recruit_module_type=0,credit_module_type=0)
                ent_mark = get_module_mark(newEntModule,ent_weight_dict)
                newEntModule.ent = ent_mark
                newEntModule.ent_type = predict(ent_mark, model=ent_model)
                ent_type_list = get_ent_module_type_list(entmodule=newEntModule, weight_dict=ent_weight_dict)
                newEntModule.ent_inner_type = inner_predict(ent_type_list, ent_model_inner)
                newEntList_entmodule.append(newEntModule)
                count_ent_module += 1

                if count_ent_module / 5000 == 1:
                    EntModule.objects.bulk_create(newEntList_entmodule)
                    newEntList_entmodule = []
                    count_ent_module = 0

            newEnt = CompanyBaseinfoSummary(entname=entname, regcap=regcap, empnum=empnum, estdate=estdate,candate=candate,revdate=revdate,
                                            entstatus=entstatus,opto=opto,enttype=enttype,entcat=entcat,industryphy=industryphy,
                                            regcapcur=regcapcur,industryco=industryco,opfrom=opfrom,regcap_type=regcap_type,company_baseinfo_module=regcap_type,rank=regcap_type)

            newEntList.append(newEnt)
            count += 1
            if count / 5000 == 1:
                CompanyBaseinfoSummary.objects.bulk_create(newEntList)
                newEntList = []
                count = 0

    EntModule.objects.bulk_create(newEntList_entmodule)
    CompanyBaseinfoSummary.objects.bulk_create(newEntList)

def change_info_update(file_path):
    data_matrix = pd.read_csv(file_path, sep=',',encoding='gbk')
    data_matrix.fillna(0,inplace=True)


    newEntList = []
    newEntList_ent_module = []

    count = 0
    count_ent_module = 0

    for row in tqdm(data_matrix.iterrows()):
        entname = row[1]['entname']
        remark = row[1]['remark']
        dataflag = row[1]['dataflag']
        alttime = row[1]['alttime']
        altitem = row[1]['altitem']
        cxstatus = row[1]['cxstatus']
        altdate = row[1]['altdate']
        openo = row[1]['openo']
        newEnt = ChangeInfo(entname=entname,remark=remark,dataflag=dataflag,alttime=alttime,altitem=altitem,cxstatus=cxstatus,
                            altdate=altdate,openo=openo)
        newEntList.append(newEnt)
        if count / 5000 == 1:
            ChangeInfo.objects.bulk_create(newEntList)
            newEntList = []
            count = 0

        oldEnt_ent_module = EntModule.objects.filter(entname__exact=entname)
        # ent_module
        if len(oldEnt_ent_module) == 0:

            newEntModule = EntModule(entname=entname, company_baseinfo_module_type=0,
                                     risk_module_type=0, investment_module_type=0,
                                     creativity_module_type=0,
                                     brand_module_type=0, recruit_module_type=0,
                                     credit_module_type=0,ent=0,ent_type=0,ent_inner_type=0)

            newEntList_ent_module.append(newEntModule)
            count_ent_module += 1

            if count_ent_module / 5000 == 1:
                EntModule.objects.bulk_create(newEntList_ent_module)
                newEntList_ent_module = []
                count_ent_module = 0

    ChangeInfo.objects.bulk_create(newEntList)
    EntModule.objects.bulk_create(newEntList_ent_module)


# investment



def ent_bid_predict(file_path,model_path):
    data_matrix = pd.read_csv(file_path, sep=',')

    ent_model_path = model_path + '/ent/ent_module_mark.m'
    ent_inner_model_path = model_path + '/ent/ent_inner_C15.m'
    ent_investment_model_path = model_path + '/investment/investment_module_mark.m'
    model_path = model_path + '/investment/ent_bid-bidnum.m'
    model = load_model(model_path)
    ent_model = load_model(ent_model_path)
    ent_inner_model = load_model(ent_inner_model_path)
    ent_investment_model = load_model(ent_investment_model_path)

    newEntList = []
    newEntList_investment_module = []
    newEntList_ent_module = []

    count = 0
    count_investment_module = 0
    count_ent_module = 0

    for row in tqdm(data_matrix.iterrows()):
        entname = row[1]['entname']
        bidnum = row[1]['bidnum']

        oldEnt = EntBid.objects.filter(entname__exact=entname)
        oldEnt_investment_module = InvestmentModule.objects.filter(entname__exact=entname)
        oldEnt_ent_module = EntModule.objects.filter(entname__exact=entname)

        bidnum_type = 0

        if len(oldEnt):
            oldEnt[0].bidnum += bidnum
            bidnum_type = predict(np.array(oldEnt[0].bidnum), model)[0]
            oldEnt[0].bidnum_type = bidnum_type
            oldEnt[0].save()

        else:
            bidnum_type = predict(np.array(bidnum), model)[0]
            newEnt = EntBid(entname=entname, bidnum=bidnum, bidnum_type=bidnum_type)
            newEntList.append(newEnt)
            count += 1

            if count / 5000 == 1:
                EntBid.objects.bulk_create(newEntList)
                newEntList = []
                count = 0

        # investment_module
        investment_module_type = 0

        if len(oldEnt_investment_module):
            oldEnt_investment_module[0].bidnum_type = bidnum_type
            ent_investment_module_mark = get_module_mark(oldEnt_investment_module[0], investment_weight_dict)
            oldEnt_investment_module[0].investment_module = ent_investment_module_mark
            investment_module_type = predict(ent_investment_module_mark, model=ent_investment_model)
            oldEnt_investment_module[0].investment_module_type = investment_module_type

            oldEnt_investment_module[0].save()

        else:
            new_investment_module = InvestmentModule(entname=entname, insurance_num_type=0, bidnum_type=bidnum_type,branchnum_type=0,
                                                     subconam_total_type=0,liacconam_total_type=0,lisubconam_total_type=0)
            ent_investment_module_mark = get_module_mark(new_investment_module, investment_weight_dict)
            new_investment_module.investment_module = ent_investment_module_mark
            investment_module_type = predict(ent_investment_module_mark, model=ent_investment_model)
            new_investment_module.investment_module_type = investment_module_type

            newEntList_investment_module.append(new_investment_module)
            count_investment_module += 1

            if count_investment_module / 5000 == 1:
                InvestmentModule.objects.bulk_create(newEntList_investment_module)
                newEntList_investment_module = []
                count_investment_module = 0

        # ent_module
        if len(oldEnt_ent_module):
            oldEnt_ent_module[0].investment_module_type = investment_module_type
            ent_mark = get_module_mark(oldEnt_ent_module[0], ent_weight_dict)
            oldEnt_ent_module[0].ent = ent_mark

            oldEnt_ent_module[0].ent_type = predict(ent_mark, model=ent_model)
            ent_type_list = get_ent_module_type_list(entmodule=oldEnt_ent_module[0], weight_dict=ent_weight_dict)
            oldEnt_ent_module[0].ent_inner_type = inner_predict(ent_type_list, ent_inner_model)

            oldEnt_ent_module[0].save()
        else:
            # newEntModule = EntModule(entname=entname, company_baseinfo_module_type=0,
            #                          risk_module_type=0, investment_module_type=investment_module_type,
            #                          creativity_module_type=0,
            #                          brand_module_type=0, recruit_module_type=0,
            #                          credit_module_type=0)
            newEntModule = EntModule(entname=entname,  investment_module_type=investment_module_type)
            ent_mark = get_module_mark(newEntModule, ent_weight_dict)
            newEntModule.ent = ent_mark
            newEntModule.ent_type = predict(ent_mark, model=ent_model)
            ent_type_list = get_ent_module_type_list(entmodule=newEntModule, weight_dict=ent_weight_dict)
            newEntModule.ent_inner_type = inner_predict(ent_type_list, ent_inner_model)

            newEntList_ent_module.append(newEntModule)
            count_ent_module += 1

            if count_ent_module / 5000 == 1:
                EntModule.objects.bulk_create(newEntList_ent_module)
                newEntList_ent_module = []
                count_ent_module = 0

    EntBid.objects.bulk_create(newEntList)
    InvestmentModule.objects.bulk_create(newEntList_investment_module)
    EntModule.objects.bulk_create(newEntList_ent_module)



def ent_branch_predict(file_path,model_path):
    data_matrix = pd.read_csv(file_path, sep=',')

    ent_model_path = model_path + '/ent/ent_module_mark.m'
    ent_inner_model_path = model_path + '/ent/ent_inner_C15.m'
    ent_investment_model_path = model_path + '/investment/investment_module_mark.m'
    model_path = model_path + '/investment/ent_branch-branchnum.m'
    model = load_model(model_path)
    ent_model = load_model(ent_model_path)
    ent_inner_model = load_model(ent_inner_model_path)
    ent_investment_model = load_model(ent_investment_model_path)

    newEntList = []
    newEntList_investment_module = []
    newEntList_ent_module = []

    count = 0
    count_investment_module = 0
    count_ent_module = 0

    for row in tqdm(data_matrix.iterrows()):
        entname = row[1]['entname']
        branchnum = row[1]['branchnum']

        oldEnt = EntBranch.objects.filter(entname__exact=entname)
        oldEnt_investment_module = InvestmentModule.objects.filter(entname__exact=entname)
        oldEnt_ent_module = EntModule.objects.filter(entname__exact=entname)

        branchnum_type = 0

        if len(oldEnt):
            oldEnt[0].branchnum += branchnum
            branchnum_type = predict(np.array(oldEnt[0].branchnum), model)[0]
            oldEnt[0].branchnum_type = branchnum_type
            oldEnt[0].save()

        else:
            branchnum_type = predict(np.array(branchnum), model)[0]
            newEnt = EntBranch(entname=entname, branchnum=branchnum, branchnum_type=branchnum_type)
            newEntList.append(newEnt)
            count += 1

            if count / 5000 == 1:
                EntBranch.objects.bulk_create(newEntList)
                newEntList = []
                count = 0

        # investment_module
        investment_module_type = 0
        if len(oldEnt_investment_module):
            oldEnt_investment_module[0].branchnum_type = branchnum_type
            ent_investment_module_mark = get_module_mark(oldEnt_investment_module[0],
                                                                    investment_weight_dict)
            oldEnt_investment_module[0].investment_module = ent_investment_module_mark
            investment_module_type = predict(ent_investment_module_mark, model=ent_investment_model)
            oldEnt_investment_module[0].investment_module_type = investment_module_type

            oldEnt_investment_module[0].save()

        else:
            # new_investment_module = InvestmentModule(entname=entname, insurance_num_type=0, bidnum_type=0,
            #                                          branchnum_type=branchnum_type,
            #                                          subconam_total_type=0, liacconam_type=0, lisubconam_type=0)
            new_investment_module = InvestmentModule(entname=entname, branchnum_type=branchnum_type)
            ent_investment_module_mark = get_module_mark(new_investment_module, investment_weight_dict)
            new_investment_module.investment_module = ent_investment_module_mark
            investment_module_type = predict(ent_investment_module_mark, model=ent_investment_model)
            new_investment_module.investment_module_type = investment_module_type

            newEntList_investment_module.append(new_investment_module)
            count_investment_module += 1

            if count_investment_module / 5000 == 1:
                InvestmentModule.objects.bulk_create(newEntList_investment_module)
                newEntList_investment_module = []
                count_investment_module = 0

        # ent_module
        if len(oldEnt_ent_module):
            oldEnt_ent_module[0].investment_module_type = investment_module_type
            ent_mark = get_module_mark(oldEnt_ent_module[0], ent_weight_dict)
            oldEnt_ent_module[0].ent = ent_mark

            oldEnt_ent_module[0].ent_type = predict(ent_mark, model=ent_model)
            ent_type_list = get_ent_module_type_list(entmodule=oldEnt_ent_module[0], weight_dict=ent_weight_dict)
            oldEnt_ent_module[0].ent_inner_type = inner_predict(ent_type_list, ent_inner_model)

            oldEnt_ent_module[0].save()
        else:
            # newEntModule = EntModule(entname=entname, company_baseinfo_module_type=0,
            #                          risk_module_type=0, investment_module_type=investment_module_type,
            #                          creativity_module_type=0,
            #                          brand_module_type=0, recruit_module_type=0,
            #                          credit_module_type=0)
            newEntModule = EntModule(entname=entname, investment_module_type=investment_module_type)
            ent_mark = get_module_mark(newEntModule, ent_weight_dict)
            newEntModule.ent = ent_mark
            newEntModule.ent_type = predict(ent_mark, model=ent_model)
            ent_type_list = get_ent_module_type_list(entmodule=newEntModule, weight_dict=ent_weight_dict)
            newEntModule.ent_inner_type = inner_predict(ent_type_list, ent_inner_model)

            newEntList_ent_module.append(newEntModule)
            count_ent_module += 1

            if count_ent_module / 5000 == 1:
                EntModule.objects.bulk_create(newEntList_ent_module)
                newEntList_ent_module = []
                count_ent_module = 0

    EntBranch.objects.bulk_create(newEntList)
    InvestmentModule.objects.bulk_create(newEntList_investment_module)
    EntModule.objects.bulk_create(newEntList_ent_module)

# 处理
def ent_contribution_predict(file_path,model_path):

    try:
        data_matrix = pd.read_csv(file_path, sep=',')
    except:
        data_matrix = pd.read_csv(file_path, sep=',',encoding='gbk')
    data_matrix.fillna('0',inplace=True)
    data_matrix_total = data_matrix.groupby('entname').sum().reset_index()

    ent_model_path = model_path + '/ent/ent_module_mark.m'
    ent_inner_model_path = model_path + '/ent/ent_inner_C15.m'
    ent_investment_model_path = model_path + '/investment/investment_module_mark.m'
    model_path = model_path + '/investment/ent_contribution-subconam_total.m'
    model = load_model(model_path)
    ent_model = load_model(ent_model_path)
    ent_inner_model = load_model(ent_inner_model_path)
    ent_investment_model = load_model(ent_investment_model_path)

    newEntList = []
    newEntList_total = []
    newEntList_investment_module = []
    newEntList_ent_module = []

    count = 0
    count_total = 0
    count_investment_module = 0
    count_ent_module = 0

    for row in tqdm(data_matrix.iterrows()):
        entname = row[1]['entname']
        invtype = row[1]['invtype']
        conform = row[1]['conform']
        subconam = row[1]['subconam']
        conprop = row[1]['conprop']
        condate = row[1]['condate']

        newEnt = EntContribution(entname=entname,invtype=invtype,conform=conform,subconam=subconam,conprop=conprop,condate=condate)
        newEntList.append(newEnt)
        count += 1

        if count / 5000 == 1:
            EntContribution.objects.bulk_create(newEntList)
            newEntList = []
            count = 0

    for row in tqdm(data_matrix_total.iterrows()):
        entname = row[1]['entname']
        subconam_total = row[1]['subconam']
        subconam_total = float(subconam_total)

        oldEnt = EntContributionTotal.objects.filter(entname__exact=entname)
        oldEnt_investment_module = InvestmentModule.objects.filter(entname__exact=entname)
        oldEnt_ent_module = EntModule.objects.filter(entname__exact=entname)

        subconam_total_type = 0

        if len(oldEnt):
            oldEnt[0].subconam_total += subconam_total
            subconam_total_type = predict(np.array(oldEnt[0].subconam_total), model)[0]
            oldEnt[0].subconam_total_type = subconam_total_type

            oldEnt[0].save()

        else:
            subconam_total_type = predict(np.array(subconam_total), model)[0]
            newEnt_total = EntContributionTotal(entname=entname, subconam_total=subconam_total,
                                                    subconam_total_type=subconam_total_type)
            newEntList_total.append(newEnt_total)
            count_total += 1

            if count_total / 5000 == 1:
                EntContributionTotal.objects.bulk_create(newEnt_total)
                newEnt_total = []
                count_total = 0

        investment_module_type = 0

        if len(oldEnt_investment_module):
            oldEnt_investment_module[0].subconam_total_type = subconam_total_type
            ent_investment_module_mark = get_module_mark(oldEnt_investment_module[0], investment_weight_dict)
            oldEnt_investment_module[0].investment_module = ent_investment_module_mark
            investment_module_type = predict(ent_investment_module_mark, model=ent_investment_model)
            oldEnt_investment_module[0].investment_module_type = investment_module_type

            oldEnt_investment_module[0].save()

        else:
            new_investment_module = InvestmentModule(entname=entname, subconam_total_type=subconam_total_type)
            ent_investment_module_mark = get_module_mark(new_investment_module, investment_weight_dict)
            new_investment_module.investment_module = ent_investment_module_mark
            investment_module_type = predict(ent_investment_module_mark, model=ent_investment_model)
            new_investment_module.investment_module_type = investment_module_type

            newEntList_investment_module.append(new_investment_module)
            count_investment_module += 1

            if count_investment_module / 5000 == 1:
                InvestmentModule.objects.bulk_create(newEntList_investment_module)
                newEntList_investment_module = []
                count_investment_module = 0

        # ent_module
        if len(oldEnt_ent_module):
            oldEnt_ent_module[0].investment_module_type = investment_module_type
            ent_mark = get_module_mark(oldEnt_ent_module[0], ent_weight_dict)
            oldEnt_ent_module[0].ent = ent_mark

            oldEnt_ent_module[0].ent_type = predict(ent_mark, model=ent_model)
            ent_type_list = get_ent_module_type_list(entmodule=oldEnt_ent_module[0], weight_dict=ent_weight_dict)
            oldEnt_ent_module[0].ent_inner_type = inner_predict(ent_type_list, ent_inner_model)

            oldEnt_ent_module[0].save()
        else:
            # newEntModule = EntModule(entname=entname, company_baseinfo_module_type=0,
            #                          risk_module_type=0, investment_module_type=investment_module_type,
            #                          creativity_module_type=0,
            #                          brand_module_type=0, recruit_module_type=0,
            #                          credit_module_type=0)
            newEntModule = EntModule(entname=entname, investment_module_type=investment_module_type)
            ent_mark = get_module_mark(newEntModule, ent_weight_dict)
            newEntModule.ent = ent_mark
            newEntModule.ent_type = predict(ent_mark, model=ent_model)
            ent_type_list = get_ent_module_type_list(entmodule=newEntModule, weight_dict=ent_weight_dict)
            newEntModule.ent_inner_type = inner_predict(ent_type_list, ent_inner_model)

            newEntList_ent_module.append(newEntModule)
            count_ent_module += 1

            if count_ent_module / 5000 == 1:
                EntModule.objects.bulk_create(newEntList_ent_module)
                newEntList_ent_module = []
                count_ent_module = 0

    EntContribution.objects.bulk_create(newEntList)
    EntContributionTotal.objects.bulk_create(newEntList_total)
    InvestmentModule.objects.bulk_create(newEntList_investment_module)
    EntModule.objects.bulk_create(newEntList_ent_module)

# 需要修改
def ent_contribution_year_predict(file_path,model_path):
    try:
        data_matrix = pd.read_csv(file_path, sep=',')
    except:
        data_matrix = pd.read_csv(file_path, sep=',',encoding='gbk')
    data_matrix_year_total = data_matrix.groupby('entname').sum().reset_index()

    ent_model_path = model_path + '/ent/ent_module_mark.m'
    ent_inner_model_path = model_path + '/ent/ent_inner_C15.m'
    ent_investment_model_path = model_path + '/investment/investment_module_mark.m'
    model_path_liacconam = model_path + '/investment/ent_contribution_year-liacconam_total.m'
    model_path_lisubconam = model_path + '/investment/ent_contribution_year-lisubconam_total.m'
    model_liacconam = load_model(model_path_liacconam)
    model_lisubconam = load_model(model_path_lisubconam)


    ent_model = load_model(ent_model_path)
    ent_inner_model = load_model(ent_inner_model_path)
    ent_investment_model = load_model(ent_investment_model_path)

    newEntList = []
    newEntList_year_total = []
    newEntList_investment_module = []
    newEntList_ent_module = []

    count = 0
    count_year_total = 0
    count_investment_module = 0
    count_ent_module = 0


    # 直接插入
    for row in tqdm(data_matrix.iterrows()):
        entname = row[1]['entname']
        subconcurrency = row[1]['subconcurrency']
        accondate = row[1]['accondate']
        subconform = row[1]['subconform']
        anchetype = row[1]['anchetype']
        subcondate = row[1]['subcondate']
        acconcurrency = row[1]['acconcurrency']
        acconform = row[1]['acconform']
        liacconam = row[1]['liacconam']
        lisubconam = row[1]['lisubconam']

        newEnt = EntContributionYear(entname=entname, subconcurrency=subconcurrency, accondate=accondate, subconform=subconform,
                                     anchetype=anchetype,subcondate=subcondate,acconcurrency=acconcurrency,acconform=acconform,
                                     liacconam=liacconam,lisubconam=lisubconam)
        newEntList.append(newEnt)

    for row in tqdm(data_matrix_year_total.iterrows()):
        entname = row[1]['entname']
        liacconam = row[1]['liacconam']
        lisubconam = row[1]['lisubconam']

        oldEnt = EntContributionYearTotal.objects.filter(entname__exact=entname)
        oldEnt_investment_module = InvestmentModule.objects.filter(entname__exact=entname)
        oldEnt_ent_module = EntModule.objects.filter(entname__exact=entname)

        liacconam_type = 0
        lisubconam_type = 0

        if len(oldEnt):
            oldEnt[0].liacconam += liacconam
            oldEnt[0].lisubconam += lisubconam
            liacconam_type = predict(np.array(oldEnt[0].liacconam), model_liacconam)[0]
            lisubconam_type = predict(np.array(oldEnt[0].lisubconam), model_lisubconam)[0]
            oldEnt[0].liacconam_type = liacconam_type
            oldEnt[0].lisubconam_type = lisubconam_type

            oldEnt[0].save()

        else:

            liacconam_type = predict(np.array(liacconam), model_liacconam)[0]
            lisubconam_type = predict(np.array(lisubconam), model_lisubconam)[0]
            newEnt_year_total = EntContributionYearTotal(entname=entname, liacconam=liacconam,lisubconam=lisubconam,
                                                             liacconam_type=liacconam_type, lisubconam_type=lisubconam_type)
            newEntList_year_total.append(newEnt_year_total)
            count_year_total += 1

            if count_year_total / 5000 == 1:
                EntContributionTotal.objects.bulk_create(newEnt_total)
                newEnt_total = []
                count_year_total = 0

        investment_module_type = 0

        if len(oldEnt_investment_module):
            oldEnt_investment_module[0].liacconam_total_type = liacconam_type
            oldEnt_investment_module[0].lisubconam_total_type = lisubconam_type

            ent_investment_module_mark = get_module_mark(oldEnt_investment_module[0], investment_weight_dict)
            oldEnt_investment_module[0].investment_module = ent_investment_module_mark
            investment_module_type = predict(ent_investment_module_mark, model=ent_investment_model)
            oldEnt_investment_module[0].investment_module_type = investment_module_type

            oldEnt_investment_module[0].save()

        else:
            new_investment_module = InvestmentModule(entname=entname, liacconam_total_type =liacconam_type, lisubconam_total_type=lisubconam_type)
            ent_investment_module_mark = get_module_mark(new_investment_module, investment_weight_dict)
            new_investment_module.investment_module = ent_investment_module_mark
            investment_module_type = predict(ent_investment_module_mark, model=ent_investment_model)
            new_investment_module.investment_module_type = investment_module_type

            newEntList_investment_module.append(new_investment_module)
            count_investment_module += 1

            if count_investment_module / 5000 == 1:
                InvestmentModule.objects.bulk_create(newEntList_investment_module)
                newEntList_investment_module = []
                count_investment_module = 0

        # ent_module
        if len(oldEnt_ent_module):
            oldEnt_ent_module[0].investment_module_type = investment_module_type
            ent_mark = get_module_mark(oldEnt_ent_module[0], ent_weight_dict)
            oldEnt_ent_module[0].ent = ent_mark

            oldEnt_ent_module[0].ent_type = predict(ent_mark, model=ent_model)
            ent_type_list = get_ent_module_type_list(entmodule=oldEnt_ent_module[0], weight_dict=ent_weight_dict)
            oldEnt_ent_module[0].ent_inner_type = inner_predict(ent_type_list, ent_inner_model)

            oldEnt_ent_module[0].save()
        else:
            newEntModule = EntModule(entname=entname, investment_module_type=investment_module_type)
            ent_mark = get_module_mark(newEntModule, ent_weight_dict)
            newEntModule.ent = ent_mark
            newEntModule.ent_type = predict(ent_mark, model=ent_model)
            ent_type_list = get_ent_module_type_list(entmodule=newEntModule, weight_dict=ent_weight_dict)
            newEntModule.ent_inner_type = inner_predict(ent_type_list, ent_inner_model)

            newEntList_ent_module.append(newEntModule)
            count_ent_module += 1

            if count_ent_module / 5000 == 1:
                EntModule.objects.bulk_create(newEntList_ent_module)
                newEntList_ent_module = []
                count_ent_module = 0


    EntContributionYear.objects.bulk_create(newEntList)
    EntContributionYearTotal.objects.bulk_create(newEntList_year_total)
    InvestmentModule.objects.bulk_create(newEntList_investment_module)
    EntModule.objects.bulk_create(newEntList_ent_module)




def ent_guarantee_update(file_path):
    try:
        data_matrix = pd.read_csv(file_path, sep=',')
    except:
        data_matrix = pd.read_csv(file_path, sep=',',encoding='gbk')

    data_matrix.fillna('',inplace=True)

    newEntList = []
    newEntList_investment_module = []
    newEntList_ent_module = []

    count = 0
    count_investment_module = 0
    count_ent_module = 0

    for row in tqdm(data_matrix.iterrows()):
        # print(row)
        entname = row[1]['entname']
        priclaseckind = row[1]['priclaseckind']
        pefperfrom = row[1]['pefperfrom']
        iftopub = row[1]['iftopub']
        priclasecam = row[1]['priclasecam']
        pefperto = row[1]['pefperto']
        guaranperiod = row[1]['guaranperiod']
        gatype = row[1]['gatype']
        rage = row[1]['rage']
        newEnt = EntGuarantee(entname=entname, priclaseckind=priclaseckind, pefperfrom=pefperfrom, iftopub=iftopub,
                              priclasecam=priclasecam, pefperto=pefperto,guaranperiod=guaranperiod, gatype=gatype,
                              rage=rage)
        newEntList.append(newEnt)
        count += 1

        if count / 5000 == 1:
            EntGuarantee.objects.bulk_create(newEntList)
            newEntList = []
            count = 0

        oldEnt_investment_module = InvestmentModule.objects.filter(entname__exact=entname)
        oldEnt_ent_module = EntModule.objects.filter(entname__exact=entname)


        if len(oldEnt_investment_module) == 0 :
            new_investment_module = InvestmentModule(entname=entname)
            newEntList_investment_module.append(new_investment_module)
            count_investment_module += 1

            if count_investment_module / 5000 == 1:
                InvestmentModule.objects.bulk_create(newEntList_investment_module)
                newEntList_investment_module = []
                count_investment_module = 0

        # ent_module
        if len(oldEnt_ent_module) == 0:
            newEntModule = EntModule(entname=entname)

            newEntList_ent_module.append(newEntModule)
            count_ent_module += 1

            if count_ent_module / 5000 == 1:
                EntModule.objects.bulk_create(newEntList_ent_module)
                newEntList_ent_module = []
                count_ent_module = 0

    EntGuarantee.objects.bulk_create(newEntList)
    InvestmentModule.objects.bulk_create(newEntList_investment_module)
    EntModule.objects.bulk_create(newEntList_ent_module)

def ent_investment_predict(file_path,model_path):
    data_matrix = pd.read_csv(file_path, sep=',')

    ent_model_path = model_path + '/ent/ent_module_mark.m'
    ent_inner_model_path = model_path + '/ent/ent_inner_C15.m'
    ent_investment_model_path = model_path + '/investment/investment_module_mark.m'
    model_path = model_path + '/investment/ent_investment-investnum.m'
    model = load_model(model_path)
    ent_model = load_model(ent_model_path)
    ent_inner_model = load_model(ent_inner_model_path)
    ent_investment_model = load_model(ent_investment_model_path)

    newEntList = []
    newEntList_investment_module = []
    newEntList_ent_module = []

    count = 0
    count_investment_module = 0
    count_ent_module = 0

    for row in tqdm(data_matrix.iterrows()):
        entname = row[1]['entname']
        investnum = row[1]['investnum']

        oldEnt = EntInvestment.objects.filter(entname__exact=entname)
        oldEnt_investment_module = InvestmentModule.objects.filter(entname__exact=entname)
        oldEnt_ent_module = EntModule.objects.filter(entname__exact=entname)

        investnum_type = 0
        if len(oldEnt):
            oldEnt[0].investnum += investnum
            investnum_type = predict(np.array(oldEnt[0].investnum), model)[0]
            oldEnt[0].investnum_type = investnum_type
            oldEnt[0].save()

        else:
            investnum_type = predict(np.array(investnum), model)[0]
            newEnt = EntInvestment(entname=entname, investnum=investnum, investnum_type=investnum_type)
            newEntList.append(newEnt)
            count += 1

            if count / 5000 == 1:
                EntInvestment.objects.bulk_create(newEntList)
                newEntList = []
                count = 0

        # investment_module
        investment_module_type = 0

        if len(oldEnt_investment_module):
            oldEnt_investment_module[0].investnum_type = investnum_type
            ent_investment_module_mark = get_module_mark(oldEnt_investment_module[0], investment_weight_dict)
            oldEnt_investment_module[0].investment_module = ent_investment_module_mark
            investment_module_type = predict(ent_investment_module_mark, model=ent_investment_model)
            oldEnt_investment_module[0].investment_module_type = investment_module_type

            oldEnt_investment_module[0].save()
        else:
            new_investment_module = InvestmentModule(entname=entname, investnum_type=investnum_type)
            ent_investment_module_mark = get_module_mark(new_investment_module, investment_weight_dict)
            new_investment_module.investment_module = ent_investment_module_mark
            investment_module_type = predict(ent_investment_module_mark, model=ent_investment_model)
            new_investment_module.investment_module_type = investment_module_type

            newEntList_investment_module.append(new_investment_module)
            count_investment_module += 1

            if count_investment_module / 5000 == 1:
                InvestmentModule.objects.bulk_create(newEntList_investment_module)
                newEntList_investment_module = []
                count_investment_module = 0

        # ent_module
        if len(oldEnt_ent_module):
            oldEnt_ent_module[0].investment_module_type = investment_module_type
            ent_mark = get_module_mark(oldEnt_ent_module[0], ent_weight_dict)
            oldEnt_ent_module[0].ent = ent_mark

            oldEnt_ent_module[0].ent_type = predict(ent_mark, model=ent_model)
            ent_type_list = get_ent_module_type_list(entmodule=oldEnt_ent_module[0], weight_dict=ent_weight_dict)
            oldEnt_ent_module[0].ent_inner_type = inner_predict(ent_type_list, ent_inner_model)

            oldEnt_ent_module[0].save()
        else:
            # newEntModule = EntModule(entname=entname, company_baseinfo_module_type=0,
            #                          risk_module_type=0, investment_module_type=investment_module_type,
            #                          creativity_module_type=0,
            #                          brand_module_type=0, recruit_module_type=0,
            #                          credit_module_type=0)
            newEntModule = EntModule(entname=entname,  investment_module_type=investment_module_type)
            ent_mark = get_module_mark(newEntModule, ent_weight_dict)
            newEntModule.ent = ent_mark
            newEntModule.ent_type = predict(ent_mark, model=ent_model)
            ent_type_list = get_ent_module_type_list(entmodule=newEntModule, weight_dict=ent_weight_dict)
            newEntModule.ent_inner_type = inner_predict(ent_type_list, ent_inner_model)

            newEntList_ent_module.append(newEntModule)
            count_ent_module += 1

            if count_ent_module / 5000 == 1:
                EntModule.objects.bulk_create(newEntList_ent_module)
                newEntList_ent_module = []
                count_ent_module = 0

    EntInvestment.objects.bulk_create(newEntList)
    InvestmentModule.objects.bulk_create(newEntList_investment_module)
    EntModule.objects.bulk_create(newEntList_ent_module)


def ent_onlineshop_predict(file_path,model_path):
    data_matrix = pd.read_csv(file_path, sep=',')

    ent_model_path = model_path + '/ent/ent_module_mark.m'
    ent_inner_model_path = model_path + '/ent/ent_inner_C15.m'
    ent_investment_model_path = model_path + '/investment/ent_investment-investnum.m'
    model_path = model_path + '/investment/ent_onlineshop-shopnum.m'
    model = load_model(model_path)
    ent_model = load_model(ent_model_path)
    ent_inner_model = load_model(ent_inner_model_path)
    ent_investment_model = load_model(ent_investment_model_path)

    newEntList = []
    newEntList_investment_module = []
    newEntList_ent_module = []

    count = 0
    count_investment_module = 0
    count_ent_module = 0


    for row in tqdm(data_matrix.iterrows()):
        entname = row[1]['entname']
        shopnum = row[1]['shopnum']

        oldEnt = EntOnlineshop.objects.filter(entname__exact=entname)
        oldEnt_investment_module = InvestmentModule.objects.filter(entname__exact=entname)
        oldEnt_ent_module = EntModule.objects.filter(entname__exact=entname)

        shopnum_type = 0
        if len(oldEnt):
            oldEnt[0].shopnum += shopnum
            shopnum_type = predict(np.array(oldEnt[0].shopnum), model)[0]
            oldEnt[0].shopnum_type = shopnum_type
            oldEnt[0].save()

        else:
            shopnum_type = predict(np.array(shopnum), model)[0]
            newEnt = EntOnlineshop(entname=entname, shopnum =shopnum, shopnum_type=shopnum_type)
            newEntList.append(newEnt)
            count += 1

            if count / 5000 == 1:
                EntBid.objects.bulk_create(newEntList)
                newEntList = []
                count = 0
        # investment_module
        investment_module_type = 0

        if len(oldEnt_investment_module):
            oldEnt_investment_module[0].shopnum_type = shopnum_type
            ent_investment_module_mark = get_module_mark(oldEnt_investment_module[0], investment_weight_dict)
            oldEnt_investment_module[0].investment_module = ent_investment_module_mark
            investment_module_type = predict(ent_investment_module_mark, model=ent_investment_model)
            oldEnt_investment_module[0].investment_module_type = investment_module_type

            oldEnt_investment_module[0].save()

        else:
            # new_investment_module = InvestmentModule(entname=entname, insurance_num_type=0,
            #                                          bidnum_type=bidnum_type, branchnum_type=0,
            #                                          subconam_total_type=0, liacconam_type=0, lisubconam_type=0)
            new_investment_module = InvestmentModule(entname=entname, shopnum_type=shopnum_type)

            ent_investment_module_mark = get_module_mark(new_investment_module, investment_weight_dict)
            new_investment_module.investment_module = ent_investment_module_mark
            investment_module_type = predict(ent_investment_module_mark, model=ent_investment_model)
            new_investment_module.investment_module_type = investment_module_type

            newEntList_investment_module.append(new_investment_module)
            count_investment_module += 1

            if count_investment_module / 5000 == 1:
                InvestmentModule.objects.bulk_create(newEntList_investment_module)
                newEntList_investment_module = []
                count_investment_module = 0

        # ent_module
        if len(oldEnt_ent_module):
            oldEnt_ent_module[0].investment_module_type = investment_module_type
            ent_mark = get_module_mark(oldEnt_ent_module[0], ent_weight_dict)
            oldEnt_ent_module[0].ent = ent_mark

            oldEnt_ent_module[0].ent_type = predict(ent_mark, model=ent_model)
            ent_type_list = get_ent_module_type_list(entmodule=oldEnt_ent_module[0], weight_dict=ent_weight_dict)
            oldEnt_ent_module[0].ent_inner_type = inner_predict(ent_type_list, ent_inner_model)

            oldEnt_ent_module[0].save()
        else:
            # newEntModule = EntModule(entname=entname, company_baseinfo_module_type=0,
            #                          risk_module_type=0, investment_module_type=investment_module_type,
            #                          creativity_module_type=0,
            #                          brand_module_type=0, recruit_module_type=0,
            #                          credit_module_type=0)
            newEntModule = EntModule(entname=entname, investment_module_type=investment_module_type)
            ent_mark = get_module_mark(newEntModule, ent_weight_dict)
            newEntModule.ent = ent_mark
            newEntModule.ent_type = predict(ent_mark, model=ent_model)
            ent_type_list = get_ent_module_type_list(entmodule=newEntModule, weight_dict=ent_weight_dict)
            newEntModule.ent_inner_type = inner_predict(ent_type_list, ent_inner_model)

            newEntList_ent_module.append(newEntModule)
            count_ent_module += 1

            if count_ent_module / 5000 == 1:
                EntModule.objects.bulk_create(newEntList_ent_module)
                newEntList_ent_module = []
                count_ent_module = 0

    EntOnlineshop.objects.bulk_create(newEntList)
    InvestmentModule.objects.bulk_create(newEntList_investment_module)
    EntModule.objects.bulk_create(newEntList_ent_module)


def enterprise_insurance_predict(file_path, model_path):
    try:
        data_matrix = pd.read_csv(file_path, sep=',')
    except:
        data_matrix = pd.read_csv(file_path, sep=',',encoding='gbk')
    data_matrix_avg = data_matrix.groupby('entname').sum().reset_index()

    ent_model_path = model_path + '/ent/ent_module_mark.m'
    ent_inner_model_path = model_path + '/ent/ent_inner_C15.m'

    ent_investment_model_path = model_path + '/investment/investment_module_mark.m'
    model_path += '/investment/enterprise_insurance_year_avg-insurance_num.m'
    model = load_model(model_path)
    ent_model = load_model(ent_model_path)
    ent_inner_model = load_model(ent_inner_model_path)
    ent_investment_model = load_model(ent_investment_model_path)

    newEntList = []
    newEntList_avg = []
    newEntList_investment_module = []
    newEntList_ent_module = []

    count = 0
    count_avg = 0
    count_investment_module = 0
    count_ent_module = 0

    for row in tqdm(data_matrix.iterrows()):
        print(row)
        entname = row[1]['entname']
        cbrq = row[1]['cbrq']
        xzbz = row[1]['xzbz']
        sbjgbh = row[1]['sbjgbh']
        xzbzmc = row[1]['xzbzmc']
        cbzt = row[1]['cbzt']
        cbztmc = row[1]['cbztmc']
        dwbh = row[1]['dwbh']
        newEnt = EnterpriseInsurance(entname=entname, cbrq=cbrq, xzbz=xzbz,sbjgbh=sbjgbh, xzbzmc=xzbzmc,
                              cbzt=cbzt, cbztmc=cbztmc, dwbh=dwbh)
        newEntList.append(newEnt)
        count += 1

        if count / 5000 == 1:
            EnterpriseInsurance.objects.bulk_create(newEntList)
            newEntList = []
            count = 0

    for row in tqdm(data_matrix_avg.iterrows()):
        entname = row[1]['entname']
        insurance_num = row[1]['cbzt']

        oldEnt = EnterpriseInsuranceYearAvg.objects.filter(entname__exact=entname)
        oldEnt_investment_module = InvestmentModule.objects.filter(entname__exact=entname)
        oldEnt_ent_module = EntModule.objects.filter(entname__exact=entname)

        insurance_num_type = 0
        if len(oldEnt):
            oldEnt[0].insurance_num += insurance_num
            insurance_num_type = predict(np.array(oldEnt[0].insurance_num), model)[0]
            oldEnt[0].insurance_num_type = insurance_num_type

            oldEnt[0].save()

        else:
            insurance_num_type = predict(np.array(insurance_num), model)[0]
            newEnt_avg = EnterpriseInsuranceYearAvg(entname=entname, insurance_num=insurance_num,insurance_num_type=insurance_num_type)
            newEntList_avg.append(newEnt_avg)
            count_avg += 1

            if count_avg / 5000 == 1:
                EnterpriseInsuranceYearAvg.objects.bulk_create(newEntList_avg)
                newEntList_avg = []
                count_avg = 0

        investment_module_type = 0
        if len(oldEnt_investment_module):
            oldEnt_investment_module[0].insurance_num_type = insurance_num_type
            ent_investment_module_mark = get_module_mark(oldEnt_investment_module[0], investment_weight_dict)
            oldEnt_investment_module[0].investment_module = ent_investment_module_mark
            investment_module_type = predict(ent_investment_module_mark, model=ent_investment_model)
            oldEnt_investment_module[0].investment_module_type = investment_module_type

            oldEnt_investment_module[0].save()

        else:
            new_investment_module = InvestmentModule(entname=entname, insurance_num_type=insurance_num_type)
            ent_investment_module_mark = get_module_mark(new_investment_module, investment_weight_dict)
            new_investment_module.investment_module = ent_investment_module_mark
            investment_module_type = predict(ent_investment_module_mark, model=ent_investment_model)
            new_investment_module.investment_module_type = investment_module_type

            newEntList_investment_module.append(new_investment_module)
            count_investment_module += 1

            if count_investment_module / 5000 == 1:
                InvestmentModule.objects.bulk_create(newEntList_investment_module)
                newEntList_investment_module = []
                count_investment_module = 0

        # ent_module
        if len(oldEnt_ent_module):
            oldEnt_ent_module[0].investment_module_type = investment_module_type
            ent_mark = get_module_mark(oldEnt_ent_module[0], ent_weight_dict)
            oldEnt_ent_module[0].ent = ent_mark

            oldEnt_ent_module[0].ent_type = predict(ent_mark, model=ent_model)
            ent_type_list = get_ent_module_type_list(entmodule=oldEnt_ent_module[0], weight_dict=ent_weight_dict)
            oldEnt_ent_module[0].ent_inner_type = inner_predict(ent_type_list, ent_inner_model)

            oldEnt_ent_module[0].save()
        else:
            newEntModule = EntModule(entname=entname, investment_module_type=investment_module_type)
            ent_mark = get_module_mark(newEntModule, ent_weight_dict)
            newEntModule.ent = ent_mark
            newEntModule.ent_type = predict(ent_mark, model=ent_model)
            ent_type_list = get_ent_module_type_list(entmodule=newEntModule, weight_dict=ent_weight_dict)
            newEntModule.ent_inner_type = inner_predict(ent_type_list, ent_inner_model)

            newEntList_ent_module.append(newEntModule)
            count_ent_module += 1

            if count_ent_module / 5000 == 1:
                EntModule.objects.bulk_create(newEntList_ent_module)
                newEntList_ent_module = []
                count_ent_module = 0

    EnterpriseInsurance.objects.bulk_create(newEntList)
    EnterpriseInsuranceYearAvg.objects.bulk_create(newEntList_avg)
    InvestmentModule.objects.bulk_create(newEntList_investment_module)
    EntModule.objects.bulk_create(newEntList_ent_module)

# risk

# 处理


def administrative_punishment_predict(file_path,model_path):
    data_matrix = pd.read_csv(file_path, sep=',')

    ent_model_path = model_path + '/ent/ent_module_mark.m'
    ent_inner_model_path = model_path + '/ent/ent_inner_C15.m'
    ent_risk_model_path = model_path + '/risk/risk_module_mark.m'
    model_path = model_path + '/risk/administrative_punishment-is_punish.m'
    model = load_model(model_path)
    ent_model = load_model(ent_model_path)
    ent_inner_model = load_model(ent_inner_model_path)
    ent_risk_model = load_model(ent_risk_model_path)

    newEntList = []
    newEntList_risk_module = []
    newEntList_ent_module = []

    count = 0
    count_risk_module = 0
    count_ent_module = 0

    for row in tqdm(data_matrix.iterrows()):
        entname = row[1]['entname']
        is_punish = row[1]['is_punish']

        oldEnt = AdministrativePunishment.objects.filter(entname__exact=entname)
        oldEnt_risk_module = RiskModule.objects.filter(entname__exact=entname)
        oldEnt_ent_module = EntModule.objects.filter(entname__exact=entname)

        is_punish_type = 0
        if len(oldEnt):
            oldEnt[0].is_punish += is_punish
            is_punish_type = predict(np.array(oldEnt[0].is_punish), model)[0]
            oldEnt[0].is_punish_type = is_punish_type
            oldEnt[0].save()

        else:
            is_punish_type = predict(np.array(is_punish), model)[0]
            newEnt = AdministrativePunishment(entname=entname, is_punish=is_punish, is_punish_type=is_punish_type)
            newEntList.append(newEnt)
            count += 1

            if count / 5000 == 1:
                AdministrativePunishment.objects.bulk_create(newEntList)
                newEntList = []
                count = 0

        # risk_module
        risk_module_type = 0

        if len(oldEnt_risk_module):
            oldEnt_risk_module[0].is_punish_type = is_punish_type
            ent_risk_module_mark = get_module_mark(oldEnt_risk_module[0], risk_weight_dict)
            oldEnt_risk_module[0].risk_module = ent_risk_module_mark
            risk_module_type = predict(ent_risk_module_mark, model=ent_risk_model)
            oldEnt_risk_module[0].risk_module_type = risk_module_type
            # 不再需要inner_type

            oldEnt_risk_module[0].save()

        else:
            new_risk_module = RiskModule(entname=entname, is_punish_type=is_punish_type)
            ent_risk_module_mark = get_module_mark(new_risk_module, risk_weight_dict)
            new_risk_module.risk_module = ent_risk_module_mark
            risk_module_type = predict(ent_risk_module_mark, model=ent_risk_model)
            new_risk_module.risk_module_type = risk_module_type

            newEntList_risk_module.append(new_risk_module)
            count_risk_module += 1

            if count_risk_module / 5000 == 1:
                RiskModule.objects.bulk_create(newEntList_risk_module)
                newEntList_risk_module = []
                count_risk_module = 0

        # ent_module
        if len(oldEnt_ent_module):
            oldEnt_ent_module[0].risk_module_type = risk_module_type
            ent_mark = get_module_mark(oldEnt_ent_module[0], ent_weight_dict)
            oldEnt_ent_module[0].ent = ent_mark

            oldEnt_ent_module[0].ent_type = predict(ent_mark, model=ent_model)
            ent_type_list = get_ent_module_type_list(entmodule=oldEnt_ent_module[0], weight_dict=ent_weight_dict)
            oldEnt_ent_module[0].ent_inner_type = inner_predict(ent_type_list, ent_inner_model)

            oldEnt_ent_module[0].save()
        else:
            newEntModule = EntModule(entname=entname, risk_module_type=0)
            ent_mark = get_module_mark(newEntModule, ent_weight_dict)
            newEntModule.ent = ent_mark
            newEntModule.ent_type = predict(ent_mark, model=ent_model)
            ent_type_list = get_ent_module_type_list(entmodule=newEntModule, weight_dict=ent_weight_dict)
            newEntModule.ent_inner_type = inner_predict(ent_type_list, ent_inner_model)

            newEntList_ent_module.append(newEntModule)
            count_ent_module += 1

            if count_ent_module / 5000 == 1:
                EntModule.objects.bulk_create(newEntList_ent_module)
                newEntList_ent_module = []
                count_ent_module = 0

    AdministrativePunishment.objects.bulk_create(newEntList)
    RiskModule.objects.bulk_create(newEntList_risk_module)
    EntModule.objects.bulk_create(newEntList_ent_module)

def business_risk_abnormal_predict(file_path,model_path):
    data_matrix = pd.read_csv(file_path, sep=',')

    ent_model_path = model_path + '/ent/ent_module_mark.m'
    ent_inner_model_path = model_path + '/ent/ent_inner_C15.m'
    ent_risk_model_path = model_path + '/risk/risk_module_mark.m'
    model_path = model_path + '/risk/business_risk_abnormal-is_bra.m'
    model = load_model(model_path)
    ent_model = load_model(ent_model_path)
    ent_inner_model = load_model(ent_inner_model_path)
    ent_risk_model = load_model(ent_risk_model_path)

    newEntList = []
    newEntList_risk_module = []
    newEntList_ent_module = []

    count = 0
    count_risk_module = 0
    count_ent_module = 0

    for row in tqdm(data_matrix.iterrows()):
        entname = row[1]['entname']
        is_bra = row[1]['is_bra']

        oldEnt = BusinessRiskAbnormal.objects.filter(entname__exact=entname)
        oldEnt_risk_module = RiskModule.objects.filter(entname__exact=entname)
        oldEnt_ent_module = EntModule.objects.filter(entname__exact=entname)

        is_bra_type = 0
        if len(oldEnt):
            oldEnt[0].is_bra += is_bra
            is_bra_type = predict(np.array(oldEnt[0].is_bra), model)[0]
            oldEnt[0].is_bra_type = is_bra_type
            oldEnt[0].save()

        else:
            is_bra_type = predict(np.array(is_bra), model)[0]
            newEnt = BusinessRiskAbnormal(entname=entname, is_bra=is_bra, is_bra_type=is_bra_type)
            newEntList.append(newEnt)
            count += 1

            if count / 5000 == 1:
                BusinessRiskAbnormal.objects.bulk_create(newEntList)
                newEntList = []
                count = 0
                # risk_module
                risk_module_type = 0

        if len(oldEnt_risk_module):
            oldEnt_risk_module[0].is_bra_type = is_bra_type
            ent_risk_module_mark = get_module_mark(oldEnt_risk_module[0], risk_weight_dict)
            oldEnt_risk_module[0].risk_module = ent_risk_module_mark
            risk_module_type = predict(ent_risk_module_mark, model=ent_risk_model)
            oldEnt_risk_module[0].risk_module_type = risk_module_type
            # 不再需要inner_type

            oldEnt_risk_module[0].save()

        else:
            new_risk_module = RiskModule(entname=entname, is_bra_type=is_bra_type)
            ent_risk_module_mark = get_module_mark(new_risk_module, risk_weight_dict)
            new_risk_module.risk_module = ent_risk_module_mark
            risk_module_type = predict(ent_risk_module_mark, model=ent_risk_model)
            new_risk_module.risk_module_type = risk_module_type

            newEntList_risk_module.append(new_risk_module)
            count_risk_module += 1

            if count_risk_module / 5000 == 1:
                RiskModule.objects.bulk_create(newEntList_risk_module)
                newEntList_risk_module = []
                count_risk_module = 0

        # ent_module
        if len(oldEnt_ent_module):
            oldEnt_ent_module[0].risk_module_type = risk_module_type
            ent_mark = get_module_mark(oldEnt_ent_module[0], ent_weight_dict)
            oldEnt_ent_module[0].ent = ent_mark

            oldEnt_ent_module[0].ent_type = predict(ent_mark, model=ent_model)
            ent_type_list = get_ent_module_type_list(entmodule=oldEnt_ent_module[0], weight_dict=ent_weight_dict)
            oldEnt_ent_module[0].ent_inner_type = inner_predict(ent_type_list, ent_inner_model)

            oldEnt_ent_module[0].save()
        else:
            newEntModule = EntModule(entname=entname, risk_module_type=0)
            ent_mark = get_module_mark(newEntModule, ent_weight_dict)
            newEntModule.ent = ent_mark
            newEntModule.ent_type = predict(ent_mark, model=ent_model)
            ent_type_list = get_ent_module_type_list(entmodule=newEntModule, weight_dict=ent_weight_dict)
            newEntModule.ent_inner_type = inner_predict(ent_type_list, ent_inner_model)

            newEntList_ent_module.append(newEntModule)
            count_ent_module += 1

            if count_ent_module / 5000 == 1:
                EntModule.objects.bulk_create(newEntList_ent_module)
                newEntList_ent_module = []
                count_ent_module = 0

    BusinessRiskAbnormal.objects.bulk_create(newEntList)
    RiskModule.objects.bulk_create(newEntList_risk_module)
    EntModule.objects.bulk_create(newEntList_ent_module)


def business_risk_all_punish_predict(file_path,model_path):
    data_matrix = pd.read_csv(file_path, sep=',')

    ent_model_path = model_path + '/ent/ent_module_mark.m'
    ent_inner_model_path = model_path + '/ent/ent_inner_C15.m'
    ent_risk_model_path = model_path + '/risk/risk_module_mark.m'
    model_path = model_path + '/risk/business_risk_all_punish-is_brap.m'
    model = load_model(model_path)
    ent_model = load_model(ent_model_path)
    ent_inner_model = load_model(ent_inner_model_path)
    ent_risk_model = load_model(ent_risk_model_path)

    newEntList = []
    newEntList_risk_module = []
    newEntList_ent_module = []

    count = 0
    count_risk_module = 0
    count_ent_module = 0

    for row in tqdm(data_matrix.iterrows()):
        entname = row[1]['entname']
        is_brap = row[1]['is_brap']

        oldEnt = BusinessRiskAllPunish.objects.filter(entname__exact=entname)
        oldEnt_risk_module = RiskModule.objects.filter(entname__exact=entname)
        oldEnt_ent_module = EntModule.objects.filter(entname__exact=entname)

        is_brap_type = 0
        if len(oldEnt):
            oldEnt[0].is_brap += is_brap
            is_brap_type = predict(np.array(oldEnt[0].is_brap), model)[0]
            oldEnt[0].is_brap_type = is_brap_type
            oldEnt[0].save()

        else:
            is_brap_type = predict(np.array(is_brap), model)[0]
            newEnt = BusinessRiskAllPunish(entname=entname, is_brap=is_brap, is_brap_type=is_brap_type)
            newEntList.append(newEnt)
            count += 1

            if count / 5000 == 1:
                BusinessRiskAllPunish.objects.bulk_create(newEntList)
                newEntList = []
                count = 0

        # risk_module
        risk_module_type = 0

        if len(oldEnt_risk_module):
            oldEnt_risk_module[0].is_brap_type = is_brap_type
            ent_risk_module_mark = get_module_mark(oldEnt_risk_module[0], risk_weight_dict)
            oldEnt_risk_module[0].risk_module = ent_risk_module_mark
            risk_module_type = predict(ent_risk_module_mark, model=ent_risk_model)
            oldEnt_risk_module[0].risk_module_type = risk_module_type
            # 不再需要inner_type

            oldEnt_risk_module[0].save()

        else:
            new_risk_module = RiskModule(entname=entname, is_brap_type=is_brap_type)
            ent_risk_module_mark = get_module_mark(new_risk_module, risk_weight_dict)
            new_risk_module.risk_module = ent_risk_module_mark
            risk_module_type = predict(ent_risk_module_mark, model=ent_risk_model)
            new_risk_module.risk_module_type = risk_module_type

            newEntList_risk_module.append(new_risk_module)
            count_risk_module += 1

            if count_risk_module / 5000 == 1:
                RiskModule.objects.bulk_create(newEntList_risk_module)
                newEntList_risk_module = []
                count_risk_module = 0

        # ent_module
        if len(oldEnt_ent_module):
            oldEnt_ent_module[0].risk_module_type = risk_module_type
            ent_mark = get_module_mark(oldEnt_ent_module[0], ent_weight_dict)
            oldEnt_ent_module[0].ent = ent_mark

            oldEnt_ent_module[0].ent_type = predict(ent_mark, model=ent_model)
            ent_type_list = get_ent_module_type_list(entmodule=oldEnt_ent_module[0], weight_dict=ent_weight_dict)
            oldEnt_ent_module[0].ent_inner_type = inner_predict(ent_type_list, ent_inner_model)

            oldEnt_ent_module[0].save()
        else:
            newEntModule = EntModule(entname=entname, risk_module_type=0)
            ent_mark = get_module_mark(newEntModule, ent_weight_dict)
            newEntModule.ent = ent_mark
            newEntModule.ent_type = predict(ent_mark, model=ent_model)
            ent_type_list = get_ent_module_type_list(entmodule=newEntModule, weight_dict=ent_weight_dict)
            newEntModule.ent_inner_type = inner_predict(ent_type_list, ent_inner_model)

            newEntList_ent_module.append(newEntModule)
            count_ent_module += 1

            if count_ent_module / 5000 == 1:
                EntModule.objects.bulk_create(newEntList_ent_module)
                newEntList_ent_module = []
                count_ent_module = 0

    BusinessRiskAllPunish.objects.bulk_create(newEntList)
    RiskModule.objects.bulk_create(newEntList_risk_module)
    EntModule.objects.bulk_create(newEntList_ent_module)



def business_risk_taxunpaid_predict(file_path,model_path):
    data_matrix = pd.read_csv(file_path, sep=',',encoding='gbk')

    ent_model_path = model_path + '/ent/ent_module_mark.m'
    ent_inner_model_path = model_path + '/ent/ent_inner_C15.m'
    ent_risk_model_path = model_path + '/risk/risk_module_mark.m'
    model_path = model_path + '/risk/business_risk_taxunpaid-taxunpaidnum.m'
    model = load_model(model_path)
    ent_model = load_model(ent_model_path)
    ent_inner_model = load_model(ent_inner_model_path)
    ent_risk_model = load_model(ent_risk_model_path)

    newEntList = []
    newEntList_risk_module = []
    newEntList_ent_module = []

    count = 0
    count_risk_module = 0
    count_ent_module = 0

    for row in tqdm(data_matrix.iterrows()):
        print(row)
        entname = row[1]['entname']
        taxunpaidnum = row[1]['taxunpaidnum']
        taxunpaidnum = float(taxunpaidnum.replace(',',''))

        oldEnt = BusinessRiskTaxunpaid.objects.filter(entname__exact=entname)
        oldEnt_risk_module = RiskModule.objects.filter(entname__exact=entname)
        oldEnt_ent_module = EntModule.objects.filter(entname__exact=entname)

        taxunpaidnum_type = 0
        if len(oldEnt):
            oldEnt[0].taxunpaidnum += taxunpaidnum
            taxunpaidnum_type = predict(np.array(oldEnt[0].taxunpaidnum), model)[0]
            oldEnt[0].taxunpaidnum_type = taxunpaidnum_type
            oldEnt[0].save()

        else:
            taxunpaidnum_type = predict(np.array(taxunpaidnum), model)[0]
            newEnt = BusinessRiskTaxunpaid(entname=entname, taxunpaidnum=taxunpaidnum, taxunpaidnum_type=taxunpaidnum_type)
            newEntList.append(newEnt)
            count += 1

            if count / 5000 == 1:
                BusinessRiskTaxunpaid.objects.bulk_create(newEntList)
                newEntList = []
                count = 0

        # risk_module
        risk_module_type = 0

        if len(oldEnt_risk_module):
            oldEnt_risk_module[0].taxunpaidnum_type = taxunpaidnum_type
            ent_risk_module_mark = get_module_mark(oldEnt_risk_module[0], risk_weight_dict)
            oldEnt_risk_module[0].risk_module = ent_risk_module_mark
            risk_module_type = predict(ent_risk_module_mark, model=ent_risk_model)
            oldEnt_risk_module[0].risk_module_type = risk_module_type
            # 不再需要inner_type

            oldEnt_risk_module[0].save()

        else:
            new_risk_module = RiskModule(entname=entname, taxunpaidnum_type=taxunpaidnum_type)
            ent_risk_module_mark = get_module_mark(new_risk_module, risk_weight_dict)
            new_risk_module.risk_module = ent_risk_module_mark
            risk_module_type = predict(ent_risk_module_mark, model=ent_risk_model)
            new_risk_module.risk_module_type = risk_module_type

            newEntList_risk_module.append(new_risk_module)
            count_risk_module += 1

            if count_risk_module / 5000 == 1:
                RiskModule.objects.bulk_create(newEntList_risk_module)
                newEntList_risk_module = []
                count_risk_module = 0

        # ent_module
        if len(oldEnt_ent_module):
            oldEnt_ent_module[0].risk_module_type = risk_module_type
            ent_mark = get_module_mark(oldEnt_ent_module[0], ent_weight_dict)
            oldEnt_ent_module[0].ent = ent_mark

            oldEnt_ent_module[0].ent_type = predict(ent_mark, model=ent_model)
            ent_type_list = get_ent_module_type_list(entmodule=oldEnt_ent_module[0], weight_dict=ent_weight_dict)
            oldEnt_ent_module[0].ent_inner_type = inner_predict(ent_type_list, ent_inner_model)

            oldEnt_ent_module[0].save()
        else:
            newEntModule = EntModule(entname=entname, risk_module_type=0)
            ent_mark = get_module_mark(newEntModule, ent_weight_dict)
            newEntModule.ent = ent_mark
            newEntModule.ent_type = predict(ent_mark, model=ent_model)
            ent_type_list = get_ent_module_type_list(entmodule=newEntModule, weight_dict=ent_weight_dict)
            newEntModule.ent_inner_type = inner_predict(ent_type_list, ent_inner_model)

            newEntList_ent_module.append(newEntModule)
            count_ent_module += 1

            if count_ent_module / 5000 == 1:
                EntModule.objects.bulk_create(newEntList_ent_module)
                newEntList_ent_module = []
                count_ent_module = 0

    BusinessRiskTaxunpaid.objects.bulk_create(newEntList)
    RiskModule.objects.bulk_create(newEntList_risk_module)
    EntModule.objects.bulk_create(newEntList_ent_module)



def business_risk_rightpledge_predict(file_path,model_path):
    data_matrix = pd.read_csv(file_path, sep=',')

    ent_model_path = model_path + '/ent/ent_module_mark.m'
    ent_inner_model_path = model_path + '/ent/ent_inner_C15.m'
    ent_risk_model_path = model_path + '/risk/risk_module_mark.m'
    model_path = model_path + '/risk/business_risk_rightpledge-pledgenum.m'
    model = load_model(model_path)
    ent_model = load_model(ent_model_path)
    ent_inner_model = load_model(ent_inner_model_path)
    ent_risk_model = load_model(ent_risk_model_path)

    newEntList = []
    newEntList_risk_module = []
    newEntList_ent_module = []

    count = 0
    count_risk_module = 0
    count_ent_module = 0

    for row in tqdm(data_matrix.iterrows()):
        entname = row[1]['entname']
        pledgenum = row[1]['pledgenum']

        oldEnt = BusinessRiskRightpledge.objects.filter(entname__exact=entname)
        oldEnt_risk_module = RiskModule.objects.filter(entname__exact=entname)
        oldEnt_ent_module = EntModule.objects.filter(entname__exact=entname)

        pledgenum_type = 0
        if len(oldEnt):
            oldEnt[0].pledgenum += pledgenum
            pledgenum_type = predict(np.array(oldEnt[0].pledgenum), model)[0]
            oldEnt[0].pledgenum_type = pledgenum_type
            oldEnt[0].save()

        else:
            pledgenum_type = predict(np.array(pledgenum), model)[0]
            newEnt = BusinessRiskRightpledge(entname=entname, pledgenum=pledgenum,
                                           pledgenum_type=pledgenum_type)
            newEntList.append(newEnt)
            if count / 5000 == 1:
                AdministrativePunishment.objects.bulk_create(newEntList)
                newEntList = []
                count = 0

        # risk_module
        risk_module_type = 0

        if len(oldEnt_risk_module):
            oldEnt_risk_module[0].pledgenum_type = pledgenum_type
            ent_risk_module_mark = get_module_mark(oldEnt_risk_module[0], risk_weight_dict)
            oldEnt_risk_module[0].risk_module = ent_risk_module_mark
            risk_module_type = predict(ent_risk_module_mark, model=ent_risk_model)
            oldEnt_risk_module[0].risk_module_type = risk_module_type
            # 不再需要inner_type

            oldEnt_risk_module[0].save()

        else:
            new_risk_module = RiskModule(entname=entname, pledgenum_type=pledgenum_type)
            ent_risk_module_mark = get_module_mark(new_risk_module, risk_weight_dict)
            new_risk_module.risk_module = ent_risk_module_mark
            risk_module_type = predict(ent_risk_module_mark, model=ent_risk_model)
            new_risk_module.risk_module_type = risk_module_type

            newEntList_risk_module.append(new_risk_module)
            count_risk_module += 1

            if count_risk_module / 5000 == 1:
                RiskModule.objects.bulk_create(newEntList_risk_module)
                newEntList_risk_module = []
                count_risk_module = 0

        # ent_module
        if len(oldEnt_ent_module):
            oldEnt_ent_module[0].risk_module_type = risk_module_type
            ent_mark = get_module_mark(oldEnt_ent_module[0], ent_weight_dict)
            oldEnt_ent_module[0].ent = ent_mark

            oldEnt_ent_module[0].ent_type = predict(ent_mark, model=ent_model)
            ent_type_list = get_ent_module_type_list(entmodule=oldEnt_ent_module[0], weight_dict=ent_weight_dict)
            oldEnt_ent_module[0].ent_inner_type = inner_predict(ent_type_list, ent_inner_model)

            oldEnt_ent_module[0].save()
        else:
            newEntModule = EntModule(entname=entname, risk_module_type=0)
            ent_mark = get_module_mark(newEntModule, ent_weight_dict)
            newEntModule.ent = ent_mark
            newEntModule.ent_type = predict(ent_mark, model=ent_model)
            ent_type_list = get_ent_module_type_list(entmodule=newEntModule, weight_dict=ent_weight_dict)
            newEntModule.ent_inner_type = inner_predict(ent_type_list, ent_inner_model)

            newEntList_ent_module.append(newEntModule)
            count_ent_module += 1

            if count_ent_module / 5000 == 1:
                EntModule.objects.bulk_create(newEntList_ent_module)
                newEntList_ent_module = []
                count_ent_module = 0

    BusinessRiskRightpledge.objects.bulk_create(newEntList)
    RiskModule.objects.bulk_create(newEntList_risk_module)
    EntModule.objects.bulk_create(newEntList_ent_module)


def ent_social_security_predict(file_path,model_path):
    try:
        data_matrix = pd.read_csv(file_path, sep=',')
    except:
        data_matrix = pd.read_csv(file_path, sep=',',encoding='gbk')
    data_matrix['unpaid_sum'] = data_matrix['unpaidsocialins_so110'] + data_matrix['unpaidsocialins_so210'] + data_matrix['unpaidsocialins_so310'] + data_matrix['unpaidsocialins_so410'] + data_matrix['unpaidsocialins_so510']
    data_matrix_deal = data_matrix.loc[data_matrix['unpaid_sum'] != 0]

    ent_model_path = model_path + '/ent/ent_module_mark.m'
    ent_inner_model_path = model_path + '/ent/ent_inner_C15.m'
    ent_risk_model_path = model_path + '/risk/risk_module_mark.m'
    model_path = model_path + '/risk/ent_social_security-unpaid_sum.m'
    model = load_model(model_path)
    ent_model = load_model(ent_model_path)
    ent_inner_model = load_model(ent_inner_model_path)
    ent_risk_model = load_model(ent_risk_model_path)


    newEntList = []
    newEntListP = []
    newEntList_risk_module = []
    newEntList_ent_module = []

    count = 0
    count_p = 0
    count_risk_module = 0
    count_ent_module = 0


    # 简单添加
    for row in tqdm(data_matrix.iterrows()):
        entname = row[1]['entname']
        unpaidsocialins_so110 = row[1]['unpaidsocialins_so110']
        unpaidsocialins_so210 = row[1]['unpaidsocialins_so210']
        unpaidsocialins_so310 = row[1]['unpaidsocialins_so310']
        unpaidsocialins_so410 = row[1]['unpaidsocialins_so410']
        unpaidsocialins_so510 = row[1]['unpaidsocialins_so510']
        updatetime = row[1]['updatetime']

        newEnt = EntSocialSecurity(entname=entname,unpaidsocialins_so110=unpaidsocialins_so110,
                                   unpaidsocialins_so210=unpaidsocialins_so210,unpaidsocialins_so310=unpaidsocialins_so310,
                                   unpaidsocialins_so410=unpaidsocialins_so410,unpaidsocialins_so510=unpaidsocialins_so510,
                                   updatetime=updatetime)

        newEntList.append(newEnt)
        count += 1

        if count / 5000 == 1:
            EntSocialSecurity.objects.bulk_create(newEntList)
            newEntList = []
            count = 0
    EntSocialSecurity.objects.bulk_create(newEntList)

    for row in tqdm(data_matrix.iterrows()):
        entname = row[1]['entname']
        unpaid_sum = row[1]['unpaid_sum']

        oldEnt = EntSocialSecurityP.objects.filter(entname__exact=entname)
        oldEnt_risk_module = RiskModule.objects.filter(entname__exact=entname)
        oldEnt_ent_module = EntModule.objects.filter(entname__exact=entname)

        unpaid_sum_type = 0

        if len(oldEnt):
            oldEnt[0].unpaid_sum += unpaid_sum
            unpaid_sum_type = predict(np.array(oldEnt[0].unpaid_sum), model)[0]
            oldEnt[0].unpaid_sum_type = unpaid_sum_type
            oldEnt[0].save()

        else:
            unpaid_sum_type = predict(np.array(unpaid_sum), model)[0]
            if unpaid_sum != 0:
                newEntP = EntSocialSecurityP(entname=entname, unpaid_sum=unpaid_sum,
                                   unpaid_sum_type=unpaid_sum_type)
                newEntListP.append(newEntP)
                count_p += 1

            if count_p / 5000 == 1:
                EntSocialSecurityP.objects.bulk_create(newEntListP)
                newEntListP = []
                count_p = 0

        # risk_module
        risk_module_type = 0

        if len(oldEnt_risk_module):
            oldEnt_risk_module[0].unpaid_sum_type = unpaid_sum_type
            ent_risk_module_mark = get_module_mark(oldEnt_risk_module[0], risk_weight_dict)
            oldEnt_risk_module[0].risk_module = ent_risk_module_mark
            risk_module_type = predict(ent_risk_module_mark, model=ent_risk_model)
            oldEnt_risk_module[0].risk_module_type = risk_module_type
            # 不再需要inner_type

            oldEnt_risk_module[0].save()

        else:
            new_risk_module = RiskModule(entname=entname, unpaid_sum_type=unpaid_sum_type)
            ent_risk_module_mark = get_module_mark(new_risk_module, risk_weight_dict)
            new_risk_module.risk_module = ent_risk_module_mark
            risk_module_type = predict(ent_risk_module_mark, model=ent_risk_model)
            new_risk_module.risk_module_type = risk_module_type

            newEntList_risk_module.append(new_risk_module)
            count_risk_module += 1

            if count_risk_module / 5000 == 1:
                RiskModule.objects.bulk_create(newEntList_risk_module)
                newEntList_risk_module = []
                count_risk_module = 0

        # ent_module
        if len(oldEnt_ent_module):
            oldEnt_ent_module[0].risk_module_type = risk_module_type
            ent_mark = get_module_mark(oldEnt_ent_module[0], ent_weight_dict)
            oldEnt_ent_module[0].ent = ent_mark

            oldEnt_ent_module[0].ent_type = predict(ent_mark, model=ent_model)
            ent_type_list = get_ent_module_type_list(entmodule=oldEnt_ent_module[0], weight_dict=ent_weight_dict)
            oldEnt_ent_module[0].ent_inner_type = inner_predict(ent_type_list, ent_inner_model)

            oldEnt_ent_module[0].save()
        else:
            newEntModule = EntModule(entname=entname, risk_module_type=0)
            ent_mark = get_module_mark(newEntModule, ent_weight_dict)
            newEntModule.ent = ent_mark
            newEntModule.ent_type = predict(ent_mark, model=ent_model)
            ent_type_list = get_ent_module_type_list(entmodule=newEntModule, weight_dict=ent_weight_dict)
            newEntModule.ent_inner_type = inner_predict(ent_type_list, ent_inner_model)

            newEntList_ent_module.append(newEntModule)
            count_ent_module += 1

            if count_ent_module / 5000 == 1:
                EntModule.objects.bulk_create(newEntList_ent_module)
                newEntList_ent_module = []
                count_ent_module = 0

    EntSocialSecurityP.objects.bulk_create(newEntListP)
    RiskModule.objects.bulk_create(newEntList_risk_module)
    EntModule.objects.bulk_create(newEntList_ent_module)



def exception_list_predict(file_path,model_path):
    data_matrix = pd.read_csv(file_path, sep=',')

    ent_model_path = model_path + '/ent/ent_module_mark.m'
    ent_inner_model_path = model_path + '/ent/ent_inner_C15.m'
    ent_risk_model_path = model_path + '/risk/risk_module_mark.m'
    model_path = model_path + '/risk/exception_list-is_except.m'
    model = load_model(model_path)
    ent_model = load_model(ent_model_path)
    ent_inner_model = load_model(ent_inner_model_path)
    ent_risk_model = load_model(ent_risk_model_path)

    newEntList = []
    newEntList_risk_module = []
    newEntList_ent_module = []

    count = 0
    count_risk_module = 0
    count_ent_module = 0

    for row in tqdm(data_matrix.iterrows()):
        entname = row[1]['entname']
        is_except = row[1]['is_except']

        oldEnt = ExceptionList.objects.filter(entname__exact=entname)
        oldEnt_risk_module = RiskModule.objects.filter(entname__exact=entname)
        oldEnt_ent_module = EntModule.objects.filter(entname__exact=entname)

        is_except_type = 0
        if len(oldEnt):
            oldEnt[0].is_except += is_except
            is_except_type = predict(np.array(oldEnt[0].is_except), model)[0]
            oldEnt[0].is_except_type = is_except_type
            oldEnt[0].save()

        else:
            is_except_type = predict(np.array(is_except), model)[0]
            newEnt = ExceptionList(entname=entname, is_except=is_except,
                                             is_except_type=is_except_type)
            newEntList.append(newEnt)
            count += 1

            if count / 5000 == 1:
                ExceptionList.objects.bulk_create(newEntList)
                newEntList = []
                count = 0
        # risk_module
        risk_module_type = 0

        if len(oldEnt_risk_module):
            oldEnt_risk_module[0].is_except_type = is_except_type
            ent_risk_module_mark = get_module_mark(oldEnt_risk_module[0], risk_weight_dict)
            oldEnt_risk_module[0].risk_module = ent_risk_module_mark
            risk_module_type = predict(ent_risk_module_mark, model=ent_risk_model)
            oldEnt_risk_module[0].risk_module_type = risk_module_type
            # 不再需要inner_type

            oldEnt_risk_module[0].save()

        else:
            new_risk_module = RiskModule(entname=entname, is_except_type=is_except_type)
            ent_risk_module_mark = get_module_mark(new_risk_module, risk_weight_dict)
            new_risk_module.risk_module = ent_risk_module_mark
            risk_module_type = predict(ent_risk_module_mark, model=ent_risk_model)
            new_risk_module.risk_module_type = risk_module_type

            newEntList_risk_module.append(new_risk_module)
            count_risk_module += 1

            if count_risk_module / 5000 == 1:
                RiskModule.objects.bulk_create(newEntList_risk_module)
                newEntList_risk_module = []
                count_risk_module = 0

        # ent_module
        if len(oldEnt_ent_module):
            oldEnt_ent_module[0].risk_module_type = risk_module_type
            ent_mark = get_module_mark(oldEnt_ent_module[0], ent_weight_dict)
            oldEnt_ent_module[0].ent = ent_mark

            oldEnt_ent_module[0].ent_type = predict(ent_mark, model=ent_model)
            ent_type_list = get_ent_module_type_list(entmodule=oldEnt_ent_module[0], weight_dict=ent_weight_dict)
            oldEnt_ent_module[0].ent_inner_type = inner_predict(ent_type_list, ent_inner_model)

            oldEnt_ent_module[0].save()
        else:
            newEntModule = EntModule(entname=entname, risk_module_type=0)
            ent_mark = get_module_mark(newEntModule, ent_weight_dict)
            newEntModule.ent = ent_mark
            newEntModule.ent_type = predict(ent_mark, model=ent_model)
            ent_type_list = get_ent_module_type_list(entmodule=newEntModule, weight_dict=ent_weight_dict)
            newEntModule.ent_inner_type = inner_predict(ent_type_list, ent_inner_model)

            newEntList_ent_module.append(newEntModule)
            count_ent_module += 1

            if count_ent_module / 5000 == 1:
                EntModule.objects.bulk_create(newEntList_ent_module)
                newEntList_ent_module = []
                count_ent_module = 0

    ExceptionList.objects.bulk_create(newEntList)
    RiskModule.objects.bulk_create(newEntList_risk_module)
    EntModule.objects.bulk_create(newEntList_ent_module)



def justice_declare_predict(file_path,model_path):
    try:
        data_matrix = pd.read_csv(file_path, sep=',')
    except:
        data_matrix = pd.read_csv(file_path, sep=',',encoding='gbk')

    ent_model_path = model_path + '/ent/ent_module_mark.m'
    ent_inner_model_path = model_path + '/ent/ent_inner_C15.m'
    ent_risk_model_path = model_path + '/risk/risk_module_mark.m'


    model_path_date = model_path + '/risk/administrative_punishment-is_punish.m'
    model_path_appellant = model_path + '/risk/justice_declare-appellant_amount.m'
    model_path_defendant = model_path + '/risk/justice_declare-defendant_amount.m'
    model_date = load_model(model_path_date)
    model_appellant = load_model(model_path_appellant)
    model_defendant = load_model(model_path_defendant)
    ent_model = load_model(ent_model_path)
    ent_inner_model = load_model(ent_inner_model_path)
    ent_risk_model = load_model(ent_risk_model_path)


    newEntList = []
    newEntList_p = []
    newEntList_risk_module = []
    newEntList_ent_module = []

    count = 0
    count_p = 0
    count_risk_module = 0
    count_ent_module = 0

    for row in tqdm(data_matrix.iterrows()):
        entname = row[1]['entname']
        declaredate = row[1]['declaredate']
        appellant = row[1]['appellant']
        defendant = row[1]['defendant']
        declarestyle = row[1]['declarestyle']

        newEnt = JusticeDeclare(entname=entname,declaredate=declaredate,appellant=appellant,defendant=defendant,declarestyle=declarestyle)
        newEntList.append(newEnt)
        count += 1

        if count / 5000 == 1:
            JusticeDeclare.objects.bulk_create(newEntList)
            newEntList = []
            count = 0



        oldEnt = JudgeDeclareP.objects.filter(entname__exact=entname)
        oldEnt_risk_module = RiskModule.objects.filter(entname__exact=entname)
        oldEnt_ent_module = EntModule.objects.filter(entname__exact=entname)

        declaredate_type = 0
        appellant_amount_type = 0
        defendant_amount_type = 0
        if len(oldEnt):
            oldEnt[0].declaredate = declaredate
            oldEnt[0].appellant_amount += appellant
            oldEnt[0].defendant_amount += defendant
            appellant_amount_type = predict(np.array(oldEnt[0].appellant_amount), model_appellant)[0]
            defendant_amount_type = predict(np.array(oldEnt[0].defendant_amount), model_defendant)[0]
            oldEnt[0].appellant_amount_type = appellant_amount_type
            oldEnt[0].defendant_amount_type = defendant_amount_type

            oldEnt[0].save()

        else:
            appellant_amount_type = predict(np.array(appellant), model_appellant)[0]
            defendant_amount_type = predict(np.array(defendant), model_defendant)[0]
            newEnt = JudgeDeclareP(entname=entname, declaredate=declaredate,appellant_amount=appellant,defendant_amount=defendant,
                                  appellant_amount_type=appellant_amount_type,defendant_amount_type=defendant_amount_type)
            newEntList_p.append(newEnt)
            count_p += 1

            if count_p / 5000 == 1:
                JudgeDeclareP.objects.bulk_create(newEntList_p)
                newEntList_p = []
                count_p = 0

        # risk_module
        risk_module_type = 0

        if len(oldEnt_risk_module):
            oldEnt_risk_module[0].appellant_amount_type = appellant_amount_type
            oldEnt_risk_module[0].defendant_amount_type = defendant_amount_type
            ent_risk_module_mark = get_module_mark(oldEnt_risk_module[0], risk_weight_dict)
            oldEnt_risk_module[0].risk_module = ent_risk_module_mark
            risk_module_type = predict(ent_risk_module_mark, model=ent_risk_model)
            oldEnt_risk_module[0].risk_module_type = risk_module_type
            # 不再需要inner_type

            oldEnt_risk_module[0].save()

        else:
            new_risk_module = RiskModule(entname=entname,appellant_amount_type = appellant_amount_type,defendant_amount_type = defendant_amount_type)
            ent_risk_module_mark = get_module_mark(new_risk_module, risk_weight_dict)
            new_risk_module.risk_module = ent_risk_module_mark
            risk_module_type = predict(ent_risk_module_mark, model=ent_risk_model)
            new_risk_module.risk_module_type = risk_module_type

            newEntList_risk_module.append(new_risk_module)
            count_risk_module += 1

            if count_risk_module / 5000 == 1:
                RiskModule.objects.bulk_create(newEntList_risk_module)
                newEntList_risk_module = []
                count_risk_module = 0

        # ent_module
        if len(oldEnt_ent_module):
            oldEnt_ent_module[0].risk_module_type = risk_module_type
            ent_mark = get_module_mark(oldEnt_ent_module[0], ent_weight_dict)
            oldEnt_ent_module[0].ent = ent_mark

            oldEnt_ent_module[0].ent_type = predict(ent_mark, model=ent_model)
            ent_type_list = get_ent_module_type_list(entmodule=oldEnt_ent_module[0], weight_dict=ent_weight_dict)
            oldEnt_ent_module[0].ent_inner_type = inner_predict(ent_type_list, ent_inner_model)

            oldEnt_ent_module[0].save()
        else:
            newEntModule = EntModule(entname=entname, risk_module_type=0)
            ent_mark = get_module_mark(newEntModule, ent_weight_dict)
            newEntModule.ent = ent_mark
            newEntModule.ent_type = predict(ent_mark, model=ent_model)
            ent_type_list = get_ent_module_type_list(entmodule=newEntModule, weight_dict=ent_weight_dict)
            newEntModule.ent_inner_type = inner_predict(ent_type_list, ent_inner_model)

            newEntList_ent_module.append(newEntModule)
            count_ent_module += 1

            if count_ent_module / 5000 == 1:
                EntModule.objects.bulk_create(newEntList_ent_module)
                newEntList_ent_module = []
                count_ent_module = 0

    JusticeDeclare.objects.bulk_create(newEntList)
    JudgeDeclareP.objects.bulk_create(newEntList_p)
    RiskModule.objects.bulk_create(newEntList_risk_module)
    EntModule.objects.bulk_create(newEntList_ent_module)


def justice_enforced_predict(file_path,model_path):

    data_matrix = pd.read_csv(file_path, sep=',')

    ent_model_path = model_path + '/ent/ent_module_mark.m'
    ent_inner_model_path = model_path + '/ent/ent_inner_C15.m'
    ent_risk_model_path = model_path + '/risk/risk_module_mark.m'
    model_path_amount = model_path + '/risk/justice_enforced-enforce_amount.m'
    model_amount = load_model(model_path_amount)
    ent_model = load_model(ent_model_path)
    ent_inner_model = load_model(ent_inner_model_path)
    ent_risk_model = load_model(ent_risk_model_path)



    newEntList = []
    newEntList_risk_module = []
    newEntList_ent_module = []

    count = 0
    count_risk_module = 0
    count_ent_module = 0
    for row in tqdm(data_matrix.iterrows()):
        entname = row[1]['entname']
        record_date = row[1]['record_date']
        enforce_amount = row[1]['enforce_amount']

        oldEnt = JusticeEnforced.objects.filter(entname__exact=entname)
        oldEnt_risk_module = RiskModule.objects.filter(entname__exact=entname)
        oldEnt_ent_module = EntModule.objects.filter(entname__exact=entname)


        enforce_amount_type = 0

        if len(oldEnt):
            oldEnt[0].record_date = record_date
            oldEnt[0].enforce_amount += enforce_amount
            enforce_amount_type = predict(np.array(oldEnt[0].enforce_amount), model_amount)[0]
            oldEnt[0].enforce_amount_type = enforce_amount_type
            oldEnt[0].save()

        else:
            enforce_amount_type = predict(np.array(enforce_amount), model_amount)[0]
            newEnt = JusticeEnforced(entname=entname, record_date=record_date,enforce_amount=enforce_amount,
                                   enforce_amount_type=enforce_amount_type)
            newEntList.append(newEnt)
            count += 1

            if count / 5000 == 1:
                JusticeEnforced.objects.bulk_create(newEntList)
                newEntList = []
                count = 0

        # risk_module
        risk_module_type = 0

        if len(oldEnt_risk_module):
            oldEnt_risk_module[0].enforce_amount_type = enforce_amount_type
            ent_risk_module_mark = get_module_mark(oldEnt_risk_module[0], risk_weight_dict)
            oldEnt_risk_module[0].risk_module = ent_risk_module_mark
            risk_module_type = predict(ent_risk_module_mark, model=ent_risk_model)
            oldEnt_risk_module[0].risk_module_type = risk_module_type
            # 不再需要inner_type

            oldEnt_risk_module[0].save()

        else:
            new_risk_module = RiskModule(entname=entname, enforce_amount_type=enforce_amount_type)
            ent_risk_module_mark = get_module_mark(new_risk_module, risk_weight_dict)
            new_risk_module.risk_module = ent_risk_module_mark
            risk_module_type = predict(ent_risk_module_mark, model=ent_risk_model)
            new_risk_module.risk_module_type = risk_module_type

            newEntList_risk_module.append(new_risk_module)
            count_risk_module += 1

            if count_risk_module / 5000 == 1:
                RiskModule.objects.bulk_create(newEntList_risk_module)
                newEntList_risk_module = []
                count_risk_module = 0

        # ent_module
        if len(oldEnt_ent_module):
            oldEnt_ent_module[0].risk_module_type = risk_module_type
            ent_mark = get_module_mark(oldEnt_ent_module[0], ent_weight_dict)
            oldEnt_ent_module[0].ent = ent_mark

            oldEnt_ent_module[0].ent_type = predict(ent_mark, model=ent_model)
            ent_type_list = get_ent_module_type_list(entmodule=oldEnt_ent_module[0], weight_dict=ent_weight_dict)
            oldEnt_ent_module[0].ent_inner_type = inner_predict(ent_type_list, ent_inner_model)

            oldEnt_ent_module[0].save()
        else:
            newEntModule = EntModule(entname=entname, risk_module_type=0)
            ent_mark = get_module_mark(newEntModule, ent_weight_dict)
            newEntModule.ent = ent_mark
            newEntModule.ent_type = predict(ent_mark, model=ent_model)
            ent_type_list = get_ent_module_type_list(entmodule=newEntModule, weight_dict=ent_weight_dict)
            newEntModule.ent_inner_type = inner_predict(ent_type_list, ent_inner_model)

            newEntList_ent_module.append(newEntModule)
            count_ent_module += 1

            if count_ent_module / 5000 == 1:
                EntModule.objects.bulk_create(newEntList_ent_module)
                newEntList_ent_module = []
                count_ent_module = 0

    JusticeEnforced.objects.bulk_create(newEntList)
    RiskModule.objects.bulk_create(newEntList_risk_module)
    EntModule.objects.bulk_create(newEntList_ent_module)

def justice_credit_predict(file_path,model_path):
    data_matrix = pd.read_csv(file_path, sep=',')

    ent_model_path = model_path + '/ent/ent_module_mark.m'
    ent_inner_model_path = model_path + '/ent/ent_inner_C15.m'
    ent_risk_model_path = model_path + '/risk/risk_module_mark.m'
    model_path = model_path + '/risk/justice_credit-is_justice_credit.m'
    model = load_model(model_path)
    ent_model = load_model(ent_model_path)
    ent_inner_model = load_model(ent_inner_model_path)
    ent_risk_model = load_model(ent_risk_model_path)

    newEntList = []
    newEntList_risk_module = []
    newEntList_ent_module = []

    count = 0
    count_risk_module = 0
    count_ent_module = 0

    for row in tqdm(data_matrix.iterrows()):
        entname = row[1]['entname']
        is_justice_credit = row[1]['is_justice_credit']

        oldEnt = JusticeCredit.objects.filter(entname__exact=entname)
        oldEnt_risk_module = RiskModule.objects.filter(entname__exact=entname)
        oldEnt_ent_module = EntModule.objects.filter(entname__exact=entname)

        is_justice_credit_type = 0
        if len(oldEnt):
            oldEnt[0].is_justice_credit += is_justice_credit
            is_justice_credit_type = predict(np.array(oldEnt[0].is_justice_credit), model)[0]
            oldEnt[0].is_justice_credit_type = is_justice_credit_type
            oldEnt[0].save()

        else:
            is_justice_credit_type = predict(np.array(is_justice_credit), model)[0]
            newEnt = JusticeCredit(entname=entname, is_justice_credit=is_justice_credit,
                                   is_justice_credit_type=is_justice_credit_type)
            newEntList.append(newEnt)
            count += 1

            if count / 5000 == 1:
                JusticeCredit.objects.bulk_create(newEntList)
                newEntList = []
                count = 0

        # risk_module
        risk_module_type = 0

        if len(oldEnt_risk_module):
            oldEnt_risk_module[0].is_justice_credit_type = is_justice_credit_type
            ent_risk_module_mark = get_module_mark(oldEnt_risk_module[0], risk_weight_dict)
            oldEnt_risk_module[0].risk_module = ent_risk_module_mark
            risk_module_type = predict(ent_risk_module_mark, model=ent_risk_model)
            oldEnt_risk_module[0].risk_module_type = risk_module_type
            # 不再需要inner_type

            oldEnt_risk_module[0].save()

        else:
            new_risk_module = RiskModule(entname=entname, is_justice_credit_type=is_justice_credit_type)
            ent_risk_module_mark = get_module_mark(new_risk_module, risk_weight_dict)
            new_risk_module.risk_module = ent_risk_module_mark
            risk_module_type = predict(ent_risk_module_mark, model=ent_risk_model)
            new_risk_module.risk_module_type = risk_module_type

            newEntList_risk_module.append(new_risk_module)
            count_risk_module += 1

            if count_risk_module / 5000 == 1:
                RiskModule.objects.bulk_create(newEntList_risk_module)
                newEntList_risk_module = []
                count_risk_module = 0

        # ent_module
        if len(oldEnt_ent_module):
            oldEnt_ent_module[0].risk_module_type = risk_module_type
            ent_mark = get_module_mark(oldEnt_ent_module[0], ent_weight_dict)
            oldEnt_ent_module[0].ent = ent_mark

            oldEnt_ent_module[0].ent_type = predict(ent_mark, model=ent_model)
            ent_type_list = get_ent_module_type_list(entmodule=oldEnt_ent_module[0], weight_dict=ent_weight_dict)
            oldEnt_ent_module[0].ent_inner_type = inner_predict(ent_type_list, ent_inner_model)

            oldEnt_ent_module[0].save()
        else:
            newEntModule = EntModule(entname=entname, risk_module_type=0)
            ent_mark = get_module_mark(newEntModule, ent_weight_dict)
            newEntModule.ent = ent_mark
            newEntModule.ent_type = predict(ent_mark, model=ent_model)
            ent_type_list = get_ent_module_type_list(entmodule=newEntModule, weight_dict=ent_weight_dict)
            newEntModule.ent_inner_type = inner_predict(ent_type_list, ent_inner_model)

            newEntList_ent_module.append(newEntModule)
            count_ent_module += 1

            if count_ent_module / 5000 == 1:
                EntModule.objects.bulk_create(newEntList_ent_module)
                newEntList_ent_module = []
                count_ent_module = 0

    JusticeCredit.objects.bulk_create(newEntList)
    RiskModule.objects.bulk_create(newEntList_risk_module)
    EntModule.objects.bulk_create(newEntList_ent_module)


def justice_credit_aic_predict(file_path,model_path):
    data_matrix = pd.read_csv(file_path, sep=',')

    ent_model_path = model_path + '/ent/ent_module_mark.m'
    ent_inner_model_path = model_path + '/ent/ent_inner_C15.m'
    ent_risk_model_path = model_path + '/risk/risk_module_mark.m'
    model_path = model_path + '/risk/justice_credit_aic-is_justice_creditaic.m'
    model = load_model(model_path)
    ent_model = load_model(ent_model_path)
    ent_inner_model = load_model(ent_inner_model_path)
    ent_risk_model = load_model(ent_risk_model_path)

    newEntList = []
    newEntList_risk_module = []
    newEntList_ent_module = []

    count = 0
    count_risk_module = 0
    count_ent_module = 0

    for row in tqdm(data_matrix.iterrows()):
        entname = row[1]['entname']
        is_justice_credit_aic = row[1]['is_justice_creditaic']

        oldEnt = JusticeCreditAic.objects.filter(entname__exact=entname)
        oldEnt_risk_module = RiskModule.objects.filter(entname__exact=entname)
        oldEnt_ent_module = EntModule.objects.filter(entname__exact=entname)

        is_justice_creditaic_type = 0
        if len(oldEnt):
            oldEnt[0].is_justice_credit_aic += is_justice_credit_aic
            is_justice_creditaic_type = predict(np.array(oldEnt[0].is_justice_credit_aic), model)[0]
            oldEnt[0].is_justice_creditaic_type = is_justice_creditaic_type
            oldEnt[0].save()

        else:
            is_justice_creditaic_type = predict(np.array(is_justice_credit_aic), model)[0]
            newEnt = JusticeCreditAic(entname=entname, is_justice_credit_aic=is_justice_credit_aic,
                                   is_justice_creditaic_type=is_justice_creditaic_type)
            newEntList.append(newEnt)
            count += 1

            if count / 5000 == 1:
                JusticeCreditAic.objects.bulk_create(newEntList)
                newEntList = []
                count = 0

        # risk_module
        risk_module_type = 0

        if len(oldEnt_risk_module):
            oldEnt_risk_module[0].is_justice_creditaic_type = is_justice_creditaic_type
            ent_risk_module_mark = get_module_mark(oldEnt_risk_module[0], risk_weight_dict)
            oldEnt_risk_module[0].risk_module = ent_risk_module_mark
            risk_module_type = predict(ent_risk_module_mark, model=ent_risk_model)
            oldEnt_risk_module[0].risk_module_type = risk_module_type
            # 不再需要inner_type

            oldEnt_risk_module[0].save()

        else:
            new_risk_module = RiskModule(entname=entname, is_justice_creditaic_type=is_justice_creditaic_type)
            ent_risk_module_mark = get_module_mark(new_risk_module, risk_weight_dict)
            new_risk_module.risk_module = ent_risk_module_mark
            risk_module_type = predict(ent_risk_module_mark, model=ent_risk_model)
            new_risk_module.risk_module_type = risk_module_type

            newEntList_risk_module.append(new_risk_module)
            count_risk_module += 1

            if count_risk_module / 5000 == 1:
                RiskModule.objects.bulk_create(newEntList_risk_module)
                newEntList_risk_module = []
                count_risk_module = 0

        # ent_module
        if len(oldEnt_ent_module):
            oldEnt_ent_module[0].risk_module_type = risk_module_type
            ent_mark = get_module_mark(oldEnt_ent_module[0], ent_weight_dict)
            oldEnt_ent_module[0].ent = ent_mark

            oldEnt_ent_module[0].ent_type = predict(ent_mark, model=ent_model)
            ent_type_list = get_ent_module_type_list(entmodule=oldEnt_ent_module[0], weight_dict=ent_weight_dict)
            oldEnt_ent_module[0].ent_inner_type = inner_predict(ent_type_list, ent_inner_model)

            oldEnt_ent_module[0].save()
        else:
            newEntModule = EntModule(entname=entname, risk_module_type=0)
            ent_mark = get_module_mark(newEntModule, ent_weight_dict)
            newEntModule.ent = ent_mark
            newEntModule.ent_type = predict(ent_mark, model=ent_model)
            ent_type_list = get_ent_module_type_list(entmodule=newEntModule, weight_dict=ent_weight_dict)
            newEntModule.ent_inner_type = inner_predict(ent_type_list, ent_inner_model)

            newEntList_ent_module.append(newEntModule)
            count_ent_module += 1

            if count_ent_module / 5000 == 1:
                EntModule.objects.bulk_create(newEntList_ent_module)
                newEntList_ent_module = []
                count_ent_module = 0

    JusticeCreditAic.objects.bulk_create(newEntList)
    RiskModule.objects.bulk_create(newEntList_risk_module)
    EntModule.objects.bulk_create(newEntList_ent_module)

def justice_judge_new_count_predict(file_path,model_path):
    try:
        data_matrix = pd.read_csv(file_path, sep=',')
    except:
        data_matrix = pd.read_csv(file_path, sep=',',encoding='gbk')

    data_matrix['judge_new_count'] = np.zeros(len(data_matrix), dtype=int)
    data_matrix_count = data_matrix.groupby('entname').count().reset_index()

    ent_model_path = model_path + '/ent/ent_module_mark.m'
    ent_inner_model_path = model_path + '/ent/ent_inner_C15.m'
    ent_risk_model_path = model_path + '/risk/risk_module_mark.m'
    model_path = model_path + '/risk/justice_judge_new-judge_new_count.m'
    model = load_model(model_path)
    ent_model = load_model(ent_model_path)
    ent_inner_model = load_model(ent_inner_model_path)
    ent_risk_model = load_model(ent_risk_model_path)

    newEntList = []
    newEntList_p = []
    newEntList_risk_module = []
    newEntList_ent_module = []

    count = 0
    count_p = 0
    count_risk_module = 0
    count_ent_module = 0

    for row in tqdm(data_matrix.iterrows()):
        entname = row[1]['entname']
        time = row[1]['time']
        title = row[1]['title']
        casetype = row[1]['casetype']
        judgeresult = row[1]['judgeresult']
        casecause = row[1]['casecause']
        evidence = row[1]['evidence']
        courtrank = row[1]['courtrank']
        datatype = row[1]['datatype']
        latypes = row[1]['latypes']

        newEnt = JusticeJudgeNew(entname=entname, time=time, title=title, casetype=casetype,
                                judgeresult=judgeresult,casecause=casecause,evidence=evidence,
                                 courtrank=courtrank,datatype=datatype,latypes=latypes)
        newEntList.append(newEnt)
        count += 1

        if count / 5000 == 1:
            JusticeJudgeNew.objects.bulk_create(newEntList)
            newEntList = []
            count = 0
    JusticeJudgeNew.objects.bulk_create(newEntList)

    for row in tqdm(data_matrix_count.iterrows()):
        entname = row[1]['entname']
        judge_new_count = row[1]['judge_new_count']

        oldEnt = JusticeJudgeNewCount.objects.filter(entname__exact=entname)
        oldEnt_risk_module = RiskModule.objects.filter(entname__exact=entname)
        oldEnt_ent_module = EntModule.objects.filter(entname__exact=entname)

        judge_new_count_type = 0
        if len(oldEnt):
            oldEnt[0].judge_new_count += judge_new_count
            oldEnt[0].judge_new_count_type = predict(np.array(oldEnt[0].judge_new_count), model)[0]
            oldEnt[0].save()

        else:
            judge_new_count = judge_new_count
            judge_new_count_type = predict(np.array(judge_new_count), model)[0]
            newEnt_p = JusticeJudgeNewCount(entname=entname, judge_new_count=judge_new_count,
                                   judge_new_count_type=judge_new_count_type)
            newEntList_p.append(newEnt_p)
            count_p += 1

            if count_p / 5000 == 1:
                JusticeJudgeNewCount.objects.bulk_create(newEntList_p)
                newEntList_p = []
                count_p = 0

        # risk_module
        risk_module_type = 0

        if len(oldEnt_risk_module):
            oldEnt_risk_module[0].judge_new_count_type = judge_new_count_type
            ent_risk_module_mark = get_module_mark(oldEnt_risk_module[0], risk_weight_dict)
            oldEnt_risk_module[0].risk_module = ent_risk_module_mark
            risk_module_type = predict(ent_risk_module_mark, model=ent_risk_model)
            oldEnt_risk_module[0].risk_module_type = risk_module_type
            # 不再需要inner_type

            oldEnt_risk_module[0].save()

        else:
            new_risk_module = RiskModule(entname=entname, judge_new_count_type=judge_new_count_type)
            ent_risk_module_mark = get_module_mark(new_risk_module, risk_weight_dict)
            new_risk_module.risk_module = ent_risk_module_mark
            risk_module_type = predict(ent_risk_module_mark, model=ent_risk_model)
            new_risk_module.risk_module_type = risk_module_type

            newEntList_risk_module.append(new_risk_module)
            count_risk_module += 1

            if count_risk_module / 5000 == 1:
                RiskModule.objects.bulk_create(newEntList_risk_module)
                newEntList_risk_module = []
                count_risk_module = 0

        # ent_module
        if len(oldEnt_ent_module):
            oldEnt_ent_module[0].risk_module_type = risk_module_type
            ent_mark = get_module_mark(oldEnt_ent_module[0], ent_weight_dict)
            oldEnt_ent_module[0].ent = ent_mark

            oldEnt_ent_module[0].ent_type = predict(ent_mark, model=ent_model)
            ent_type_list = get_ent_module_type_list(entmodule=oldEnt_ent_module[0], weight_dict=ent_weight_dict)
            oldEnt_ent_module[0].ent_inner_type = inner_predict(ent_type_list, ent_inner_model)

            oldEnt_ent_module[0].save()
        else:
            newEntModule = EntModule(entname=entname, risk_module_type=0)
            ent_mark = get_module_mark(newEntModule, ent_weight_dict)
            newEntModule.ent = ent_mark
            newEntModule.ent_type = predict(ent_mark, model=ent_model)
            ent_type_list = get_ent_module_type_list(entmodule=newEntModule, weight_dict=ent_weight_dict)
            newEntModule.ent_inner_type = inner_predict(ent_type_list, ent_inner_model)

            newEntList_ent_module.append(newEntModule)
            count_ent_module += 1

            if count_ent_module / 5000 == 1:
                EntModule.objects.bulk_create(newEntList_ent_module)
                newEntList_ent_module = []
                count_ent_module = 0

    JusticeJudgeNewCount.objects.bulk_create(newEntList_p)
    RiskModule.objects.bulk_create(newEntList_risk_module)
    EntModule.objects.bulk_create(newEntList_ent_module)


def justice_credit_aic_predict(file_path,model_path):
    data_matrix = pd.read_csv(file_path, sep=',')

    ent_model_path = model_path + '/ent/ent_module_mark.m'
    ent_inner_model_path = model_path + '/ent/ent_inner_C15.m'
    ent_risk_model_path = model_path + '/risk/risk_module_mark.m'
    model_path = model_path + '/risk/justice_credit_aic-is_justice_creditaic.m'
    model = load_model(model_path)
    ent_model = load_model(ent_model_path)
    ent_inner_model = load_model(ent_inner_model_path)
    ent_risk_model = load_model(ent_risk_model_path)

    newEntList = []
    newEntList_risk_module = []
    newEntList_ent_module = []

    count = 0
    count_risk_module = 0
    count_ent_module = 0

    for row in tqdm(data_matrix.iterrows()):
        entname = row[1]['entname']
        is_justice_creditaic = row[1]['is_justice_creditaic']

        oldEnt = JusticeCreditAic.objects.filter(entname__exact=entname)
        oldEnt_risk_module = RiskModule.objects.filter(entname__exact=entname)
        oldEnt_ent_module = EntModule.objects.filter(entname__exact=entname)

        is_justice_creditaic_type = 0
        if len(oldEnt):
            oldEnt[0].is_justice_creditaic += is_justice_creditaic
            is_justice_creditaic_type = predict(np.array(oldEnt[0].is_justice_creditaic), model)[0]
            oldEnt[0].is_justice_creditaic_type = is_justice_creditaic_type
            oldEnt[0].save()

        else:
            is_justice_creditaic_type = predict(np.array(is_justice_creditaic), model)[0]
            newEnt = JusticeCreditAic(entname=entname, is_justice_creditaic=is_justice_creditaic,
                                   is_justice_creditaic_type=is_justice_creditaic_type)
            newEntList.append(newEnt)
            count += 1

            if count / 5000 == 1:
                JusticeCreditAic.objects.bulk_create(newEntList)
                newEntList = []
                count = 0

        # risk_module
        risk_module_type = 0

        if len(oldEnt_risk_module):
            oldEnt_risk_module[0].is_justice_creditaic_type = is_justice_creditaic_type
            ent_risk_module_mark = get_module_mark(oldEnt_risk_module[0], risk_weight_dict)
            oldEnt_risk_module[0].risk_module = ent_risk_module_mark
            risk_module_type = predict(ent_risk_module_mark, model=ent_risk_model)
            oldEnt_risk_module[0].risk_module_type = risk_module_type
            # 不再需要inner_type

            oldEnt_risk_module[0].save()

        else:
            new_risk_module = RiskModule(entname=entname, is_justice_creditaic_type=is_justice_creditaic_type)
            ent_risk_module_mark = get_module_mark(new_risk_module, risk_weight_dict)
            new_risk_module.risk_module = ent_risk_module_mark
            risk_module_type = predict(ent_risk_module_mark, model=ent_risk_model)
            new_risk_module.risk_module_type = risk_module_type

            newEntList_risk_module.append(new_risk_module)
            count_risk_module += 1

            if count_risk_module / 5000 == 1:
                RiskModule.objects.bulk_create(newEntList_risk_module)
                newEntList_risk_module = []
                count_risk_module = 0

        # ent_module
        if len(oldEnt_ent_module):
            oldEnt_ent_module[0].risk_module_type = risk_module_type
            ent_mark = get_module_mark(oldEnt_ent_module[0], ent_weight_dict)
            oldEnt_ent_module[0].ent = ent_mark

            oldEnt_ent_module[0].ent_type = predict(ent_mark, model=ent_model)
            ent_type_list = get_ent_module_type_list(entmodule=oldEnt_ent_module[0], weight_dict=ent_weight_dict)
            oldEnt_ent_module[0].ent_inner_type = inner_predict(ent_type_list, ent_inner_model)

            oldEnt_ent_module[0].save()
        else:
            newEntModule = EntModule(entname=entname, risk_module_type=0)
            ent_mark = get_module_mark(newEntModule, ent_weight_dict)
            newEntModule.ent = ent_mark
            newEntModule.ent_type = predict(ent_mark, model=ent_model)
            ent_type_list = get_ent_module_type_list(entmodule=newEntModule, weight_dict=ent_weight_dict)
            newEntModule.ent_inner_type = inner_predict(ent_type_list, ent_inner_model)

            newEntList_ent_module.append(newEntModule)
            count_ent_module += 1

            if count_ent_module / 5000 == 1:
                EntModule.objects.bulk_create(newEntList_ent_module)
                newEntList_ent_module = []
                count_ent_module = 0

    JusticeCreditAic.objects.bulk_create(newEntList)
    RiskModule.objects.bulk_create(newEntList_risk_module)
    EntModule.objects.bulk_create(newEntList_ent_module)





def predict_all(file_list,model):
    for f in file_list:
        print(f)
        filename = f.split('/')[-1].split('.')[0]
        if filename == 'trademark_infoa' or filename == 'trademark_infob':
            fun_str = filename[:-1] + '_predict'
            print(fun_str)

        elif filename == 'justice_judge_new' :
            fun_str = filename + '_count_predict'

        elif filename == 'change_info' or filename == 'ent_guarantee':
            fun_str = filename + '_update'
            eval(fun_str)(f)
            continue

        elif filename == 'recruit_qcwy' or filename == 'recruit_zhyc' or filename == 'recruit_zlzp':
            fun_str = 'recruit_predict'

        else:
            fun_str = filename + '_predict'
        print(fun_str+"-----------------------------------------------------")
        eval(fun_str)(f,model)



import os



def get_full_filename(dirname):
    pathname = []

    filelist = os.listdir(dirname)

    for f in filelist:
        pathname.append(dirname+'/'+f)

    return pathname



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



def dbpredict(request):
    if request.method == 'POST':



        start = time.time()

        del_file('data/tmp')
        del_file('data/dbpredict')
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
        dest_dir = 'data/dbpredict'

        un_zip(file_name, dest_dir)

        dirname = 'data/dbpredict'
        filelist = get_full_filename(dirname)
        model = 'train/env/default_model_doc'
        predict_all(filelist,model)

        end = time.time()

        res = {}
        res['msg'] = 'ok'
        res['time'] = end-start
        return JsonResponse(res)





