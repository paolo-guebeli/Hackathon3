
import shutil
import subprocess

import os

from radiomics import featureextractor


def move_files(path):
        if len(os.listdir(path)) > 1:
            dir_list = []
            for i in os.listdir(path):
                if 'Segmentation' not in i:
                    dir_list.append(i)
                else:
                    shutil.rmtree(path+'/'+i)
            seg_path = path + '/' + dir_list[1]
            path += '/' + dir_list[0]
            if len(os.listdir(seg_path)) > 0:
                for seg_file in os.listdir(seg_path):
                    os.rename(seg_path + '/' + seg_file, path + '/' + seg_file)
            shutil.rmtree(seg_path)
            return path
        return path+'/'+os.listdir(path)[0]


def converter(base_path):
        path = base_path + '/' + os.listdir(base_path)[0]
        base_path = '/'.join(base_path.split('/')[:-1])
        result_path = base_path + '-nrrd'
        subprocess.call(['plastimatch', 'convert', '--input', path, '--output-prefix', result_path, '--prefix-format', 'nrrd', '--output-img', result_path+"_full.nrrd"])
        return base_path


def get_features(path):
    metastases = 0
    path += '-nrrd'
    extractor = featureextractor.RadiomicsFeatureExtractor("Params.yaml")
    if os.path.exists(path + '/GTV-1.nrrd'):
        result = extractor.execute(path +'_full.nrrd', path + '/GTV-1.nrrd')
    else:
        for i in os.listdir(path):
            if 'gtv' in i:
                result = extractor.execute(path + '_full.nrrd', path + '/' + i)
                metastases -= 1
                break
    clean_dict = {}
    for key, value in result.items():
        if 'diagnostics' not in key:
            value = float(value)
            clean_dict[key] = value
    for i in os.listdir(path):
        if 'gtv' in i:
            metastases += 1
    clean_dict['metastases'] = metastases
    return clean_dict


def main(path):
    move_files(path)
    converter(path)
    print(get_features(path))



