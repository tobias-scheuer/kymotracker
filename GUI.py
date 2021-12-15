#import of modules
import tkinter
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
import re
import matplotlib.pyplot as plt
import numpy
from skimage import io
from tkinter import filedialog
import lumicks.pylake as lk
from tkinter.ttk import Frame
from tkinter import RAISED
from image_function import ImageFunction
from file_function import FileFunction
from analysis_function import AnalysisFunction

filename = ""
# global variable
original_arr = numpy.array(1)
threshold_arr = numpy.array(1)
reshaped_arr = numpy.array(1)
mean_arr = numpy.array(1)
edge_arr = numpy.array(1)
substract_arr = numpy.array(1)
track_arr = numpy.array(1)

array_used = ""
coordinates_x = []
coordinates_y = []
all_lines_x = []
all_lines_y = []
# for the manual_track to check whether keyboard is pressed!
m = "up"
bind = "down"
pick = 2
start_index = 0
end_index = 0
start_ind = numpy.array([1])
#print(start_ind)

# new try
gl_xdata = numpy.array([])
gl_ydata = numpy.array([])
gl_start_index = 0
gl_end_index = 0
clicked = "first"



# basic stuff of tkinter
# with tkinter you can build your GUI (Graphic User Interface)
root = tkinter.Tk()
# title of your program
root.wm_title("Kymograph Analysis")

#with that you can get the actual dimensions of your screen!
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
#print(screen_height, screen_width)
#root.attributes("-fullscreen", True)  # substitute `Tk` for whatever your `Tk()` object is called

# you could change the geometry of your GUI to a fixed size
geo = str(screen_width) + "x" + str(screen_height)
root.geometry(geo)
# root.minsize('800x400')

frame_top = Frame(root)
frame_top.grid(column=0, row = 0, columnspan=2)
frame_left = Frame(root, relief=RAISED, borderwidth=1)
frame_left.grid(column=0, row = 1, sticky=tkinter.N + tkinter.E + tkinter.W +tkinter.S, padx = 10, pady=10, ipady=10)
frame_right = Frame(root, relief=RAISED, borderwidth=1)
frame_right.grid(column=1, row= 1, sticky= tkinter.N + tkinter.W + tkinter.E + tkinter.S, pady = 10, ipady= 10)


root.grid_rowconfigure(1, minsize=screen_height*0.7)
root.grid_columnconfigure(0, minsize=screen_width*(4/5))
root.grid_columnconfigure(1, minsize=screen_width*(1/5))










def choose_array():
    global array_used, original_arr, threshold_arr, reshaped_arr, mean_arr, edge_arr, substract_arr, track_arr
    print(array_used)
    if array_used == "original_array":
        working_array = original_arr
    if array_used == "threshold_array":
        working_array = threshold_arr
    if array_used == "reshaped_array":
        working_array = reshaped_arr
    if array_used == "mean_array":
        working_array = mean_arr
    if array_used == "edge_array":
        working_array = edge_arr
    if array_used == "substract_array":
        working_array = substract_arr
    if array_used == "track_array":
        working_array = track_arr
    return working_array


def _add_kymo_info():
    kymo_filename = filedialog.askopenfilename()
    h5file = lk.File(kymo_filename)

    name, kymo = h5file.kymos.popitem()
    Lb.insert(1, "Linetime in sec: "+str(kymo.line_time_seconds))
    Lb.insert(2, "pixelsize in µm: "+str(kymo.pixelsize_um))




def add_path():
    pathname = tkinter.simpledialog.askstring("pathname", "add your pathname")

    # print(Lb.get(0, "end").index("Kymo"))
    Lb.insert(100000, pathname)
    global coordinates_x
    coordinates_x.clear()
    global coordinates_y
    coordinates_y.clear()



def distance_beads():
    start = tkinter.simpledialog.askinteger("start value", "add upper pixel value")
    stop = tkinter.simpledialog.askinteger("stop value", "add lower pixel value")
    Lb.insert(3, "distance: " + str(stop-start))



def del_point():
    selected = Lb.curselection()
    # finds the index in the list
    Lb.delete(selected[0])

def func(self, _event=None):
    # same function but with single key
    selected = Lb.curselection()
    # find the index in the list
    Lb.delete(selected[0])



