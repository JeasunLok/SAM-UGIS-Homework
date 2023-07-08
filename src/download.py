from samgeo import tms_to_geotiff
from osgeo import gdal,osr
# 导入上级目录的模块
import os
dir_path = os.path.dirname(os.path.realpath(__file__)) # 获取当前目录
parent_dir_path = os.path.abspath(os.path.join(dir_path, os.pardir)) # 获取上级目录
import sys
sys.path.append(parent_dir_path) # 添加上级目录
from utils import tif_processing

def download_satellite_image(img_path, bbox, zoom, source="Satellite", return_image=False):
    # 调用API下载EPSG:3857的google影像
    tms_to_geotiff(output=img_path,
                   bbox=bbox,
                   zoom=zoom,
                   source=source,
                   crs="EPSG:3857",
                   return_image=return_image,
                   overwrite=True)
    
    # WKT3857的投影信息
    WKT_3857 = 'PROJCS["WGS 84 / Pseudo-Mercator", GEOGCS["WGS 84",DATUM["WGS_1984",SPHEROID["WGS 84",6378137,298.257223563, AUTHORITY["EPSG","7030"]], AUTHORITY["EPSG","6326"]], PRIMEM["Greenwich",0,AUTHORITY["EPSG","8901"]], UNIT["degree",0.0174532925199433, AUTHORITY["EPSG","9122"]], AUTHORITY["EPSG","4326"]], PROJECTION["Mercator_1SP"], PARAMETER["central_meridian",0], PARAMETER["scale_factor",1], PARAMETER["false_easting",0], PARAMETER["false_northing",0], UNIT["metre",1, AUTHORITY["EPSG","9001"]], AXIS["Easting",EAST], AXIS["Northing",NORTH], EXTENSION["PROJ4","+proj=merc +a=6378137 +b=6378137 +lat_ts=0 +lon_0=0 +x_0=0 +y_0=0 +k=1 +units=m +nadgrids=@null +wktext +no_defs"], AUTHORITY["EPSG","3857"]]'

    # 进行投影
    img = gdal.Open(path)
    GeoTransform = img.GetGeoTransform()
    tif_processing.geoCoordSys(path, GeoTransform, WKT_3857)
    
if __name__ == "__main__":
    path = r"images/download/test.tif"
    bbox = [-95.3704, 29.6762, -95.366, 29.6795]
    download_satellite_image(path, bbox, 20)