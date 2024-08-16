from tinydb import TinyDB, Query
import json

# 创建数据库  db.json
db = TinyDB('db.json',encoding='utf-8')
# 创建表
table = db.table('t_user')

if __name__ == '__main__':

    # 清空表中数据
    table.truncate()
    # 用户数据
    userlist = [{'name': '小明11', 'pwd': 'a123456', 'idCard': 'XXXXXXX',
                 'remark': '焊接与热切割作业111'},
                {'name': '小明12', 'pwd': 'a123456', 'idCard': 'XXXXXXX',
                 'remark': '焊接与热切割作业222'}
                ]
    # 插入数据
    for user in userlist:
        table.insert(user)

    # 关闭数据库以确保所有数据写入文件
    db.close()


    # 读取 TinyDB 数据库文件
    with open('db.json', 'r', encoding='utf-8') as file:
        data = json.load(file)

    # 写回 JSON 文件，确保中文不被转义
    with open('db.json', 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)