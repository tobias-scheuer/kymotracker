#import of modules
import tkinter
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.backend_bases import key_press_handler
import re
import glob
import matplotlib.pyplot as plt
import numpy
from skimage import io
from tkinter import filedialog
import lumicks.pylake as lk
from tkinter.ttk import Frame, Button, Style
from tkinter import Tk, RIGHT, BOTH, RAISED


# functions to convert h5 files into tiff files or do it with complete folders!
def _convert_h5totiff(filename, save_folder):
    # grabs the desired file
    h5file = lk.File(filename)
    # modifies the filename
    filename = filename[0:-3]
    index = [m.start() for m in re.finditer("/", filename)]
    filename = filename[index[-1]+1:]
    # saves the h5 file as a tiff
    name, kymo = h5file.kymos.popitem()
    kymo.save_tiff(save_folder + "//"+filename+".tiff")


def _select_file():
    # open the browser to select your file
    filename = filedialog.askopenfilename(title="Which file do you want to convert")
    # open the browser to select the saving directory
    save_folder = filedialog.askdirectory(title="Select folder for Save")
    _convert_h5totiff(filename, save_folder)
    # saying that stuff will be saved as the h5 file!


def _select_direct():
    # open the browser to select your directory
    fileorder = filedialog.askdirectory(title="Select folder with files you want to convert")
    # open the browser to select the saving directory
    save_folder = filedialog.askdirectory(title="Select folder to save Tiffs in")
    # ask ones for the save folder! and then iterate through every single file in that folder
    files = glob.glob(fileorder+"/*")
    liste = []
    for filenames in files:
        #erst stutzen und dann gucken sobald etwas kommt, was nicht in Liste ist
        final_filename = fileorder+"/"+filenames[len(fileorder)+1:]
        #substract file order (len(fileorder)
        _convert_h5totiff(final_filename, save_folder)












