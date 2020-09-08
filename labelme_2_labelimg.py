import os
import glob
import json
from numba import njit
import xml.dom.minidom
from xml.dom import minidom
path = "F:\\0903modeldata\\labels\\"
img_list = glob.glob(path + "*.json")
width = 0
height = 0

# 自行填写当前文件夹，假如文件路径分割数组长度为1
folder = ""


def get_annotation(labels):
    res = []
    for i in range(len(labels)):
        bndbox = get_bndbox(labels[i]['points'])
        res.append([labels[i]['label'], bndbox])
    return res


def get_bndbox(list):
    global width, height
    xmin = width
    ymin = height
    xmax = 0
    ymax = 0
    for i in range(len(list)):
        if list[i][0] > xmax:
            xmax = int(list[i][0])
        if list[i][0] < xmin:
            xmin = int(list[i][0])
        if list[i][1] > ymax:
            ymax = int(list[i][1])
        if list[i][1] < ymin:
            ymin = int(list[i][1])
    return [xmin, ymin, xmax, ymax]




for i in range(len(img_list)):
    json_path = img_list[i]
    is_exists = os.path.exists(json_path)
    if is_exists:
        # 打开json文件
        f = open(json_path, encoding='utf-8')
        # 读取json
        content = json.load(f)
        width = content['imageWidth']
        height = content['imageHeight']
        labels = content['shapes']
        labels = get_annotation(labels)
        image_path = content['imagePath']
        path_array = image_path.split('\\')
        length = len(path_array)
        if length < 1:
            continue
        elif length > 1:
            folder = path_array[0]
        impl = minidom.getDOMImplementation()
        # 创建根节点
        dom = impl.createDocument(None, 'annotation', None)
        root = dom.documentElement
        # folder
        nameE = dom.createElement('folder')
        nameT = dom.createTextNode(folder)
        nameE.appendChild(nameT)
        root.appendChild(nameE)
        # filename
        nameE = dom.createElement('filename')
        nameT = dom.createTextNode(path_array[len(path_array)-1])
        nameE.appendChild(nameT)
        root.appendChild(nameE)
        # path
        nameE = dom.createElement('path')
        nameT = dom.createTextNode(image_path)
        nameE.appendChild(nameT)
        root.appendChild(nameE)
        # source
        nameE = dom.createElement('source')
        # sub - database
        nameE_sub = dom.createElement('database')
        nameT_sub = dom.createTextNode("Unknown")
        nameE_sub.appendChild(nameT_sub)
        nameE.appendChild(nameE_sub)
        root.appendChild(nameE)
        # size
        nameE = dom.createElement('size')
        # sub - width
        nameE_sub = dom.createElement('width')
        nameT_sub = dom.createTextNode(str(width))
        nameE_sub.appendChild(nameT_sub)
        nameE.appendChild(nameE_sub)
        root.appendChild(nameE)
        # sub - height
        nameE_sub = dom.createElement('height')
        nameT_sub = dom.createTextNode(str(height))
        nameE_sub.appendChild(nameT_sub)
        nameE.appendChild(nameE_sub)
        root.appendChild(nameE)
        # sub - depth
        nameE_sub = dom.createElement('depth')
        nameT_sub = dom.createTextNode('3')
        nameE_sub.appendChild(nameT_sub)
        nameE.appendChild(nameE_sub)
        root.appendChild(nameE)
        # segmented
        nameE = dom.createElement('segmented')
        nameT = dom.createTextNode('0')
        nameE.appendChild(nameT)
        root.appendChild(nameE)
        # object - iterator
        for obj_i in labels:
            # object
            nameE = dom.createElement('object')
            # sub - name
            nameE_sub = dom.createElement('name')
            nameT_sub = dom.createTextNode(obj_i[0])
            nameE_sub.appendChild(nameT_sub)
            nameE.appendChild(nameE_sub)
            # sub - pose
            nameE_sub = dom.createElement('pose')
            nameT_sub = dom.createTextNode('Unspecified')
            nameE_sub.appendChild(nameT_sub)
            nameE.appendChild(nameE_sub)
            # sub - truncated
            nameE_sub = dom.createElement('truncated')
            nameT_sub = dom.createTextNode('0')
            nameE_sub.appendChild(nameT_sub)
            nameE.appendChild(nameE_sub)
            # sub - difficult
            nameE_sub = dom.createElement('difficult')
            nameT_sub = dom.createTextNode('0')
            nameE_sub.appendChild(nameT_sub)
            nameE.appendChild(nameE_sub)
            # sub - bndbox
            nameE_sub = dom.createElement('bndbox')
            # sub2 - xmin
            nameE_sub2 = dom.createElement('xmin')
            nameT_sub2 = dom.createTextNode(str(obj_i[1][0]))
            nameE_sub2.appendChild(nameT_sub2)
            nameE_sub.appendChild(nameE_sub2)
            # sub2 - ymin
            nameE_sub2 = dom.createElement('ymin')
            nameT_sub2 = dom.createTextNode(str(obj_i[1][1]))
            nameE_sub2.appendChild(nameT_sub2)
            nameE_sub.appendChild(nameE_sub2)
            # sub2 - xmax
            nameE_sub2 = dom.createElement('xmax')
            nameT_sub2 = dom.createTextNode(str(obj_i[1][2]))
            nameE_sub2.appendChild(nameT_sub2)
            nameE_sub.appendChild(nameE_sub2)
            # sub2 - ymax
            nameE_sub2 = dom.createElement('ymax')
            nameT_sub2 = dom.createTextNode(str(obj_i[1][3]))
            nameE_sub2.appendChild(nameT_sub2)
            nameE_sub.appendChild(nameE_sub2)
            nameE.appendChild(nameE_sub)
            root.appendChild(nameE)
        new_file = path_array[len(path_array)-1].replace('jpg', 'xml')
        new_file = "F:\\0903modeldata\\xml\\" + new_file
        f = open(new_file, 'w')
        dom.writexml(f, addindent=' ', newl='\n', encoding='utf-8')
        f.close()
        print(new_file + ' - 已生成')
    else:
        print(json_path + " - 没有该文件")
