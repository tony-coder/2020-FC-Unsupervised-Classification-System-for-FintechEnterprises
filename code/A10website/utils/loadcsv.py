import csv
import os

import mysql.connector
from tqdm import tqdm


def getConnection(user,password,host,port,database):
    connection = mysql.connector.connect(user=user,password=password,host=host,port=port,database=database)
    return connection
#
# user = 'root'
# password = 'Ck123456!'
# host = '127.0.0.1'
# port = 3306
# database = 'entdb_bak'
# con =  getConnection(user,password,host,port,database)
# cursor = con.cursor()
# # cursor.execute('select * from mydf')
# # result = cursor.fetchall()
# read = csv.reader(open('C:/Users/1/Desktop/mydb.csv'))
# count = 0
# datas = []
# for line in read:
#     if count == 0:
#         count += 1
#         continue
#     sql_insert = "insert into mydf (username,password) VALUES(%s,%s) ON DUPLICATE KEY UPDATE password = values(password)"
#     data = (username, password)
#     datas.append(data)
#     count += 1
#     if count / 200000 == 1:
#         cursor.executemany(sql_insert, datas)
#         con.commit()
#         count = 0
#         datas = []
# cursor.executemany(sql_insert, datas)
# con.commit()
# cursor.close()
# con.close()
def get_files(dirname):
    files = os.listdir(dirname)  # 得到文件夹下的所有文件名称
    s = []
    for file in files:  # 遍历文件夹
        if not os.path.isdir(file):  # 判断是否是文件夹，不是文件夹才打开
            f = open(dirname + "\\" + file);  # 打开文件
            iter_f = iter(f);  # 创建迭代器
            str = ""
            for line in iter_f:  # 遍历文件，一行行遍历，读取文本
                str = str + line
            s.append(str)  # 每个文件的文本存到list中
    print(s)

def EnumPathFiles(path, callback):
    if not os.path.isdir(path):
        print('Error:"',path,'" is not a directory or does not exist.')
        return
    list_dirs = os.walk(path)

    filenames = []
    for root, dirs, files in list_dirs:
        for d in dirs:
            EnumPathFiles(os.path.join(root, d), callback)
        for f in files:
            filename = callback(root, f)
            filenames.append(filename)

    return filenames

def callback1(path, filename):
    return path+'\\'+filename


def read_lines(filename):
    lines = []
    with open(filename,encoding='UTF-8') as file:
        lines = file.readlines()
        count = len(lines)

        if count > 0:
            del lines[0]
    return lines

def line_to_sql(lines,sql):
    user = 'root'
    password = 'Ck123456!'
    host = '127.0.0.1'
    port = 3306
    database = 'entdb_bak'
    con = getConnection(user,password,host,port,database)
    cursor = con.cursor()
    datas = []
    count = 0
    for line in tqdm(lines):

        data = tuple(line.split(","))
        datas.append(data)
        count += 1
        if count / 10000 == 1:
            cursor.executemany(sql, datas)
            con.commit()
            count = 0
            datas = []

    cursor.executemany(sql, datas)
    con.commit()
    cursor.close()
    con.close()


# lines = read_lines('D:/学习/A10/docs/数据集合打包/数据集合打包/7-基本/test.csv')
#
sql = "insert into company_baseinfo_summary (entname,regcap,empnum,estdate,candate,revdate,entstatus,opto," \
      "enttype,entcat,industryphy,regcapcur,industryco,opfrom,regcap_type,company_baseinfo_module,company_baseinfo_module_type) " \
      "VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) " \
      "ON DUPLICATE KEY UPDATE regcap = values(regcap),empnum = values(empnum),estdate = values(estdate),candate = values(candate)," \
      "revdate = values(revdate),entstatus = values(entstatus),opto = values(opto),enttype = values(enttype),entcat = values(entcat)," \
      "industryphy = values(industryphy),regcapcur = values(regcapcur),industryco = values(industryco),opfrom = values(opfrom),regcap_type = values(regcap_type)," \
      "company_baseinfo_module = values(company_baseinfo_module),company_baseinfo_module_type = values(company_baseinfo_module_type)"
#
#
# line_to_sql(lines,sql)

# files = get_files('D:\\学习\\A10\\docs\\数据集合打包\\数据集合打包')
# print(files)

sql_administrative_punishmen = '''
insert into administrative_punishment (entname, is_punish, is_punish_type) VALUES(%s,%s,%s)
ON DUPLICATE KEY UPDATE is_punish = values(is_punish),is_punish_type = values(is_punish_type)
'''


sql_brand_module = '''
insert into administrative_punishment (entname, is_jnsn_type, level_rank_type, passpercent_type,
is_infoa_type,is_infob_type,brand_module,brand_module_type,brand_module_inner_type)
VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s) 
ON DUPLICATE KEY UPDATE is_jnsn_type = values(is_jnsn_type),level_rank_type = values(level_rank_type),
passpercent_type = values(passpercent_type),is_infoa_type = values(is_infoa_type),is_infob_type = values(is_infob_type)
brand_module = values(brand_module),brand_module_type = values(brand_module_type),brand_module_inner_type = values(brand_module_inner_type)
'''



sql_administrative_punishment = ''
sql_administrative_punishment = ''
sql_administrative_punishment = ''
sql_administrative_punishment = ''
sql_administrative_punishment = ''
sql_administrative_punishment = ''
sql_administrative_punishment = ''
sql_administrative_punishment = ''
sql_administrative_punishment = ''
sql_administrative_punishment = ''
sql_administrative_punishment = ''
sql_administrative_punishment = ''
sql_administrative_punishment = ''
sql_administrative_punishment = ''
sql_administrative_punishment = ''
sql_administrative_punishment = ''
sql_administrative_punishment = ''
sql_administrative_punishment = ''










filelist = EnumPathFiles('D:\\学习\\A10\\docs\\数据集合打包\\数据集合打包',callback1)
print(filelist)
