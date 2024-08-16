from DrissionPage import ChromiumPage, ChromiumOptions
from loguru import logger
import time
import threading

def getPage():
    path = r'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe'  # 浏览器的可执行文件路径
    # 设置无头模式
    # co = ChromiumOptions().headless()
    co = ChromiumOptions()

    # 设置浏览器路径
    co.set_browser_path(path)

    # 来宾模式
    co.set_argument('--guest')

    # 无痕模式
    co.incognito()

    # 设置初始窗口大小
    co.set_argument('--window-size', '500,900')

    # 阻止“自动保存密码”的提示气泡
    # co.set_pref('credentials_enable_service', False)

    # 阻止“要恢复页面吗？Chrome未正确关闭”的提示气泡
    # co.set_argument('--hide-crash-restore-bubble')

    # 设置浏览器的UA
    co.set_user_agent(user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36 Edg/127.0.0.0')

    # 自动分配端口，从而启动一个全新浏览器
    co.auto_port(True,"C:\\Users\\18271\\Desktop\\temp_data",[9600,19600])

    # 浏览器静音
    co.mute(True)

    # 创建页面对象，并启动或接管浏览器,传入浏览器配置
    page = ChromiumPage(co)

    # 之后出现的弹窗都会自动确认
    page.set.auto_handle_alert()

    return page

def toLoginPage(page):
    # 休眠2秒
    time.sleep(2)
    # 首页
    page.get('https://www.zhipin.com/?ka=header-home-logo')

    logger.info(page.html)




def toListPage(page):
    # 休眠2秒
    time.sleep(2)
    # 跳转网页
    page.get('https://yzya.qsanquan.com/weixin/school/person/project/list')
    # 休眠2秒
    time.sleep(2)
    # 找到href属性为javascript:void(0)的a标签,并进行点击
    page.ele('@@tag()=a@@href=javascript:void(0)').click()
    # 休眠2秒
    time.sleep(2)
    # 爬取该用户进度
    i_tag = page.ele("@class=progress_online_con_bar").child(2)
    # 把用户进度数据插入到数据库中
    user['progress'] = i_tag.text

    return user


# 获取未看完，未学习课件视频的a标签节点
def get_a_tag(page):
    # 休眠2秒
    time.sleep(2)
    # 刷新页面
    page.refresh()
    # 休眠2秒
    time.sleep(2)
    # 等待页面加载完成
    page.wait.doc_loaded()

    # a标签节点
    a_tag = None
    # 休眠2秒
    time.sleep(2)
    # 获取class= class_list class_list2 base_div class_list_scroll 的元素节点。即ui标签
    ui_tags = page.ele("@class=class_list class_list2 base_div class_list_scroll")
    # 获取ui标签的多个子 li标签
    li_tags = ui_tags.children()
    for li_tag in li_tags:
        lis = li_tag.child().children()
        for index, li in enumerate(lis):
            if index != 0:
                if li.child(1).ele("@tag()=a").text == "已完成":
                    continue
                else:
                    # 课程未完成，查询课件情况
                    a_list = li.child(2).children()
                    for a in a_list:
                        if a.ele("@tag()=i").text == "已学习":
                            continue
                        else:
                            a_tag = a
                            return a_tag
    return a_tag

def toWatchVideo(page,user):
    # 循环调用get_a_tag方法，获取未学习，未看完课件视频的a标签节点
    a_tag = get_a_tag(page)
    while a_tag != None:
        video_name = a_tag.ele("@tag()=h3").text
        video_status = a_tag.ele("@tag()=i").text
        # 点击a标签，跳转到该课件视频的播放页面
        a_tag.click(by_js=True)
        # 休眠3秒
        time.sleep(3)
        # 执行页面中的js函数，获取视频的已播放时间，视频时长
        try:
            current_time = int(page.run_js("return player.getCurrentTime()"))
        except:
            logger.warning(
                f"{user['name']} 未找到 player.getCurrentTime() 方法。更换获取当前时间的方式,调用player.getPosition() 方法。")
            current_time = int(page.run_js("return player.getPosition()"))

        duration = int(page.run_js("return player.getDuration()"))
        # 计算出休眠时间。额外加10秒
        sleep_time = duration - current_time + 10
        logger.info(
            f"{user['name']}  课件视频名称 = {video_name} 该课件 {video_status}。课件视频时长为 {duration} , 当前已看时长为 {current_time}。因此开始观看视频,程序开始休眠，休眠时间为{sleep_time}")
        # 执行页面中的js函数，播放视频
        page.run_js("player.play()")
        # 开始休眠
        time.sleep(sleep_time)
        # 再次调用get_a_tag方法，获取未学习，未看完课件视频的a标签节点
        a_tag = get_a_tag(page)


if __name__ == '__main__':
    try:
        # 获取浏览器对象
        page = getPage()
        toLoginPage(page)

    except Exception as e:
        logger.error(f"发生异常，异常信息为 {e} 。")

    logger.info(f"该线程结束运行并关闭浏览器。")

    time.sleep(120)
    # 关闭浏览器
    page.quit()

























