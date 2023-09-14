# _*_ coding : utf-8 _*_
# @Time : 2023/9/11 23:38
# @Author : 林展平
# @File : cxk
# @Project : Desktop、
# 创建一个Chrome浏览器实例
import re#导入正则模块
with open('弹幕.txt','r',encoding='utf-8')as fp:
    lines=fp.readlines()#逐行读取文件
lineCount={}#建立空字典
for line in lines:#统计弹幕数
    if line not in lineCount:#如果不在字典中,就创建新的数据
        lineCount[line]=1
    else:
        lineCount[line]+=1#在字典中，就让次数加一
sortedDict = sorted(lineCount.items(),key=lambda x:x[1],reverse=True)#对字典进行降序排序
for i in range(len(sortedDict)):
    danmu=str(sortedDict[i])
    danmu=re.sub(r'[^\w\s,]','',danmu)
    danmu=danmu.replace('n, ',':')#对字典中的元素规范化之后再写入文件
    with open('B站弹幕.txt', 'a', encoding='utf-8') as fp:
        fp.write(danmu)
        fp.write('\n')


