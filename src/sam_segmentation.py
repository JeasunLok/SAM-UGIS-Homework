import torch
from samgeo import SamGeo
from osgeo import ogr
import sys

def sam_segmentation(image_path, segmentation_path, str_device):
    checkpoint = r'asset\sam_vit_b_01ec64.pth'

    if str_device == "GPU":
        device = 'cuda' if torch.cuda.is_available() else 'cpu'
    else:
        device = 'cpu'
    
    sam = SamGeo(
        checkpoint=checkpoint,
        model_type='vit_b',
        device=device,
        sam_kwargs=None,
    )
    with torch.no_grad():
        sam.generate(image_path, segmentation_path)

def sam_segmentation_with_point(image_path, point_shp_path, segmentation_path, str_device):
    checkpoint = r'asset\sam_vit_b_01ec64.pth'

    if str_device == "GPU":
        device = 'cuda' if torch.cuda.is_available() else 'cpu'
    else:
        device = 'cpu'

    sam = SamGeo(
        checkpoint = checkpoint,
        model_type = "vit_b",
        device = device,
        automatic = False,
        sam_kwargs = None,
    )

    sam.set_image(image_path)

    #设置driver
    driver = ogr.GetDriverByName("ESRI Shapefile")
    #打开矢量
    ds = driver.Open(point_shp_path, 0)
    if ds is None:
        print("Open shapefile ERROR!")
        sys.exit(1)
    #获取图层
    layer = ds.GetLayer()

    #获取要素及要素地理位置
    point_coords = []
    feature = layer.GetNextFeature()
    while feature:
        geometry = feature.GetGeometryRef()
        x = geometry.GetX()
        y = geometry.GetY()
        point_coords.append([x, y]) 
        feature = layer.GetNextFeature()
    print(point_coords) 
    sam.predict(point_coords, point_labels=1, point_crs="EPSG:4326", output=segmentation_path)