def on_move(event):
    # works fine when fig. is defined (maybe has to define it all the time new
    # but after zooming in or so it doesn´t work anymore
    global m
    # wenn m == 0 also m runtergedrückt, dann tracke sonst nicht!
    if m == "down":
        global ix, iy
        # save fig also as a global variable!
        ix, iy = event.xdata, event.ydata
        print ("x="+str(ix)+" y="+str(iy))

        if coordinates_x[-1] != int(ix):
            coordinates_x.append(int(ix))
            coordinates_y.append(int(iy))


def manual_track(event=None):
    global figure
    # why did i append here 0 first? maybe because of coordinates_x[-1] --> else error?
    coordinates_x.append(0)
    coordinates_y.append(0)
    root.bind('<KeyPress>', down)
    root.bind('<KeyRelease>', up)
    figure.canvas.mpl_connect("motion_notify_event", on_move)

def down(e):
    global m
    if m == "up":
        print ('Down\n', e.char, '\n', e)
        #global m
        m = "down"
        #while m = 1 i can do something otherwise not?
        #e.g. track motion!

def up(e):
    global m
    if m == "down":
        print ('Up\n', e.char, '\n', e)
       # global m
        m = "up"

def choose_path():
    global bind
    if bind == "down":
        button_choose_path.configure(borderwidth=5)
        bind = "up"
        root.bind('<KeyPress>', down)
        root.bind('<KeyRelease>', up)
    else:
        button_choose_path.configure(borderwidth=2)
        bind="down"
        root.unbind('<KeyPress>')


def add_man_track():
  #  working_array = choose_array()

 #   _clear_without_numpy()

 #   fig = plt.figure(figsize=(10, 4))
 #   global figure, coordinates_y, coordinates_x
 #   figure = fig
    # create the new figure in canvas with toolbar
#    plt.imshow(working_array)
    # because we appended a 0 here!
    coordinates_x.pop(0)
    coordinates_y.pop(0)
    for i in range(len(coordinates_x)):
        Lb.insert(100000, str(coordinates_x[i]) + " "+ str(coordinates_y[i]))
 #   plt.plot(coordinates_x, coordinates_y)
    all_lines_x.append(coordinates_x[:])
    all_lines_y.append(coordinates_y[:])
    print(all_lines_x)
    plt.title("tracks")
    plt.colorbar()
    plt.xlabel("x-axis")
    plt.ylabel("y-axis")
 #   canvas = FigureCanvasTkAgg(fig, master=frame_left)
 #   canvas.draw()
  #  canvas.get_tk_widget().pack(side=tkinter.TOP, fill=tkinter.BOTH)

 #   toolbar = NavigationToolbar2Tk(canvas, frame_top)
  #  toolbar.update()

  #  global overall_canvas, overall_toolbar, track_arr
  #  overall_canvas = canvas
 #   overall_toolbar = toolbar
    print(array_used)
    coordinates_y.clear()
    coordinates_x.clear()


def show_paths():
    # get the info from Lb and recreates it into a plot.
    # all infos are in Lb (Threshold, size, ...)
    # maye this is something for later
    _clear_without_numpy()

    fig = plt.figure(figsize=(10, 4))
    global figure, original_arr
    figure = fig
    # create the new figure in canvas with toolbar
    plt.imshow(original_arr)

    path_coordinates_x = []
    path_coordinates_y = []
    x_size = 0
    y_size = 0

    data = Lb.get(0, tkinter.END)
    for ele in data:
        if "Size changed" in ele:
            values = re.split(": |-| ", ele)
            x_size = int(values[3])
            y_size = int(values[6])
            print(x_size, y_size)
        elif "path" in ele:
            print(path_coordinates_x)
            number = ele.split("h")
            print(number)
            label = int(number[1])-1
            print(label)
            if len(path_coordinates_x) > 0:
                plt.plot(path_coordinates_x, path_coordinates_y, label=label)
            path_coordinates_x.clear()
            path_coordinates_y.clear()
        elif "Threshold" in ele or "Mean" in ele or "Background" in ele or "Edge" in ele or "C:" in ele:
            continue
        else:
            coor = ele.split(" ")
            path_coordinates_x.append(x_size + int(coor[0]))
            path_coordinates_y.append(y_size + int(coor[1]))


    if len(path_coordinates_x) > 0:
        plt.plot(path_coordinates_x, path_coordinates_y, label=label+1)

    plt.legend()
    plt.title("tracks")
    plt.colorbar()
    plt.xlabel("x-axis")
    plt.ylabel("y-axis")
    canvas = FigureCanvasTkAgg(fig, master=frame_left)
    canvas.draw()
    canvas.get_tk_widget().pack(side=tkinter.TOP, fill=tkinter.BOTH)

    toolbar = NavigationToolbar2Tk(canvas, frame_top)
    toolbar.update()

    global overall_canvas, overall_toolbar, track_arr
    overall_canvas = canvas
    overall_toolbar = toolbar

    index = Lb.get(0, "end").index(data[-1])
    print(data)
    for ele in data:
        if "path" in ele:
            index = Lb.get(0, "end").index(ele)
            #get the index of it
            print(index)
    print("show paths!")


