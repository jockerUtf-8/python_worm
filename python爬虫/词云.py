# _*_ coding : utf-8 _*_
# @Time : 2023/9/13 16:12
# @Author : 林展平
# @File : 词云.py
# @Project : Desktop、
import wordcloud
import jieba
f=open('B站弹幕.txt',encoding='utf-8')
txt=f.read()
string=' '.join(jieba.lcut(txt))
print(type(string))
wc=wordcloud.WordCloud(
    width=700,#宽和高各700
    height=700,
    background_color='white',#背景白色
    scale=15,#规模
    font_path='STXINWEI.TTF'#字体
)
wc.generate(string)
wc.to_file('弹幕词云.png')
