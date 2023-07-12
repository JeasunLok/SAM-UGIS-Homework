import os
import sys
import geopandas as gpd
from osgeo import gdal
from osgeo import ogr
import numpy as np
import pandas as pd
import scipy
from sklearn.ensemble import RandomForestClassifier
from sklearn import svm
from sklearn.tree import DecisionTreeClassifier
import sklearn.metrics as m
dir_path = os.path.dirname(os.path.realpath(__file__)) # 获取当前目录
parent_dir_path = os.path.abspath(os.path.join(dir_path, os.pardir)) # 获取上级目录
sys.path.append(parent_dir_path) # 添加上级目录
from utils import other
from utils import tif_processing

def main_classification(img_path, segmentation_path, samples_path,classification_path, train_radio, classification_method):
    '''
    classify the segmented image
    :param img_path: original image
    :param segmentation_path: segmentation file(sam/econ)
    :param samples_path:point feature(samplex.shp)
    :param classification_path:classification output path
    :param train_radio:radio of train dataset
    :param classification_method:"RF" or "SVM" or" DT"
    :return:accuracy assessment dict
    :save:classification tiff result
    '''
    # print("classification")
    #-------------read file----------------
    im_data, im_geotrans, im_proj, im_width, im_height = tif_processing.read_tif(img_path)
    segmentation,_,_,_,_= tif_processing.read_tif(segmentation_path)

    im_data = im_data[0:3]
    temp = im_data.transpose((2, 1, 0))
    segmentation = segmentation.transpose((1,0))
    #----------split train,test-------------
    train_path,test_path = other.split_dataset(samples_path,train_radio)
    #--------------build feature-----------
    segment_ids = np.unique(segmentation)
    objects = []
    object_ids = []
    for i in segment_ids:
        segment_pixels = temp[segmentation == i]
        object_features = other.segment_features(segment_pixels)
        objects.append(object_features)
        object_ids.append(id)
    #-------------get train/test objects using train/test samples-------
    train_img,training_objects, training_labels = other.match(segmentation, objects, segment_ids, train_path, im_geotrans, im_proj, im_width, im_height)
    test_img,_,_ = other.match(segmentation, objects, segment_ids, test_path, im_geotrans, im_proj, im_width, im_height)
    #------------classify----------------
    if classification_method == "RF":
        classifier = RandomForestClassifier(n_jobs=-1)
    elif classification_method == "SVM":
        classifier = svm.SVC(gamma='scale', C=1.0, decision_function_shape='ovr', kernel='rbf')
    elif classification_method == "DT":
        classifier = DecisionTreeClassifier(random_state=0)

    classifier.fit(training_objects, training_labels)
    predicted = classifier.predict(objects)
    #----------output----------------
    clf = segmentation.copy()
    for segment_id, klass in zip(segment_ids, predicted):
        clf[clf == segment_id] = klass
    mask = np.sum(temp, axis=2)
    mask[mask > 0.0] = 1.0
    mask[mask == 0.0] = -1.0

    clf = np.multiply(clf, mask)
    clf[clf < 0] = 0
    clf[clf > 255] = 255
    clf = clf.transpose((1, 0))
    driverTiff = gdal.GetDriverByName("GTiff")
    clfds = driverTiff.Create(classification_path, im_width, im_height,
                              1, gdal.GDT_Byte)
    clfds.SetGeoTransform(im_geotrans)
    clfds.SetProjection(im_proj)
    clfds.GetRasterBand(1).SetNoDataValue(255)
    clfds.GetRasterBand(1).WriteArray(clf)
    clfds = None
    #-------------accuracy assesment------------------
    clf = clf.transpose((1, 0))
    prec_res = other.accuracy_asessment(test_img[test_img!=0], clf[test_img!=0],classes=len(np.unique(test_img))-1)
    return prec_res

if __name__=="__main__":
    state = 'sam'
    econ_seg = True
    train_radio = 0.6
    classification_method = 'DT'
    if state=='sam':
        img_path = r'images\download\example1.tif'
        segmentation_path = r'images\segmentation\sam\example1_segmentation.tif'
        samples_path = r'images\samples\sample1.shp'
        classification_path = r'images\classification\example1_classification_DT.tif'
    if state=='econ':
        img_path = r'images\download\example1.tif'
        segmentation_path = r'images\segmentation\econ\example1_segmentation.tif'
        samples_path = r'images\samples\sample1.shp'
        classification_path = r'images\classification\example1_classification_DT.tif'
        # if econ_seg==True:
        #     econ_segmentation.econ_segmentation(img_path, segmentation_path, kernel_size=10, max_dist=10)

    precision_dict = main_classification(img_path, segmentation_path, samples_path, classification_path, train_radio,
                        classification_method)
    # print(precision_dict)
    print(1)