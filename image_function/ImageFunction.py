#import of modules
import statistics
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





def calculatebackground(x_start, x_stop, y_start, y_stop, array):
    # first get the values and calculate the summed of 3x3 and 4x4
    summed_3 = []
    mean_3 = []

    for i in range((y_stop - y_start)):
        if i + y_start == y_stop - 1:
            break
        for j in range((x_stop - x_start)):
            if j + x_start == x_stop - 1:
                break
            sum = 0
            for ii in range(3):
                for jj in range(3):
                    sum = sum + array[i + y_start + ii, j + x_start + jj]
            #         print(i+y_start+ii, j+x_start+jj)
            summed_3.append(sum)
            mean_3.append(round(sum / 9, 2))

    mean_of_summed_3 = statistics.mean(summed_3)
    return mean_of_summed_3

def gothrougharray(mean, array):
    # go through reshaped array and calculate the mean values, if it is +- 20 of the mean value --> save it in new array with 0
    # save the whole 3x3 area?? or just the single pixel value?
    dimensions = array.shape
    substract_array = numpy.zeros((dimensions[0], dimensions[1]))

    for i in range(0, dimensions[0], 3):
        if i >= dimensions[0]-3:
            break
        for j in range(0, dimensions[1], 3):
            if j >= dimensions[1]-3:
                break
            sum = 0
            for ii in range(3):
                for jj in range(3):
                    sum = sum + array[i + ii, j + jj]

            # hier am besten auch mit Prozentzahlen arbeiten!
            if sum > (mean+(mean*0.3)) or sum < (mean-(mean*0.3)):
                # wenn es außerhalb des Bereiches ist soll an dem 0 array was verändert werden!
                for ii in range(3):
                    for jj in range(3):
                        substract_array[i+ii, j+jj] = array[i+ii, j+jj]



    return substract_array



#track_lines
def _track_line_while(x,y, array_wo_bg, total_coordinates):
    # with this we don´t have a restriction of 1000 anymore!!
    coordinates_x = []
    coordinates_y = []

    coordinates_x.clear()
    coordinates_y.clear()

    arr = array_wo_bg
    dimension = arr.shape
    # calculate the rest of the image to avoid out_of_range error
    if (len(arr[0]) - x) > 2:
        x_max = 3
    else:
        x_max = len(arr[0]) + 1 - x

    # different approach
    while x < dimension[1]-1:
        value = 0
        value_x = 0
        value_y = 0
        # do you calculations here!
        for i in range(1, x_max):
            for j in range(-3, 4):
                # try and except because in case of the corner regions of the image you get an error (index out of region)
                # ich muss hier einbauen, das wir nicht ins negative gehen können!
                if y + j < 0:
                    continue
                try:
                    new_value = arr[y + j, x + i]
                except:
                    new_value = 0
                if new_value > value:
                    value = new_value
                    value_x = x + i
                    value_y = y + j

        if value == 0:
            if len(coordinates_x) > 4:
               # return
                plt.plot(coordinates_x, coordinates_y)
               # all_lines_x.append(coordinates_x)
                # diese punkte können dann auch gerne in total aufgenommen werden, da sie ja auch wirklich geplottet werden
                for ele in range(len(coordinates_x)):
                    total_coordinates.append(str(coordinates_x[ele]) + " " + str(coordinates_y[ele]))
                return coordinates_x, coordinates_y
            return None, None

        coordinates_x.append(value_x)
        coordinates_y.append(value_y)
       # print(value_x)
      #  print(value)
        x = value_x
        y = value_y

        str_to_search = str(value_x) + " " + str(value_y)
        # wenn der punkt in total_coordinates ist dann können wir direkt aufhören mit der Suche, wenn der trace auch noch sehr klein ist!
        if str_to_search in total_coordinates and len(coordinates_x) < 5:
            return None, None
        # if the trace is longer or equal to 5 than we can save it and plot it!
        # actually we can break the algorithm than from here and just go to the one below, plot it and save it!
        if str_to_search in total_coordinates and len(coordinates_x) >= 5:
            break



    if len(coordinates_x) > 4:
        # nur wenn eine mindestanzahl an punkten drinnen ist soll das ganze geplottet werden
        coordinates_x.pop(-1)
        coordinates_y.pop(-1)
        plt.plot(coordinates_x, coordinates_y)

        # diese punkte können dann auch gerne in total aufgenommen werden, da sie ja auch wirklich geplottet werden
        for ele in range(len(coordinates_x)):
            total_coordinates.append(str(coordinates_x[ele])+" "+str(coordinates_y[ele]))
        return coordinates_x, coordinates_y


#_track_line_while(2, 116, array_wo_bg)
#print(coordinates_x)
#print(coordinates_y)








def automatic_track(array_wo_bg):
    all_lines_x = []
    all_lines_y = []
    total_coordinates = []

    dimensions = array_wo_bg.shape

    # ich muss hier dringend einbauen, das man nicht über die Grenze von - kommt!

    for j in range(0, dimensions[1]-2, 2):
        for i in range(0, dimensions[0]-2, 2):
            print(j)
            if array_wo_bg[i,j] > 0:
                #if it is bigger than 0 than we can look for a line!
                # check for 6 values in front of i,j if there are values!
                # if there are >= 3 than we say ok! --> we can change that variable later on
                count = 0
                for jj in range(1,3,1):
                    for ii in range(-1,2,1):
                        # check again that we don´t get errors here!
                        try:
                            value = array_wo_bg[i + ii, j + jj]
                        except:
                            value = 0

                        if value > 0:
                            count = count+1
                        # check how many values there are actually filled, to check if we should check track_line
                if count > 4:
                    # if we count more than 3 values than we go for it!
                    # check for the start points!
                    try:
                        coordinate_x, coordinate_y = _track_line_while(j,i,array_wo_bg, total_coordinates)
                      #  print(type(coordinate_x))
                    except:
                        print("wrong")
                    if coordinate_x != None:
                        all_lines_x.append(coordinate_x[:])
                        all_lines_y.append(coordinate_y[:])

    # nested list with all the informations are returned and can then be used for final image
   # print(all_lines_x)
    return all_lines_x, all_lines_y














































