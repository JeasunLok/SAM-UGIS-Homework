import numpy as np
from osgeo import gdal

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
