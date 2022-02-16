import os

import SimpleITK as sitk
import six
import pandas as pd
import os

import radiomics as rm
from radiomics import featureextractor


def get_features(path):
    tdf_list = []
    dir_list = []
    for dir in os.listdir():
        if '_full.nrrd' not in dir:
            dir_list.append(dir)
    for folder in dir_list:
        extractor = featureextractor.RadiomicsFeatureExtractor("Params.yaml")
        result = extractor.execute(path+'LUNG1-001-nrrd_full.nrrd', path + 'LUNG1-001-nrrd/GTV-1.nrrd')
        clean_dict = {}
        for key, value in result.items():
            if 'diagnostics' not in key:
                value = float(value)
                clean_dict[key] = value
        tdf = pd.DataFrame(columns=clean_dict.keys())
        tdf = tdf.append(clean_dict, ignore_index=True)
        tdf_list.append(tdf)
    return tdf_list
