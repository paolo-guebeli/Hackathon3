import shutil
import subprocess
import os


def move_files(base_path='10_patients'):
    for dir in os.listdir(base_path):
        path = base_path + '/' + dir
        path += '/' + os.listdir(path)[0]
        seg_dir = ''
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


def converter(base_path='10_patients'):
    for dir in os.listdir(base_path):
        path = base_path + '/' + dir
        path += '/' + os.listdir(path)[0]
        path += '/' + os.listdir(path)[0]
        print(path)
        result_path = base_path+'/'+dir+'-nrrd'
        subprocess.call(['plastimatch', 'convert', '--input', path, '--output-prefix', result_path, '--prefix-format', 'nrrd', '--output-img', result_path+"_full.nrrd"])


def main():
    path = 'dataset/manifest-1603198545583/NSCLC-Radiomics'
    converter(path)


if __name__ == '__main__':
    main()
