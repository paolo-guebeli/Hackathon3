import os

import SimpleITK as sitk
import six
import pandas as pd
import os

import radiomics as rm
from radiomics import featureextractor


def get_features(path):
    dir_list = []
    metastases = 0
    for dir in os.listdir(path):
        if '_full.nrrd' not in dir:
            if 'nrrd' in dir:
                dir_list.append(dir)
    tdf = None
    count = 0
    for folder in dir_list:
        extractor = featureextractor.RadiomicsFeatureExtractor("Params.yaml")
        if os.path.exists(path + '/' + folder + '/GTV-1.nrrd'):
            result = extractor.execute(path + '/' + folder + '_full.nrrd', path + '/' + folder + '/GTV-1.nrrd')
        else:
            for i in os.listdir( path + '/' + folder):
                if 'gtv' in i:
                    result = extractor.execute(path + '/' + folder + '_full.nrrd', path + '/' + folder + '/'+i)
                    metastases -= 1
                    break
        clean_dict = {}
        for key, value in result.items():
            if 'diagnostics' not in key:
                value = float(value)
                clean_dict[key] = value
        for i in os.listdir(path + '/' + folder):
            if 'gtv' in i:
                metastases += 1
        clean_dict['metastases'] = metastases
        if tdf is None:
            tdf = pd.DataFrame(columns=clean_dict.keys())
        tdf = tdf.append(clean_dict, ignore_index=True)
        count += 1
        print(f'{count}/{len(dir_list)}')

    return tdf


def main():
    tdf = get_features(path='dataset/manifest-1603198545583/NSCLC-Radiomics')
    tdf.to_csv('features.csv', sep=';')


if __name__ == '__main__':
    main()
