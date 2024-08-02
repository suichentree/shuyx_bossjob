import sys

import requests
import time
import json
import random
from db.sql_utils import createTable,insert_list_data
from loguru import logger

def job_josn(cookies,query,city,page,pageSize):
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36 Edg/125.0.0.0',
    }
    params = {
        'scene': '1',
        'query': query,
        'city': city,
        'experience': '',
        'payType': '',
        'partTime': '',
        'degree': '',
        'industry': '',
        'scale': '',
        'stage': '',
        'position': '',
        'jobType': '',
        'salary': '',
        'multiBusinessDistrict': '',
        'multiSubway': '',
        'page': page,
        'pageSize': pageSize,
    }
    logger.info(f"开始调用joblist.json接口,请求params = {params} ")
    response = requests.get('https://www.zhipin.com/wapi/zpgeek/search/joblist.json', params=params, cookies=cookies,headers=headers).text
    response_dict_info = json.loads(response)
    return response_dict_info

# 起始
if __name__ == "__main__":
    # 创建表（若表存在，无动作）
    createTable()

    # cookies
    cookies = {
        '__zp_stoken__': '013dfw413BgUzBA8aVQXCv1jCvWdiwq5uUUNqwrBDwrBpTcKewr7CvMOMwqxoWGZNasOMwrfCgsKxwo1Ww77CpMKiXsKVwqPDtcKlwpHCp8KvwrjCnsSRxIrDksWuxLZGwr7CkDI8AQQOAQMYBRsYBhgFBA8NHBkHHBoBBA4BAzQ5wqXCrDQxNzQtRlhFAllVak5VTQ9UTUE%2FMQMbXlUxJT40Pz3DiMK%2BwrA3wrbCv8KyTMOIwr3CswY0Nz0%2FwrMSJC%2FCssSJI8Kyw54gJiDCsiUDwr7DiwPDjVXCrMOfw69%2FPDQ%2Bwr%2FEvjYzEjU0MjU9MjUyMyIyAsOPaMKWw5TDrcKKIzQSTDIzNjQ0MjNIMjYuMzVMLjI%2BJDYCBAYNGiM1wrLCs8K%2Fw5cyMw%3D%3D; __c=1722474195'    }
    # 搜索内容
    query = "java"
    # 目标城市 101280100是广州
    city = "101280100"

    # 初始页码，初始循环条件
    page = 9
    isContinue = True
    while isContinue:
        # 随机休眠10-20秒后运行，防止频繁调用
        sleep_time = random.randrange(10, 20)
        logger.info(f"休眠 {sleep_time} 秒")
        time.sleep(sleep_time)
        # 调用joblist.json接口，获取职位信息
        job_info = job_josn(cookies,query,city,page,30)
        # 是否有更多职位数据
        hasMore = False

        if job_info['code'] != 0:
            logger.error(f"调用joblist.json接口失败。job_info = {job_info}")
            sys.exit()
        else:
            logger.success(f"调用joblist.json接口成功。job_info = {job_info}")
            hasMore = job_info["zpData"]["hasMore"]

            # 职位信息数据
            jobList = job_info["zpData"]["jobList"]
            job_data_list = []
            for job in jobList:
                ## jobName 职位名称,cityName 职位所在城市,areaDistrict 职位所在地区,businessDistrict 职位所在地点,jobDegree 职位所需学位,jobExperience 职位所需经验,skills 职位所需技能,
                ## salaryDesc 职位薪酬,jobValidStatus 职位有效状态,brandName 公司品牌名称,brandScaleName 公司规模人数,brandIndustry 公司所在行业
                job_dict = {"jobName":job['jobName'],"cityName":job['cityName'],"areaDistrict":job['areaDistrict'],
                            "businessDistrict":job['businessDistrict'],"jobDegree":job['jobDegree'],"jobExperience":job['jobExperience'],
                            "skills":str(job['skills']),"salaryDesc":job['salaryDesc'],"jobValidStatus":job['jobValidStatus']
                            ,"brandName":job['brandName'],"brandScaleName":job['brandScaleName'],"brandIndustry":job['brandIndustry']}
                job_data_list.append(job_dict)
            # 插入数据到表中
            insert_list_data(job_data_list)

        # 判断是否有更多职位数据
        if hasMore:
            page = page + 1
        else:
            isContinue = False
