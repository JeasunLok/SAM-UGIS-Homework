from osgeo import gdal
from skimage.segmentation import  quickshift
from skimage.segmentation import mark_boundaries
import os
import sys
dir_path = os.path.dirname(os.path.realpath(__file__)) # 获取当前目录
parent_dir_path = os.path.abspath(os.path.join(dir_path, os.pardir)) # 获取上级目录
sys.path.append(parent_dir_path) # 添加上级目录
from utils import tif_processing

def econ_segmentation(img_path, segmentation_path, kernel_size=10, max_dist=10):
    '''
    use quickshift method(similar to econ's) to segment image
    :param img_path: original image for segmentation
    :param segmentation_path: path to save segmentation result
    :param kernel_size: parameter for segmentation,parameter is bigger,segmentation objects are bigger
    :param max_dist: parameter for segmentation,parameter is bigger,segmentation objects are bigger
    :return: none
    :save1:econ_segmentation tiff result for latter use
    :save2:econ_segmentation tiff result for displaying
    '''
    print("segmentation")
    im_data, im_geotrans, im_proj, im_width, im_height = tif_processing.read_tif(img_path)
    im_data = im_data[0:3]
    temp = im_data.transpose((2, 1, 0))  # image(width, height, channels) ndarray
    segmentation = quickshift(temp, kernel_size=kernel_size, max_dist=max_dist, ratio=0.5)
    display = mark_boundaries(temp, segmentation)
    display = display.transpose((2, 1, 0))
    segmentation = segmentation.transpose((1, 0))
    tif_processing.write_tif(segmentation_path, segmentation, im_geotrans, im_proj, gdal.GDT_Float32)
    tif_processing.write_tif(segmentation_path[:-4]+'_display.tif', display, im_geotrans, im_proj, gdal.GDT_Float32)