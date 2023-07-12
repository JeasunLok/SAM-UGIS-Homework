from osgeo import gdal
import numpy as np
from sklearn.metrics import confusion_matrix, cohen_kappa_score
# 导入上级目录的模块
import os
dir_path = os.path.dirname(os.path.realpath(__file__)) # 获取当前目录
parent_dir_path = os.path.abspath(os.path.join(dir_path, os.pardir)) # 获取上级目录
import sys
sys.path.append(parent_dir_path) # 添加上级目录
from utils import tif_processing

def main_classification(segmentation_path, samples_path, classification_path, classification_method):
    print("classification")
    segmentation, seg_Geotrans, seg_proj, seg_cols, seg_rows = tif_processing.read_tif(segmentation_path)
    samples, smp_Geotrans, smp_proj, smp_cols, smp_rows = tif_processing.read_tif(samples_path)

    if seg_Geotrans!=smp_Geotrans or seg_proj!= smp_proj or seg_cols!=smp_cols or seg_rows!=smp_rows:
        return False
    else:
        if classification_method == "DT":
            classification_result = dt_classification(segmentation, samples)
        elif classification_method == "SVM":
            classification_result = svm_classification(segmentation, samples)
        elif classification_result == "RF":
            classification_result = rf_classification(segmentation, samples)

        tif_processing.write_tif(classification_path, classification_result, seg_Geotrans, seg_proj, gdal.GDT_Float32)
        oa, kappa = accuracy_asessment(samples, classification_result)
        return oa, kappa

def accuracy_asessment(samples, classification):
    conf_matrix = confusion_matrix(samples.flatten(), classification.flatten(), labels=np.linspace(1, np.max(samples), np.max(samples)))

    overall_accuracy = np.trace(conf_matrix) / sum(sum(conf_matrix))

    kappa = cohen_kappa_score(samples.flatten(), classification.flatten(), labels=np.linspace(1, np.max(samples), np.max(samples)))

    return overall_accuracy, kappa

def dt_classification(segmentation, samples):
    print("dt classification")
    classification = None
    return classification

def svm_classification(segmentation, samples):
    print("dt classification")
    classification = None
    return classification

def rf_classification(segmentation, samples):
    print("dt classification")
    classification = None
    return classification