# tkinter window design
# create the first empty window!
fig = plt.figure(figsize=(10, 4))

canvas = FigureCanvasTkAgg(fig, master=frame_left)
canvas.draw()

toolbar = NavigationToolbar2Tk(canvas, frame_top)
toolbar.update()
canvas.get_tk_widget().pack(side=tkinter.TOP, fill=tkinter.BOTH)

overall_canvas = canvas
overall_toolbar = toolbar



# brauche ich die drei wirklich?
#canvas.mpl_connect("key_press_event", on_key_press)

#cid = fig.canvas.mpl_connect('button_press_event', onclick)

var = tkinter.IntVar()


# all the buttons, listbox and elements
button_add_info = tkinter.Button(frame_right, text="add info", command=_add_kymo_info)
button_add_info.grid(column=0, row = 0, sticky=tkinter.E + tkinter.W)

button_add_dist = tkinter.Button(frame_right, text="add dist", command=distance_beads)
button_add_dist.grid(column=0, row = 1, sticky=tkinter.E + tkinter.W)

button_add_path = tkinter.Button(frame_right, text="add path", command=add_path)
button_add_path.grid(column=0, row = 2, sticky=tkinter.E + tkinter.W)

frame_right.grid_rowconfigure(3, minsize=10)

button_choose_path = tkinter.Button(frame_right, text="choose path", command=choose_path)
button_choose_path.grid(column=0, row = 4, sticky=tkinter.E + tkinter.W)

button_track_manual = tkinter.Button(frame_right, text="manual tracking", command=manual_track)
button_track_manual.grid(column=0, row = 5, sticky=tkinter.E + tkinter.W)

button_track_manual = tkinter.Button(frame_right, text="add man track", command=add_man_track)
button_track_manual.grid(column=0, row = 6, sticky=tkinter.E + tkinter.W)

#frame_right.grid_rowconfigure(6, minsize=10)

button_delete = tkinter.Button(frame_right, text="delete", command=del_point)
button_delete.grid(column=0, row = 7, sticky=tkinter.E + tkinter.W)

button_show_paths = tkinter.Button(frame_right, text="show paths", command=show_paths)
button_show_paths.grid(column=0, row=8, sticky=tkinter.E + tkinter.W)


# triggers a reaction after keyboard click "f"
button_f = tkinter.Button(root, text="Hello", command=func)
root.bind('f', func)


#frame_right.grid_rowconfigure(8, minsize=100)


Lb = tkinter.Listbox(frame_right)
Lb.grid(column=1, row = 0, rowspan=20, sticky=tkinter.N + tkinter.W + tkinter.E)



frame_right.grid_columnconfigure(1, minsize=150)

frame_height = frame_right.winfo_screenheight()
button_add_path.winfo_screenheight()
print(button_add_path.winfo_screenheight())
print(frame_height)
frame_right.grid_rowconfigure(10, minsize=frame_height*0.6)

def new_plt(arr, title, arr_used):
    # create a new figure
    fig = plt.figure(figsize=(10, 4))
    global figure
    figure = fig
    # create the new figure in canvas with toolbar
    plt.imshow(arr)
    plt.title(title)
    plt.colorbar()
    plt.xlabel("x-axis")
    plt.ylabel("y-axis")
    canvas = FigureCanvasTkAgg(fig, master=frame_left)
    canvas.draw()
    canvas.get_tk_widget().pack(side=tkinter.TOP, fill=tkinter.BOTH)

    toolbar = NavigationToolbar2Tk(canvas, frame_top)
    toolbar.update()
