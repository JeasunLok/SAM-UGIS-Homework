import numpy as np
from osgeo import gdal
# 读取tif
def read_tif(path):
    dataset = gdal.Open(path)
    cols = dataset.RasterXSize # 图像长度
    rows = (dataset.RasterYSize) # 图像宽度
    im_proj = (dataset.GetProjection()) # 读取投影
    im_Geotrans = (dataset.GetGeoTransform()) # 读取仿射变换
    im_data = dataset.ReadAsArray(0, 0, cols, rows) # 转为numpy格式
    del dataset
    return im_data, im_Geotrans, im_proj, cols, rows

# 写出tif
def write_tif(newpath, im_data, im_geotrans, im_proj, datatype):
    # datatype常用gdal.GDT_UInt16 gdal.GDT_Int16 gdal.GDT_Float32
    if len(im_data.shape)==3:
        im_bands, im_height, im_width = im_data.shape
    else:
        im_bands, (im_height, im_width) = 1, im_data.shape
    driver = gdal.GetDriverByName('GTiff')
    new_dataset = driver.Create(newpath, im_width, im_height, im_bands, datatype)
    new_dataset.SetGeoTransform(im_geotrans)
    new_dataset.SetProjection(im_proj)

    if im_bands == 1:
        new_dataset.GetRasterBand(1).WriteArray(im_data.reshape(im_height, im_width))
    else:
        for i in range(im_bands):
            new_dataset.GetRasterBand(i+1).WriteArray(im_data[i])
    del new_dataset

# 为影像写入坐标系的函数（创建新tif）
# def geoCoordSys(read_path, img_transf, img_proj):
#         array_dataset = gdal.Open(read_path)
#         img_array = array_dataset.ReadAsArray(
#             0, 0, array_dataset.RasterXSize, array_dataset.RasterYSize)
#         if 'int8' in img_array.dtype.name:
#             datatype = gdal.GDT_Byte
#         elif 'int16' in img_array.dtype.name:
#             datatype = gdal.GDT_UInt16
#         else:
#             datatype = gdal.GDT_Float32

#         if len(img_array.shape) == 3:
#             img_bands, im_height, im_width = img_array.shape
#         else:
#             img_bands, (im_height, im_width) = 1, img_array.shape

#         filename = read_path[:-4] + '_proj' + '.tif'
#         driver = gdal.GetDriverByName("GTiff")  # 创建文件驱动
#         dataset = driver.Create(
#             filename, im_width, im_height, img_bands, datatype)
#         dataset.SetGeoTransform(img_transf)  # 写入仿射变换参数
#         dataset.SetProjection(img_proj)  # 写入投影

#         # 写入影像数据
#         if img_bands == 1:
#             dataset.GetRasterBand(1).WriteArray(img_array)
#         else:
#             for i in range(img_bands):
#                 dataset.GetRasterBand(i + 1).WriteArray(img_array[i])
#         print(read_path, 'geoCoordSys get!')

# 为影像修改坐标系的函数（修改tif）
def geoCoordSys(read_path, img_transf, img_proj): 
        dataset = gdal.Open(read_path)
        dataset.SetGeoTransform(img_transf)  # 写入仿射变换参数
        dataset.SetProjection(img_proj)  # 写入投影
        print(read_path, 'geoCoordSys get!')
