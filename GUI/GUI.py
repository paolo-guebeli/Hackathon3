from dataclasses import dataclass
import os, glob, imp
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
import pdfFunction
import pandas as pd
import pickle




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
        plots = []
        for f in glob.glob(img_path + "/*.dcm"):
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
    # Add prediction script
    # pass data vector to pdf creator
   

    features_df = pd.DataFrame.from_dict(features)
    
    relevant_feat_over_list = ['original_shape_Maximum2DDiameterRow', 'original_shape_Sphericity',
                               'original_glcm_DifferenceEntropy', 'original_glrlm_ShortRunEmphasis', 'metastases']
    overall_model_pkl_filename = 'overall_stage_model.pkl'
    overall_stage_model_pkl = open(overall_model_pkl_filename, 'rb')
    overall_stage_model = pickle.load(overall_stage_model_pkl)
    predictions_overall = overall_stage_model.predict(features_df)
    if predictions_overall == 0:
        pred_over = "I"
    if predictions_overall == 0:
        pred_over = "II"
    if predictions_overall == 0:
        pred_over = "IIIa"
    if predictions_overall == 0:
        pred_over = "IIIb"
    print(f"Overall stage {pred_over} is predicted for the patient")
    
    # t_stage model
    relevant_feat_t_list = ['original_shape_LeastAxisLength', 'original_shape_MinorAxisLength',
                            'original_shape_Sphericity', 'original_firstorder_90Percentile',
                            'original_glcm_ClusterProminence', 'original_glcm_Correlation', 'original_glcm_Idn',
                            'original_glrlm_ShortRunEmphasis', 'original_gldm_SmallDependenceEmphasis']
    t_model_pkl_filename = 't_stage_model.pkl'
    t_stage_model_pkl = open(t_model_pkl_filename, 'rb')
    t_stage_model = pickle.load(t_stage_model_pkl)
    predictions_t = t_stage_model.predict(features_df)
    print(f"T stage {predictions_t} is predicted for the patient")
    
    relevant_feat_n_list = ['original_shape_Flatness', 'original_shape_Sphericity', 'original_firstorder_Skewness',
                            'metastases']
    n_model_pkl_filename = 'n_stage_model.pkl'
    n_stage_model_pkl = open(n_model_pkl_filename, 'rb')
    n_stage_model = pickle.load(n_stage_model_pkl)
    predictions_n = n_stage_model.predict(features_df)
    print(f"N stage {predictions_n} is predicted for the patient")
    
    # Add PDF creator
    pdfFunction.createPdf()


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





