#import of modules
import re
import glob
from tkinter import filedialog
import lumicks.pylake as lk

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


def _select_h5_file():
    # open the browser to select your file
    filename = filedialog.askopenfilename(title="Which file do you want to convert")
    # open the browser to select the saving directory
    save_folder = filedialog.askdirectory(title="Select folder for Save")
    # convert the h5 to tiff and saves it
    _convert_h5totiff(filename, save_folder)


def _select_h5_directory():
    # open the browser to select the directory with your files
    target_directory = filedialog.askdirectory(title="Select folder with files you want to convert")
    # open the browser to select the saving directory
    saving_directory = filedialog.askdirectory(title="Select folder to save Tiffs in")
    # iterate through every single file in the target_directory, convert the image and saves it in the saving_directory
    files = glob.glob(target_directory+"/*")
    for filenames in files:
        # get name of the h5 file
        final_filename = target_directory+"/"+filenames[len(target_directory)+1:]
        # convert the h5 to tiff and saves it
        _convert_h5totiff(final_filename, saving_directory)
