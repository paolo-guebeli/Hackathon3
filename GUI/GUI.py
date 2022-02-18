from dataclasses import dataclass
import os, glob
from tabnanny import filename_only
from tkinter import filedialog
from tkinter import *
import matplotlib.pyplot as plt
import pydicom
import pydicom.data
import numpy as np
import pylab as pl
import sys
import matplotlib.path as mplPath
import one_time_features
import pickle

# set plotly credentials here 
# this allows you to send results to your account plotly.tools.set_credentials_file(username=your_username, api_key=your_key
#import SimpleITK as sitk
#import six
#import pandas as pd
#import os

#import radiomics as rm
#from radiomics import featureextractor


#def get_features(path):
#    dir_list = []
#    metastases = 0
#    for dir in os.listdir(path):
#        if '_full.nrrd' not in dir:
#            if 'nrrd' in dir:
#                dir_list.append(dir)
#    tdf = None
#    count = 0
#    for folder in dir_list:
#        extractor = featureextractor.RadiomicsFeatureExtractor("Params.yaml")
#        if os.path.exists(path + '/' + folder + '/GTV-1.nrrd'):
#            result = extractor.execute(path + '/' + folder + '_full.nrrd', path + '/' + folder + '/GTV-1.nrrd')
#        else:
#            for i in os.listdir( path + '/' + folder):
#                if 'gtv' in i:
#                    result = extractor.execute(path + '/' + folder + '_full.nrrd', path + '/' + folder + '/'+i)
#                    metastases -= 1
#                    break
#        clean_dict = {}
#        for key, value in result.items():
#            if 'diagnostics' not in key:
#                value = float(value)
#                clean_dict[key] = value
#        for i in os.listdir(path + '/' + folder):
#            if 'gtv' in i:
#                metastases += 1
#        clean_dict['metastases'] = metastases
#        if tdf is None:
#            tdf = pd.DataFrame(columns=clean_dict.keys())
#        tdf = tdf.append(clean_dict, ignore_index=True)
#        count += 1
#        print(f'{count}/{len(dir_list)}')

#    return tdf

#functions for dcm images display


def browse_button():
    filename = filedialog.askdirectory()
    #tdf = get_features(path=filename)
    #tdf.to_csv('features.csv', sep=';')
    print(filename)
    img_path = one_time_features.move_files(filename)
    newWindow = Toplevel(root)
    newWindow.geometry('400x400')
    label1 = Label(newWindow, text="Select a option:")
    label1.pack(fill=X, padx=5, pady=5)
    button2 = Button(newWindow, text="Run script", command=lambda: get_prediction(), bg='LIGHTBLUE').pack(
        side=TOP,
        ipadx=5,
        ipady=5,
        expand=True
    )
    button3 = Button(newWindow, text="view image", command=lambda: view_image(filename, img_path), bg='LIGHTBLUE').pack(
        side=TOP,
        ipadx=5,
        ipady=5,
        expand=True
    )
    return_button = Button(newWindow, text='Return', command=lambda: newWindow.destroy()).pack(
        side=TOP,
        ipadx=5,
        ipady=5,
        expand=True
    )
    exit_button = Button(newWindow, text='Exit', command=lambda: root.quit()).pack(
        side=TOP,
        ipadx=5,
        ipady=5,
        expand=True
    )


def view_image(path, img_path):
        class IndexTracker(object):
            def __init__(self, ax, X):
                self.ax = ax
                ax.set_title('Scroll to Navigate through the DICOM Image Slices')

                self.X = X
                rows, cols, self.slices = X.shape
                self.ind = self.slices//2

                self.im = ax.imshow(self.X[:, :, self.ind])
                self.update()

            def onscroll(self, event):
                print("%s %s" % (event.button, event.step))
                if event.button == 'up':
                    self.ind = (self.ind + 1) % self.slices
                else:
                    self.ind = (self.ind - 1) % self.slices
                self.update()

            def update(self):
                self.im.set_data(self.X[:, :, self.ind])
                #ax.set_ylabel('Slice Number: %s' % self.ind)
                self.im.axes.figure.canvas.draw()
        fig, ax = plt.subplots(1,1)
        
        os.system("tree "+ path)
        #os.system("tree C:/Users/giorg/Desktop/test python/LUNG1-001/09-18-2008-StudyID-NA-69331")
        plots = []
        for f in glob.glob(img_path + "/*.dcm"):
        #for f in glob.glob("C:/Users/giorg/Desktop/test python/LUNG1-001/09-18-2008-StudyID-NA-69331/img/*.dcm"):
            if '1-1.dcm' not in f:
                pass
                ds = pydicom.dcmread(f)
                pix = ds.pixel_array
                pix = pix*1+(-1024)
                plots.append(pix)

        y = np.dstack(plots)

        tracker = IndexTracker(ax, y)

        fig.canvas.mpl_connect('scroll_event', tracker.onscroll)
        plt.show()


def get_prediction(path):
    base_path = one_time_features.converter(path)
    features = one_time_features.get_features(base_path)
    features_df = pd.DataFrame.from_dict(features)
    relevant_feat_over_list = ['original_shape_Maximum2DDiameterRow', 'original_shape_Sphericity',
                               'original_glcm_DifferenceEntropy', 'original_glrlm_ShortRunEmphasis', 'metastases']
    
    # Add prediction script
    overall_model_pkl_filename = 'overall_stage_model.pkl'
    overall_stage_model_pkl = open(overall_model_pkl_filename, 'rb')
    overall_stage_model = pickle.load(overall_stage_model_pkl)
    overall_stage_model.predict(features_df)
    
    # Add PDF creator


if __name__ == '__main__':
    root = Tk()
    root.configure(bg='white')
    root.geometry('400x400')
    root.resizable(True, True)
    root.title('Radiomics')

    label = Label(root, text='Click button to select the patient to analyse',bg='white')
    label.pack(ipadx=5, ipady=5)

    button = Button(text="Select patient folder", command=browse_button, bg='LIGHTBLUE').pack(
        side=TOP,
        ipadx=5,
        ipady=5,
        expand=True
    )
    exit_button = Button(
        root,
        text='Exit',
        command=lambda: root.quit()
    ).pack(
        side=TOP,
        ipadx=5,
        ipady=5,
        expand=True
        )

    mainloop()





