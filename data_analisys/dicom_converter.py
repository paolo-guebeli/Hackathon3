import subprocess
import os


def move_files(base_path='10_patients'):
    for dir in os.listdir(base_path):
        path = base_path + '/' + dir
        path += '/' + os.listdir(path)[0]
        seg_dir = ''
        for i in os.listdir(path)[1:]:
            if 'Segmentation' not in i:
                seg_dir = i
        seg_path = path + '/' + seg_dir
        path += '/' + os.listdir(path)[0]
        if len(os.listdir(seg_path)) > 0:
            for seg_file in os.listdir(seg_path):
                os.rename(seg_path + '/' + seg_file, path + '/' + seg_file)


def converter(base_path='10_patients'):
    for dir in os.listdir(base_path):
        path = base_path + '/' + dir
        path += '/' + os.listdir(path)[0]
        path += '/' + os.listdir(path)[0]
        result_path = base_path+'/'+dir+'-nrrd'
        subprocess.call(['plastimatch', 'convert', '--input', path, '--output-prefix', result_path, '--prefix-format', 'nrrd', '--output-img', result_path+"_full.nrrd"])



def main():
    move_files()
    converter()


if __name__ == '__main__':
    main()
