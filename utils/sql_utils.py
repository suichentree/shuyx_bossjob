# 定义用户类
import sqlite3
import os


# 将查询结果从元组转换为字典
def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

# 获取当前脚本所在的目录
current_path = os.path.dirname(os.path.abspath(__file__))
# 获取当前脚本所在的项目根目录
root_path = os.path.dirname(current_path)

# 数据库文件所在的路径
db_path = 'boss_job_data.db'

# 初始化表
def init_table():
    # 先删除表
    dropTable()
    # 后创建表
    createTable()

# 删除数据库
def dropTable():
    sql = "DROP TABLE IF EXISTS t_job_info;"
    excute_sql(sql)

# 判断表是否存在
def isExistTable(tableName):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    sql = f"SELECT name FROM sqlite_master WHERE type='table' AND name='{tableName}';"
    results = cursor.execute(sql).fetchall()
    if len(results) == 0:
        return False
    else:
        return True

# 创建数据库
def createTable():
    # 判断表是否存在，若存在则不创建
    if not isExistTable('t_job_info'):
        # 创建表
        sql = """CREATE TABLE IF NOT EXISTS t_job_info(
                                id INTEGER PRIMARY KEY AUTOINCREMENT,   --id编号，自增长
                                jobName TEXT NOT NULL,                  --职位名称
                                cityName TEXT NOT NULL,                 --职位所在城市
                                areaDistrict TEXT NOT NULL,             --职位所在地区
                                businessDistrict TEXT NOT NULL,         --职位所在地点
                                jobDegree TEXT NOT NULL,                --职位所需学位
                                jobExperience TEXT NOT NULL,            --职位所需经验
                                skills TEXT NOT NULL,                   --职位所需技能
                                salaryDesc TEXT NOT NULL,               --职位薪酬
                                jobValidStatus TEXT NOT NULL,           --职位有效状态
                                brandName TEXT NOT NULL,                --公司品牌名称
                                brandScaleName TEXT NOT NULL,           --公司规模人数
                                brandIndustry TEXT NOT NULL,            --公司所在行业
                                createTime DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP --创建时间
                                );"""
        excute_sql(sql)

# 执行查询语句
def excute_select_sql(sql):
    # 创建sqlite3的数据库连接
    conn = sqlite3.connect(db_path)
    conn.row_factory = dict_factory
    cursor = conn.cursor()
    results = cursor.execute(sql)
    return results.fetchall()

# 执行非查询语句
def excute_sql(sql):
    conn = sqlite3.connect(db_path)
    conn.row_factory = dict_factory
    cursor = conn.cursor()
    cursor.execute(sql)
    # 提交数据库
    conn.commit()
    # 关闭游标对象
    cursor.close()
    # 关闭数据库连接
    conn.close()

# 批量插入数据
def insert_list_data(list_data):
    conn = sqlite3.connect(db_path)
    conn.row_factory = dict_factory
    cursor = conn.cursor()
    for obj in list_data:
        info = (obj['jobName'],obj['cityName'], obj['areaDistrict'], obj['businessDistrict'], obj['jobDegree'], obj['jobExperience'],
                obj['skills'], obj['salaryDesc'], obj['jobValidStatus'], obj['brandName'], obj['brandScaleName'],obj['brandIndustry'])

        sql = """INSERT INTO t_job_info(jobName,cityName,areaDistrict,businessDistrict,jobDegree,jobExperience,
                    skills,salaryDesc,jobValidStatus,brandName,brandScaleName,brandIndustry) 
                    VALUES(?,?,?,?,?,?,?,?,?,?,?,?);"""
        # 执行SQL语句
        cursor.execute(sql, info)
        # 提交数据库
        conn.commit()

    # 关闭游标对象
    cursor.close()
    # 关闭数据库连接
    conn.close()

# 查询全部
def select_all():
    sql = "SELECT * FROM t_job_info"
    return excute_select_sql(sql)