#    canvas.get_tk_widget().pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=True)


    global overall_canvas, overall_toolbar, array_used
    overall_canvas = canvas
    overall_toolbar = toolbar
    array_used = arr_used
    print(array_used)

def _clear():
    # destroy the old canvas and toolbar
    overall_canvas.get_tk_widget().destroy()
    overall_toolbar.destroy()
    # destroy the old array
    global original_arr
    original_arr = numpy.array(1)

def load_image():
    # ask first if you want to save the results!
    print(Lb.get(0, tkinter.END))
    if str(Lb.get(0, tkinter.END)) != "()":
        result = tkinter.messagebox.askyesno(title="Do you want to save?", message="Do you want to save your results?")
        if result == True and filename == "":
            save_as()
        if result ==  True and filename != "":
            save()

    # automatically deletes the old canvas and toolbar!
    _clear()
    # clear the whole LB list
    Lb.delete(0, tkinter.END)

    # load the file you want to analyse
    filename1 = filedialog.askopenfilename()

    # add path of file to the listbox
    Lb.insert(0, filename1)
    #Lb.insert(4, "path1")

    # creates a new figure
    im = io.imread(filename1)

    # default color = green = 1 and creates an numpy array with green color
    color = 1
    Y = int(len(im))
    X = len(im[0])
    new_array = numpy.zeros((Y, X))
    for i in range(len(im)):
        for j in range(len(im[0])):
            new_array[i, j] = im[i, j, color]

    global original_arr
    original_arr = new_array
    # display the picture as an canvas with toolbar
    new_plt(new_array, "green plot", "original_array")


def save():
    # select the directory
    global filename
    if filename == "":
        filename1 = filedialog.asksaveasfilename(title="Save file", defaultextension=".txt",
                                        filetypes=[("text file", "*.txt")])
        filename = filename1

    # check if we already have an filename!
    #
    data = Lb.get(0, tkinter.END)
    try:
        with open(str(filename), "r") as result:
            text = result.read()
    except:
        text = ""
    with open(filename, "w") as result:
        result.write(text + "\n\n" + str(data))


def save_as():
      #  folder = filedialog.askdirectory()
    filename1 = filedialog.asksaveasfilename(title="Save file", defaultextension=".txt",
                                               filetypes=[("text file", "*.txt")])
    global filename
    filename = filename1
      # check if we already have an filename!

    data = Lb.get(0, tkinter.END)
    try:
        with open(str(filename), "r") as result:
            text = result.read()
    except:
        text=""
    with open(filename, "w") as result:
        result.write(text + "\n\n" + str(data))


def _clear_without_numpy():
    # destroy the old canvas and toolbar
    overall_canvas.get_tk_widget().destroy()
    overall_toolbar.destroy()


# function to change the size of the numpy array
def change_size(start_x, stop_x, start_y, stop_y):
    #decide what should be the array to work with
    global reshaped_arr
    working_array = choose_array()


    # delete the old canvas and toolbar
    _clear_without_numpy()
    data = Lb.get(0, tkinter.END)
    index = Lb.get(0, "end").index(data[-1])
    Lb.insert(100000, "Size changed X: "+str(start_x)+"-"+str(stop_x)+" Y: "+str(start_y)+"-"+str(stop_y))

    # either take the threshold version or the original array (depends on if threshold was applied)!
    # maybe always save it as original_arr




    # create the reshaped numpy array
    reshaped_array = numpy.zeros(((stop_y - start_y), (stop_x - start_x)))
    for i in range((stop_y - start_y)):
        for j in range((stop_x - start_x)):
            reshaped_array[i, j] = working_array[i + start_y, j + start_x]


    reshaped_arr = reshaped_array
    # create the new figure in canvas with toolbar
    new_plt(reshaped_array, "Reshaped Array", "reshaped_array")


def _size():
    # creating a tkinter window
    filewin = tkinter.Toplevel(root)
    label = tkinter.Label(filewin, text="Choose your prefered size: ")
    label.grid(row=0, column=0, columnspan=2)
    label1 = tkinter.Label(filewin, text="Start X-axis: ")
    label1.grid(row=1, column=0)
    start_x = tkinter.Entry(filewin)
    start_x.grid(row=1, column=1)

    label2 = tkinter.Label(filewin, text="Stop X-axis: ")
    label2.grid(row=2, column=0)
    stop_x = tkinter.Entry(filewin)
    stop_x.grid(row=2, column=1)

    label3 = tkinter.Label(filewin, text="Start Y-axis: ")
    label3.grid(row=3, column=0)
    start_y = tkinter.Entry(filewin)
    start_y.grid(row=3, column=1)

    label4 = tkinter.Label(filewin, text="Stop Y-axis: ")
    label4.grid(row=4, column=0)
    stop_y = tkinter.Entry(filewin)
    stop_y.grid(row=4, column=1)

    button = tkinter.Button(filewin, text="Apply", command=lambda: change_size(int(start_x.get()), int(stop_x.get()), int(start_y.get()), int(stop_y.get())))
    button.grid(row=5, column=1)


