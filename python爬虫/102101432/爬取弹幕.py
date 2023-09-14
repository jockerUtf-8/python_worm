
import time
from selenium import webdriver#selenium的浏览器真实模拟器
from selenium.webdriver.common.by import By
import requests#request请求方便快捷
import re#正则表达式
import wordcloud#词云专属包
import jieba#处理文字专用包
if __name__ == '__main__':
    Link = []#记录300个视频的url
    count = 0
    proxy = {'http': '182.34.102.153:9999'}#我爬虫的次数太多了，ip被B站列入了黑名单,只能请求代理
    headers = {'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Mobile Safari/537.36'}
    # 搜索关键词后第一页的网页地址
    url = ['https://search.bilibili.com/all?keyword=%E6%97%A5%E6%9C%AC%E6%A0%B8%E6%B1%A1%E6%B0%B4%E6%8E%92%E6%B5%B7']
    for i in range(14):  # 每页是24个视频，至少要打开14页才能爬取到300个视频
        if (i > 0): url.append(url[0] + '&page=' + str(i + 1) + '&o=' + str(24 * i))  # 第二页以后每页地址的规律格式
    driver = webdriver.Chrome()
    for i in range(14):
        driver.get(url[i])
        time.sleep(1)  # 需要等待1秒，不然会因页面点击太快而出错
        if (i == 0):
            for j in range(24):
                response = driver.find_element(By.XPATH,'/html/body/div[3]/div/div[2]/div[2]/div/div/div/div[2]/div/div[' + str(j + 1) + ']/div/div[2]/a')  # 第一页中所有视频url的xpath规律格式
                link = response.get_attribute('href')  # 获取当前视频的url
                link = link.replace('bilibili', 'ibilibili')  # 弹幕信息在ibilibili的地址中
                Link.append(link)  # 收集url
                count += 1
        else:
            for j in range(24):  # 同第一页的代码同理,只是xpath的格式不同
                response = driver.find_element(By.XPATH,'/html/body/div[3]/div/div[2]/div[2]/div/div/div[1]/div[' + str(j + 1) + ']/div/div[2]/a')
                link = response.get_attribute('href')
                # response.click()
                link = link.replace('bilibili', 'ibilibili')
                Link.append(link)
                count += 1
                if (count > 300):  # 当获取的url达到300个时结束循环
                    break
    for i in range(300):
        response=requests.get(url=Link[i],headers=headers,proxies=proxy)#获取视频信息
        content = response.text#获取信息文本
        pattern = r'cid":"\d+"'#弹幕地址存储在信息文本中的cid中
        match = re.search(pattern, content)#以上述模式寻找信息
        cid=match.group()#group为匹配到的目标字符串
        cid=cid.lstrip('cid":"')
        cid=cid.rstrip('"')#去除边角
        url='https://api.bilibili.com/x/v1/dm/list.so?oid='+cid#拼凑出弹幕的地址
        print(url)
        response=requests.get(url=url,headers=headers)#请求弹幕内容
        response.encoding='utf-8'
        contentList=re.findall('<d p=".*?">(.*?)</d>',response.text)#提取有效信息
        for content in contentList:#写入弹幕.txt
            with open('弹幕.txt','a',encoding='utf-8')as fp:
                fp.write(content)
                fp.write('\n')
