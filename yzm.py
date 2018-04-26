# -*- coding: utf-8 -*-
"""
Created on Thu Apr 26 16:51:54 2018
破解验证码
@author: ZJKfly
"""
from PIL import Image
import hashlib
import time
import random
import math
import os
class VectorCompare:
    #计算矢量大小
    def magnitude(self,concordance):
        total = 0
        for word,count in concordance.items():
            total += count ** 2
        return math.sqrt(total)

    #计算矢量之间的 cos 值
    def relation(self,concordance1, concordance2):
        topvalue = 0
        for word, count in concordance1.items():
            if word in concordance2:
                topvalue += count * concordance2[word]
        return topvalue / (self.magnitude(concordance1) * self.magnitude(concordance2))
im = Image.open("l9pelg.gif")
#(将图片转换为8位像素模式)
im.convert("P")

his = im.histogram()
#打印颜色直方图
print(his)
#寻找前10的颜色数目
values ={}
#将像素点给values字典
for i in range(255):
    values[i] = his[i]
    
#求出字典的前10的像素值
for j,k in sorted(values.items(),key= lambda x:x[1],reverse = True)[:10]:
    print(j,k)
    
    
#画出一个白板
im2 = Image.new("P",im.size,255) 

#将红点或者灰点（212.220）画到白板上面
for x in range(im.size[1]):
    for y in range(im.size[0]):
        pix = im.getpixel((y,x))
        if pix == 220 or pix == 227:
            im2.putpixel((y,x),0)         
#im2.show()   

#分割成n等分的图片，并保存在 (纵向切割)
inletter = False
foundletter=False
start = 0
end = 0
letters = []

for x in range(im.size[0]):
    for y in range(im2.size[1]):
        if im2.getpixel((x,y)) == 0:
            inletter = True
    if foundletter == False and inletter == True:
    
        foundletter = True
        start = x
    
    if foundletter == True and inletter == False:
        foundletter = False
        end = x
        letters.append((start,end))
            
    inletter=False
 

#吧切割后的图片赋值给某一个文件夹下
'''
count = 0
for letter in letters:
    im3 = im2.crop(( letter[0] , 0, letter[1],im2.size[1] ))
    m = random.randint(0,1111)
    im3.save("./%s.gif"%(m))
    count += 1
'''    
#图片矢量化
def buildvector(im):
    d1 = {}
    count = 0
    for i in im.getdata():
        d1[count] = i
        count += 1
    return d1

#新建向量操作类
v = VectorCompare()

#加载训练集合      
iconset = ['0','1','2','3','4','5','6','7','8','9','0','a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']

#加载训练集
imageset = []
for letter in iconset:
    for img in os.listdir('./iconset/%s/'%(letter)):
        temp = []
        if img != "Thumbs.db" and img != ".DS_Store":
            temp.append(buildvector(Image.open("./iconset/%s/%s"%(letter,img))))
        imageset.append({letter:temp})
#print(imageset)

count = 0
#对验证码图片进行切割
for letter in letters:
    im3 = im2.crop(( letter[0] , 0, letter[1],im2.size[1] ))

    guess = []
    '''
    for image in imageset:
        for x,y in image.():
            print(x)
    '''

    for image in imageset:
        for x,y in image.items():
            if len(y) != 0:
                guess.append( ( v.relation(y[0],buildvector(im3)),x) )

    guess.sort(reverse=True)
    print(guess[0])
    count += 1
        





     
            