def change_threshold(threshold_value, arr):
    global threshold_arr
    working_array = choose_array()

    # first destroy the old canvas and toolbar
    _clear_without_numpy()
    #einfach immer an den Schluss setzen!!
    data = Lb.get(0, tkinter.END)
    index = Lb.get(0, "end").index(data[-1])
    Lb.insert(100000, "Threshold: "+ str(threshold_value))
    # create your new numpy.array with the desired threshold
    threshold_array = working_array
    for i in range(len(threshold_array)):
        for j in range(len(threshold_array[0])):
            #print(arr[i,j])
            if threshold_array[i, j] < threshold_value:
                threshold_array[i, j] = 0


    threshold_arr = threshold_array
    # display the picture as an canvas with toolbar
    title = "Threshold = "+ str(threshold_value)
    new_plt(threshold_array, title, "threshold_array")


def _threshold():
    threshold = tkinter.simpledialog.askinteger("Threshold", "Choose your preferred Threshold")
    change_threshold(threshold, original_arr)


def choose_color(color):
    # automatically deletes the old canvas and toolbar and numpy array
    _clear_without_numpy()
    filename1 = Lb.get(0)
    # creates a new figure
    im = io.imread(filename1)

    # creates a new numpy array depending on the color you choosed
    Y = int(len(im))
    X = len(im[0])
    new_array = numpy.zeros((Y, X))
    for i in range(len(im)):
        for j in range(len(im[0])):
            new_array[i, j] = im[i, j, color]


    global original_arr
    original_arr = new_array

    if color == 0:
        title = "red plot"
    if color == 1:
        title = "green plot"
    if color == 2:
        title = "blue plot"

    new_plt(new_array, title, "original_array")


def mean_filter():
    # choose array
    global mean_arr
    working_array = choose_array()

    _clear_without_numpy()
    data = Lb.get(0, tkinter.END)
    index = Lb.get(0, "end").index(data[-1])
    Lb.insert(100000, "Mean Filter")
    dimensions = working_array.shape
    #  print(dimensions)
    mean_array = numpy.zeros((dimensions[0], dimensions[1]))
    #mean_arr = reshaped_array
    #  print(2)
    for i in range(1, dimensions[0]-2, 1):
        for j in range(1, dimensions[1]-2, 1):
            #  von dem punkt aus die area um den punkt ausrechnen!
            sum = 0
            for ii in range(-1,2,1):
                for jj in range(-1,2,1):
                    sum = sum + working_array[i + ii, j + jj]

            mean_array[i,j] = int(sum/9)


    mean_arr = mean_array
    new_plt(mean_array, "mean filter", "mean_array")


def edge_finding():
    # choose array
    global edge_arr
    working_array = choose_array()

    _clear_without_numpy()
    data = Lb.get(0, tkinter.END)
    index = Lb.get(0, "end").index(data[-1])
    Lb.insert(100000, "Edge Detection")
    arr = working_array
    #arr = reshaped_array
    dimensions = arr.shape
    edge_array = numpy.zeros((dimensions[0], dimensions[1]))
    # maybe change the variables!
    m = -2
    var_array = numpy.array([[m, m, m],[m, 16, m],[m, m, m]])
    print(var_array)
    # then go through the normal array and calculate all values!
    for i in range(1, dimensions[0] - 1, 1):
        for j in range(1, dimensions[1] - 1, 1):
            sum = 0
            for ii in range(-1,2,1):
                for jj in range(-1,2,1):
                    sum = sum + (arr[i + ii, j + jj] * var_array[ii+1,jj+1])
            if sum < 0:
                sum = 0
            if sum > 500:
                sum = 500
            edge_array[i,j] = sum

    edge_arr = edge_array
    new_plt(edge_array, "edge", "edge_array")


