
from Module_management import generate_password_hash
import pickle

# USERS_DATA = [
#     {
#         "id": 10000,

#         "姓名": 'ccelend',
#         "性别": '男',
#         "出生年月": '20011010',
#         "学历": '本科',
#         "职务": '经理',
#         "住址": '吉林省',
#         "电话": '111111',

#         "username": 'admin',
#         "password": generate_password_hash('admin')
#     },
#     {
#         "id": 10001,

#         "姓名": '123',
#         "性别": '女',
#         "出生年月": '20001111',
#         "学历": '高中',
#         "职务": '员工',
#         "住址": '黑龙江',
#         "电话": '222222',

#         "username": 'user',
#         "password": generate_password_hash('user')
#     },
#     {
#         "id": 10002,

#         "姓名": '456',
#         "性别": '男',
#         "出生年月": '19991211',
#         "学历": '本科',
#         "职务": '员工',
#         "住址": '吉林省',
#         "电话": '333333',

#         "username": 'user1',
#         "password": generate_password_hash('user1')
#     },
#     {
#         "id": 10003,

#         "姓名": '789',
#         "性别": '女',
#         "出生年月": '20020310',
#         "学历": '博士',
#         "职务": '主管',
#         "住址": '上海',
#         "电话": '444444',

#         "username": 'user2',
#         "password": generate_password_hash('user2')
#     }
# ]

# 将对象序列化成二进制对象，并写入data文件
def write_data():
    global USERS_DATA
    with open("data.pickle", "wb") as f:
        pickle.dump(USERS_DATA, f)

USERS_DATA = []
#读取指定的序列化数据文件，并返回用户信息对象-列表
def read_data():
    global USERS_DATA
    with open("data.pickle", "rb") as f:
        USERS_DATA = pickle.load(f)
