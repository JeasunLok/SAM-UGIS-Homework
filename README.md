# SAM application in remote sensing images object-based classification for UGIS course
The homework of UGIS course: to develop a software (including algorithm and GUI) equipped with SAM to do segmentation and classification for remote sensing images.
***
#### Authors: [@JeasunLok](https://github.com/JeasunLok) [@PiggieGo](https://github.com/PiggieGo) [@XiaXiaJiang](https://github.com/XiaxiaJiang)
#### Geography Information Science Grade 2020, School of Geography and Planning, Sun Yat-Sen Univeristy.
#### June 14, 2023
#### Video: [Video of how to use the software in Chinese](https://www.bilibili.com/video/BV19V411T7UD/?vd_source=37637236b9378fa05cf47dbdc81be5df)
***
## Introduction
This is a software that can use SAM or multiscale segmentation to sement remote sensing images, then classify the images with input samples based on the segmenation and check the accuracy. 
The software is entirely written by Python, and the GUI is written by Python package tkinter.
***
## Features
* Easy installation and visualized GUI
* Two segmentation algorithms and three classification algorithms
* All results can be seen in GUI
***
## Installation
Install the requirement
```
git clone https://github.com/JeasunLok/SAM-UGIS-Homework.git && cd SAM-UGIS-Homework
conda create -n SAM-UGIS-Homework python=3.9
conda activate SAM-UGIS-Homework
pip install -r requirements.txt
pip install torch==1.13.1+cu117 -f https://download.pytorch.org/whl/torch_stable.html
```
Run the GUI in main to complete your task
```
python main.py
```
Download the pth parameters file of sam_vit_b in:
[Parameters file of sam_vit_b](https://dl.fbaipublicfiles.com/segment_anything/sam_vit_b_01ec64.pth)
Then place it under folder <b>asset</b>.  
Or you can modify the code an switch the backbone to sam_vit_l or sam_vit_h.
***
## How to use it
The GUI is shown below:
![GUI](/asset/GUI_show.png#pic_center=400x)
1. <b>Segmentation</b>  
Two file paths are need: click <b>"选择路径"</b> for <b>""输入图像文件"</b> and <b>""输出分割文件"</b>， <b>""输入图像文件"</b> is the original image you want to do segmentation and the output segmentation file is <b>""输出分割文件"</b>, then select the segmentation algorithm in <b>"选择分割算法"</b>. All these files are `tif` file.
Two selections <b>"SAM分割"</b> and <b>""多尺度分割"</b> can be selected. The former uses SAM to do segmentation and the latter uses quickshift algorithm to do segmentation. When using <b>""多尺度分割"</b>, two parmaters <b>""核大小"</b> and <b>""最大距离"</b> are needed, which represent the scale of the segmentation.
When doing segmentation, you should select the device GPU or CPU in <b>"选择运算设备"</b>.
<br>

2. <b>Classification</b>  
After completing the segmentation or you have the segmentation result of original image, you can enter two paths: click <b>"选择路径"</b> for <b>""输入样本文件"</b> and <b>""输出分类文件"</b>，<b>""输入样本文件"</b> is the training and testing samples of the classfier, and the output classification file is <b>""输出分割文件"</b>
Then select the classification algorithm in <b>"选择分类算法"</b>, <b>"决策树"</b> is decision tree algorithm, <b>"支持向量机"</b> is support vector machine algorithm and <b>"随机森林"</b> is random forest algorithm. It should be noticed that the samples file is `shp` point file and the output classification file is `tif` file.
The train ratio <b>ranged from 0 to 1</b> should be entered in <b>"训练集比例"</b>, and the classification accuracies (i.e. Overall accuracy (OA) and kappa coefficient (Kappa)) are shown in GUI immediately.
<br>

3. <b>Image visualization</b>  
The "图片" button can check the original image, segmentation result and classification result of the task:
![Image](/asset/Image_show.png#pic_center=400x)
* <b>"初始图片"</b> button shows the original image.
* <b>"分割结果"</b> button shows the segmentation result.
* <b>"分类结果"</b> button shows the classification result.
***
## Source
We provide 3 example images and samples in folder <b>images</b> for users to use and test our software and <b>the video of how to use the software in Chinese is released at [video of how to use the software](https://www.bilibili.com/video/BV19V411T7UD/?vd_source=37637236b9378fa05cf47dbdc81be5df)</b>.
***
## License
The software is licensed under the Apache 2.0 license.
***
## Acknowledgement
This software is made possible by the following open source projects. Credit goes to the developers of these projects: 
[segment-geospatial](https://github.com/opengeos/segment-geospatial)  
[segment-anything](https://github.com/facebookresearch/segment-anything)  