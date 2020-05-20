# Labelme-dataset-extension-script
对已使用labelme标注的数据集生成左右/上下镜面翻转后的图片与标注文件

## 开发环境
python 3.6.10

## 使用教程
https://blog.csdn.net/a2824256/article/details/106231949

## labeme是什么？
一个用于标注图像语义分割或者说图像实例分割的标注软件

## labelme标注文件格式
- shapes - 标注的多边形数据
- imagePath - 图片路径
- imageData - 图片base64转义的图像数据
- imageHeight - 图像的高度
- imageWidth - 图像的宽度

## 特别说明
labelme读取的是json文件里的数据，图片数据是读imageData的base64数据而不是原图

## 使用说明
直接修改transform.py文件顶部这几个参数即可使用
```python
# 数据集路径
path = ".\\data\\"
# 生成数据的保存路径
save_path = ".\\data\\"
# 当前数据集图片格式
file_format = ".jpg"
# 替换格式jpg -> json
replace_format = ".json"
# 左右翻转文件名附加字符
LR = "lr_"
# 上下翻转文件名附加字符
TB = "tb_"
```
####
```python
# 最后执行
python transform.py
```
