'''
stage I : get all names of photos and save them in files
'''
# import os
# import random
# trainval_percent = 0.1
# train_percent = 0.9
# xmlfilepath = './VOCData/Annotations'  #xml文件存放地址
# if not os.path.exists('./VOCData/ImageSets/'):
#     os.makedirs('./VOCData/ImageSets/')
#
# total_xml = os.listdir(xmlfilepath)
# num = len(total_xml)
# list = range(num)
# tv = int(num * trainval_percent)
# tr = int(tv * train_percent)
# trainval = random.sample(list, tv)
# train = random.sample(trainval, tr)
# ftrainval = open('./VOCData/ImageSets/trainval.txt', 'w')
# ftest = open('./VOCData/ImageSets/test.txt', 'w')
# ftrain = open('./VOCData/ImageSets/train.txt', 'w')
# fval = open('./VOCData/ImageSets/val.txt', 'w')
# for i in list:
#     name = total_xml[i][:-4] + '\n'
#     if i in trainval:
#         ftrainval.write(name)
#         if i in train:
#             ftest.write(name)
#         else:
#             fval.write(name)
#     else:
#         ftrain.write(name)
# ftrainval.close()
# ftrain.close()
# fval.close()
# ftest.close()

'''
stage II : to create test.txt, train.txt and the val.txt
'''


import xml.etree.ElementTree as ET
import pickle
import os
from os import listdir, getcwd
from os.path import join
sets = ['train', 'test','val']
Imgpath = './VOCData/images'    #图片文件夹
xmlfilepath = './VOCData/Annotations/'  #xml文件存放地址
ImageSets_path='./VOCData/ImageSets/'
classes = ['car', 'bus', 'van', 'others']   # 识别目标种类
def convert(size, box):
    dw = 1. / size[0]
    dh = 1. / size[1]
    x = (box[0] + box[1]) / 2.0
    y = (box[2] + box[3]) / 2.0
    w = box[1] - box[0]
    h = box[3] - box[2]
    x = x * dw
    w = w * dw
    y = y * dh
    h = h * dh
    return (x, y, w, h)
def convert_annotation(image_id):
    in_file = open(xmlfilepath+'%s.xml' % (image_id))
    out_file = open('VOCData/labels/%s.txt' % (image_id), 'w')
    tree = ET.parse(in_file)
    root = tree.getroot()
    size = root.find('size')
    w = int(size.find('width').text)
    h = int(size.find('height').text)
    for obj in root.iter('object'):
        difficult = obj.find('difficult').text
        cls = obj.find('name').text
        if cls not in classes or int(difficult) == 1:
            continue
        cls_id = classes.index(cls)
        xmlbox = obj.find('bndbox')
        b = (float(xmlbox.find('xmin').text), float(xmlbox.find('xmax').text), float(xmlbox.find('ymin').text),
             float(xmlbox.find('ymax').text))
        bb = convert((w, h), b)
        out_file.write(str(cls_id) + " " + " ".join([str(a) for a in bb]) + '\n')
wd = getcwd()
# print(wd)  #current file which you are executing path
for image_set in sets:
    if not os.path.exists('VOCData/labels'):
        os.makedirs('VOCData/labels')
    image_ids = open(ImageSets_path+'%s.txt' % (image_set)).read().strip().split()
    list_file = open('VOCData/%s.txt' % (image_set), 'w')
    for image_id in image_ids:
        list_file.write(Imgpath+'/%s.jpg\n' % (image_id))
        convert_annotation(image_id)
    list_file.close()