def substract_background(x_start, x_stop, y_start, y_stop):
    # choose array
    working_array = choose_array()

    _clear_without_numpy()
    data = Lb.get(0, tkinter.END)
    index = Lb.get(0, "end").index(data[-1])
    Lb.insert(100000,
              "Background X: " + str(x_start) + "-" + str(x_stop) + " Y: " + str(y_start) + "-" + str(y_stop))

    mean_bg = ImageFunction.calculatebackground(x_start, x_stop, y_start, y_stop, working_array)
    substract_array = ImageFunction.gothrougharray(mean_bg, working_array)
    new_plt(substract_array, "substracted background", "substract_array")


    global substract_arr
    substract_arr = substract_array


def background_size():
    # creating a tkinter window
    filewin = tkinter.Toplevel(root)
    label = tkinter.Label(filewin, text="Choose area of background: ")
    label.grid(row=0, column=0, columnspan=2)
    label1 = tkinter.Label(filewin, text="Start X-axis: ")
    label1.grid(row=1, column=0)
    start_x = tkinter.Entry(filewin)
    start_x.grid(row=1, column=1)

    label2 = tkinter.Label(filewin, text="Stop X-axis: ")
    label2.grid(row=2, column=0)
    stop_x = tkinter.Entry(filewin)
    stop_x.grid(row=2, column=1)

    label3 = tkinter.Label(filewin, text="Start Y-axis: ")
    label3.grid(row=3, column=0)
    start_y = tkinter.Entry(filewin)
    start_y.grid(row=3, column=1)

    label4 = tkinter.Label(filewin, text="Stop Y-axis: ")
    label4.grid(row=4, column=0)
    stop_y = tkinter.Entry(filewin)
    stop_y.grid(row=4, column=1)

    button = tkinter.Button(filewin, text="Apply", command=lambda: substract_background(int(start_x.get()), int(stop_x.get()), int(start_y.get()), int(stop_y.get())))
    button.grid(row=5, column=1)


def automatic_track():
    # choose array
    global all_lines_x, all_lines_y
    working_array = choose_array()

    _clear_without_numpy()
    new_all_lines_x, new_all_lines_y = ImageFunction.automatic_track(working_array)
    all_lines_x = new_all_lines_x
    all_lines_y = new_all_lines_y
   # print(all_lines_x)
    #print(all_lines_y)

    fig = plt.figure(figsize=(10, 4))
    global figure
    figure = fig
    # create the new figure in canvas with toolbar
    plt.imshow(working_array)

    for i in range(len(new_all_lines_x)):
        plt.plot(new_all_lines_x[i], new_all_lines_y[i], picker=True, label=i)

    plt.title("tracks")
    plt.colorbar()
    plt.xlabel("x-axis")
    plt.ylabel("y-axis")
    canvas = FigureCanvasTkAgg(fig, master=frame_left)
    canvas.draw()
    canvas.get_tk_widget().pack(side=tkinter.TOP, fill=tkinter.BOTH)

    toolbar = NavigationToolbar2Tk(canvas, frame_top)
    toolbar.update()

    def on_pick(event):
        global pick, start_index, end_index, start_ind, gl_xdata, gl_ydata
        print("onpick")
        thisline = event.artist
        xdata = thisline.get_xdata()
        ydata = thisline.get_ydata()

        if m == "down":
            print("pick first value")
            if clicked == "first":
                gl_xdata = xdata
                gl_ydata = ydata

            # just check if you picked the correct one
            if clicked == "second":
                comparison = gl_xdata == xdata
                if comparison.all() == False:
                    tkinter.messagebox.showinfo(title="Warning",
                                                message="You did not pick the same path?")

        if m == "up":
            gl_xdata = xdata
            gl_ydata = ydata

        fig.canvas.draw()

    def onclick(event):
        global start_ind, gl_xdata, gl_ydata, clicked, gl_start_index, gl_end_index
        print("onclicked")
        ix, iy = event.xdata, event.ydata
        # if it is a double click
        if m == "up":
            for i in range(len(gl_xdata)):
                Lb.insert(100000, str(int(gl_xdata[i])) + " " + str(int(gl_ydata[i])))

        else:
            if clicked == "first":
                print("first")
                for i in range(len(gl_xdata)):
                    if ix <= int(gl_xdata[i]):
                        gl_start_index = i
                        print(i)
                        clicked = "second"
                        break
            else:
                print("second")
                for i in range(len(gl_xdata)):
                    if ix <= int(gl_xdata[i]) or i == len(gl_xdata)-1:
                        gl_end_index = i
                        clicked = "first"
                        if gl_start_index < gl_end_index:
                            for i in range(gl_end_index-gl_start_index):
                                data = Lb.get(0, tkinter.END)
                                index = Lb.get(0, "end").index(data[-1])
                                Lb.insert(100000, str(int(gl_xdata[gl_start_index + i])) + " " +
                                          str(int(gl_ydata[gl_start_index + i])))

                        print(i)
                        break

    fig.canvas.callbacks.connect('pick_event', on_pick)
    fig.canvas.mpl_connect('button_press_event', onclick)
    # could do that again with butt on press m = 1

    global overall_canvas, overall_toolbar, track_arr
    overall_canvas = canvas
    overall_toolbar = toolbar
    track_arr == working_array
    array_used = "track_array"
    print(array_used)


