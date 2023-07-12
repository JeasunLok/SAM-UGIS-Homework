from osgeo import gdal,ogr
import numpy as np
from sklearn.metrics import confusion_matrix, cohen_kappa_score
from skimage.segmentation import  quickshift
import pandas as pd
import scipy
import geopandas as gpd
from sklearn.ensemble import RandomForestClassifier
import sklearn.metrics as m
from utils import tif_processing

def segment_features(segment_pixels):
    features = []
    npixels, nbands = segment_pixels.shape
    for b in range(nbands):
        stats = scipy.stats.describe(segment_pixels[:, b])
        band_stats = [stats.mean,stats.variance]
        if npixels == 1:
            band_stats=[int(segment_pixels[:, b]),0]
        features+=band_stats
    return features

def split_dataset(samples_path,train_radio=0.7):
    gdf = gpd.read_file(samples_path)
    gdf_train = gdf.sample(frac=train_radio)
    gdf_test = gdf.drop(gdf_train.index)
    train_path = samples_path[:-4]+'_train.shp'
    test_path = samples_path[:-4] + '_test.shp'
    gdf_train.to_file(train_path)
    gdf_test.to_file(test_path)
    return train_path,test_path

def match(segmentation,objects,segment_ids,t_sample_path,im_geotrans,im_proj,im_width, im_height):
    train_ds = ogr.Open(t_sample_path)
    lyr = train_ds.GetLayer()
    driver = gdal.GetDriverByName('MEM')
    target_ds = driver.Create('', im_width, im_height, 1, gdal.GDT_UInt16)
    target_ds.SetGeoTransform(im_geotrans)
    target_ds.SetProjection(im_proj)
    options = ['ATTRIBUTE=gridcode']
    gdal.RasterizeLayer(target_ds, [1], lyr, options=options)#train/test sample array
    ground_truth = target_ds.GetRasterBand(1).ReadAsArray()#train/test sample array
    ground_truth = ground_truth.transpose((1, 0))
    classes = np.unique(ground_truth)[1:]
    segments_per_class = {}
    for klass in classes:
        segments_of_class = segmentation[ground_truth == klass]
        segments_per_class[klass] = set(segments_of_class)

    intersection = set()
    accum = set()
    for class_segments in segments_per_class.values():
        intersection |= accum.intersection(class_segments)
        accum |= class_segments
    # assert len(intersection) == 0, "Segment(s) represent multiple classes"

    train_img = np.copy(segmentation)
    threshold = train_img.max() + 1

    for klass in classes:
        class_label = threshold + klass
        for segment_id in segments_per_class[klass]:
            train_img[train_img == segment_id] = class_label

    train_img[train_img <= threshold] = 0
    train_img[train_img > threshold] -= threshold

    training_objects = []
    training_labels = []
    for klass in classes:
        class_train_object = [v for i, v in enumerate(objects) if segment_ids[i] in segments_per_class[klass]]
        training_labels += [klass] * len(class_train_object)
        training_objects += class_train_object

    return train_img,training_objects,training_labels

def accuracy_asessment(samples, classification,classes):

    prec_res = {"recall": [], "precision": [], "F1": [], "OA": [],"kappa":[]}
    prec_res['F1'] = m.f1_score(samples.flatten(), classification.flatten(), average=None)
    prec_res['precision'] = m.precision_score(samples.flatten(), classification.flatten(), average=None)
    prec_res['recall'] = m.recall_score(samples.flatten(), classification.flatten(), average=None)
    prec_res['OA'] = m.accuracy_score(samples.flatten(), classification.flatten())
    prec_res['kappa'] = cohen_kappa_score(samples.flatten(), classification.flatten(), labels=range(1, classes + 1))

    return prec_res