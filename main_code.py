import sys
import requests
import json
from loguru import logger

def getSession():
    mySession = requests.Session()
    mySession.headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36 Edg/125.0.0.0'}
    return requests.Session()

def toStart(mySession):
    # 访问首页
    mySession.get("https://www.zhipin.com/guangzhou/?seoRefer=index")
    # 打印mySession中的cookie值
    print(requests.utils.dict_from_cookiejar(mySession.cookies))

def job_josn(mySession,query,city,page):
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
        'pageSize': 30,
    }
    logger.info(f"开始调用joblist.json接口,查询内容：{query},查询城市：{city}，页码：{page}")
    response = mySession.get('https://www.zhipin.com/wapi/zpgeek/search/joblist.json', params=params)
    response_dict_info = json.loads(response.text)
    # 打印mySession中的cookie值
    print(requests.utils.dict_from_cookiejar(mySession.cookies))
    return response_dict_info


# 起始
if __name__ == "__main__":
    # 获取会话session
    mySession = getSession()
    # 请求boss直聘首页
    toStart(mySession)

    # 搜索请求
    # 搜索内容
    query = "爬虫"
    # 目标城市 101280100是广州
    city = "101280100"

    # 调用joblist.json接口，获取职位信息
    job_info = job_josn(mySession,query,city,1)
    print(job_info)
    # 程序结束运行
    sys.exit()


    # 初始页码，初始循环条件
    page = 1
    isContinue = True
    while isContinue:
        # 随机休眠10-20秒后运行，防止频繁调用
        sleep_time = random.randrange(10, 20)
        logger.info(f"休眠 {sleep_time} 秒")
        time.sleep(sleep_time)
        # 调用joblist.json接口，获取职位信息
        job_info = job_josn(query,city,page,30)
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