def reload():
    # automatically deletes the old canvas and toolbar and numpy array
    _clear_without_numpy()
    filename1 = Lb.get(0)
    # creates a new figure
    im = io.imread(filename1)

    # creates a new numpy array depending on the color you choosed
    new_array = numpy.zeros((len(im), len(im[0])))
    for i in range(len(im)):
        for j in range(len(im[0])):
            new_array[i, j] = im[i, j, 1]

    global original_arr
    original_arr = new_array

    new_plt(new_array, "green plot", "original_array")

# menubar with elements
# filemenu
menubar = tkinter.Menu(root)
filemenu = tkinter.Menu(menubar, tearoff=0)
filemenu.add_command(label="Load Image", command=load_image)
filemenu.add_command(label="Save", command=save)
filemenu.add_command(label="Save as", command=save_as)
filemenu.add_command(label="Export Results")
filemenu.add_command(label="Clear")
filemenu.add_command(label="Exit")
filemenu.add_command(label="Undo")
filemenu.add_separator()

submenu = tkinter.Menu(filemenu)
submenu.add_command(label="Single File", command=FileFunction._select_h5_file) # lambda to pass arguments to functions
submenu.add_command(label="Folder", command=FileFunction._select_h5_directory)
filemenu.add_cascade(label='H5 to Tiff', menu=submenu, underline=0)

menubar.add_cascade(label="File", menu=filemenu)

# imagemenu
imagemenu = tkinter.Menu(menubar, tearoff=0)

imagemenu.add_command(label="Cut")
menubar.add_cascade(label="Image", menu=imagemenu)

imagemenu.add_command(label="Threshold", command=_threshold)
imagemenu.add_command(label="Change size", command=_size)
imagemenu.add_command(label="Mean Filter", command=mean_filter)
imagemenu.add_command(label="Substract Background", command=background_size)
imagemenu.add_command(label="Edge Detection", command=edge_finding)
imagemenu.add_command(label="automatic tracking", command=automatic_track)
imagemenu.add_command(label="reload original image", command=reload)

submenu = tkinter.Menu(imagemenu)
submenu.add_command(label="Red", command= lambda : choose_color(0)) # lambda to pass arguments to functions
submenu.add_command(label="Green", command= lambda : choose_color(1))
submenu.add_command(label="Blue", command= lambda : choose_color(2))
imagemenu.add_cascade(label='Color', menu=submenu, underline=0)

def analyse_results(analysis):
    #fileorder = filedialog.askopenfile()
    # ask for the file and then go through it with your functions!
    filename = filedialog.askopenfilename()
    AnalysisFunction.starting_function(filename, analysis)
    # find a way to extract all the informations into an Excel file!

# analysismenu
analysismenu = tkinter.Menu(menubar, tearoff=0)
analysismenu.add_command(label="Position on DNA", command=lambda: analyse_results("position"))
analysismenu.add_command(label="Duration on DNA", command=lambda: analyse_results("duration"))
analysismenu.add_command(label="Movement on DNA", command=lambda: analyse_results("movement"))
analysismenu.add_command(label="Pos.; Dur.; Mov.", command=lambda: analyse_results("all"))
menubar.add_cascade(label="Analysis", menu=analysismenu)


root.config(menu=menubar)

button_f = tkinter.Button(root, text="Hello")
#root.bind('f', func)

tkinter.mainloop()