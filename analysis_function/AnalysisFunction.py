import statistics
import matplotlib.pyplot as plt
import numpy as np

class KymoAnalysisTools():
    def __init__(self):
        pass

    def create_lists(self):
        pass

    def show_all(self):
        pass

    def start_point(self):
        pass

    def duration_of_stay(self):
        pass

    def track_movement(self):
        pass

    def plot_histogramm(self, data: list, xlabel_name: str, ylabel_name: str):
        plt.hist(data, color="k")
        plt.title("n = " + str(len(data)))
        plt.xlabel(xlabel_name)
        plt.ylabel(ylabel_name)
        plt.show()

    def plot_scatter(self):
        pass





def create_lists(data):
    # this is the function that gets the data from the textfile and convert it into some useful list to work with later on

    # declare some lists to store our data in
    x_coordinates = []
    y_coordinates = []
    kymos = []
    dis = []
    tim = []
    pix = []
    paths = []
    lengths = []

    # because in each kymo we have multiply "proteinpaths" we want to make sure that we track every path only once!
    path = 0
    for lines in data:
        # iterate throught the single lines of the textfile
        if lines[0] == "(":
            # because i also stored some other stuff in the textfile i just want to analyse the lines with my datapoints
            # and this line begins with "("
            # processing of the text line
            lines = lines[1:-2]
            # with this you create a list with the single entries (single datapoints)
            single_items = lines.split(",")
            initial_length = len(x_coordinates)
            # you than iterate through the list
            for i in range(len(single_items)):
                if "Threshold" in single_items[i] or "Mean" in single_items[i]  or "Background" in single_items[i]  \
                        or "Edge" in single_items[i]  or "C:" in single_items[i] or "Size changed" in single_items[i]:
                    continue
                # because we also store information about the kymograph and the name of the kymograph in that line
                # we first want to extract those informations
                if i == 1:
                    # here we check if we already looked for that kymograph, if we did we don´t have to save the information again
                    # that´s because you can multiple time save your kymograph in the textfile
                    if single_items[0] not in kymos:
                        # name of the kymograph
                        kymos.append(single_items[0])

                        # here we save the linetime of the kymograph, but first we do some processing to get the raw number
                        time_line = single_items[1]
                        time_start_pos = time_line.index(":")
                        time_size = time_line[time_start_pos + 2:-1]
                        tim.append(float(time_size))

                        # here we save the pixelsize of the kymograph, but first we do some processing to get the raw number
                        pixel_line = single_items[2]
                        pixel_start_pos = pixel_line.index(":")
                        pixel_size = pixel_line[pixel_start_pos + 3:-2]
                        pix.append(float(pixel_size))

                        # here we save the distance of the beads, but first we do some processing to get the raw number
                        distance_line = single_items[3]
                        dist_start_pos = distance_line.index(":")
                        dist_size = distance_line[dist_start_pos + 2:-1]
                        dis.append(float(dist_size))

                        # with a new kymo we also start with the path 0 so we can put it back to zero
                        path = 0

                # the first 4 entries are just information about the kymo (see above) that we don´t need for our analysis
                # of the coordinates so we skip over the first 4 entries
                if i < 4:
                    continue

                # if the list entry does not contain "path" than we have a coordinate that can be stored in a list
                if single_items[i].find("path") == -1:
                    # append was decleared below and tells you if you should save the path or not
                    # if append == 0 you should save the paths
                    if append == 0:
                        # process the data so we only save the raw numbers
                        white_index = single_items[i].split(" ")
                        raw_x = white_index[1]
                        raw_y = white_index[2]
                        # save the coordinates in the two lists
                        x_coordinates.append(raw_x[1:])
                        y_coordinates.append(raw_y[:-1])

                # if the list entry does contain "path" then we want to end the last path and create a new one!
                else:
                    # this is to get the number of the paths
                    h_index = single_items[i].split("h")
                    number = h_index[1]
                    # here we check if the path of that specific kymo was already tracked or not
                    if path < int(number[:-1]):
                        # reassign the new path to make sure next time we don´t track the same path again
                        path = int(number[:-1])
                        paths.append(int(number[:-1]))
                        # tell the function above that we want to save all following coordinates
                        append = 0
                        # at the beginning of every path we can add a -10 as marker for later processing
                        x_coordinates.append(-10)
                        y_coordinates.append(-10)
                        # save the amount of datapoints in that list, this is important later for the creation
                        # of a numpy array
                        lengths.append(len(x_coordinates)-initial_length)
                    else:
                        # if the path was already saved we don´t want to save the results again
                        append = 1

            # save the amount of datapoints in that list, this is important later for the creation of a numpy array
            lengths.append(len(x_coordinates) - initial_length)


    # find the start positions of the pathes
  #  indices_x = [i for i, x in enumerate(x_coordinates) if x == -10]
  #  indices_y = [i for i, x in enumerate(y_coordinates) if x == -10]

    # create two new 3D arrays for the x and y coordinates filled with value -5
    new_arr_x = np.full((len(kymos),max(paths),max(lengths)), -5)
    new_arr_y = np.full((len(kymos), max(paths), max(lengths)), -5)

    # what the numpy arrays look like
    #[kymo1[paths1[coor]paths2[coor]]
    #kymo2[paths1[coor]paths2[coor]]
    #...
    #kymo16[paths[coor]paths2[coor]]]


    # pops out the first value of the list because it is a -10 and we don´t need it
    x_coordinates.pop(0)
    y_coordinates.pop(0)

    # then we fill our two created numpy arrays "new_arr_x/y" with the kymographs
    already = 0
    kym = -1
    # go through every path
    for i in range(len(paths)):
        # if a new kymograph starts (path1) then start a new kymo (change parameter where to store your data in)
        if paths[i] == 1:
            kym = kym + 1
        # iterate as long as the longest path is
        for j in range(max(lengths)):
            # to find the index of the variables
            index = already + j
            # to avoid error at the end we break the loop if we are at the end
            if index >= len(x_coordinates):
                break
            # if value == -10 (-10 was assigned when a new paths starts) than break the loop
            if x_coordinates[index] == -10:
                # save where we are in the list that in the next loop we start at that position
                already = index+1
                break
            # save the values in the two created numpy arrays
            new_arr_x[kym, paths[i]-1, j] = x_coordinates[index]
            new_arr_y[kym, paths[i]-1, j] = y_coordinates[index]

    # return the following variables
    return x_coordinates, y_coordinates, new_arr_x, new_arr_y, tim, pix, dis



def show_all(arr_x, arr_y):
    # find out the dimensions of the old numpy array to create new ones with the same dimensions
    dimensions = arr_x.shape
    # create new numpy arrays with values -200 because we want to process our data so that they all start at x = 0
    # and y = always +10 of the paths before that
    zerod_arr_x = np.full((dimensions[0], dimensions[1], dimensions[2]), -200)
    zerod_arr_y = np.full((dimensions[0], dimensions[1], dimensions[2]), -200)

    # code to fill up the new arrays with our data
    iteration = -10
    for i in range(len(arr_x)):
        # iterate through the kymos in the numpy array
        for j in range(len(arr_x[i])):
            # iterate through the paths in the numpy array
            for k in range(dimensions[2]):
                # iterate through the single coordinates of the numpy array
                if arr_x[i,j,k] != -5:
                    # if value would be -5 than the paths would be empty, because we set up the last numpy arrray with
                    # -5 values and only changed that value in case we have a paths there, so -5 means the array is
                    # empty or the path ended

                    # because we want to shift the y and x values to a specific number we need to record first what
                    # there actual values are
                    if k == 0:
                        # iteration important for the position of the y value
                        iteration = iteration + 10
                        # find out the actual position
                        back_x = arr_x[i,j,k]
                        back_y = arr_y[i,j,k]

                    # then we save the new values (calculated actual value - the value we have to go back)
                    zerod_arr_x[i,j,k] = arr_x[i,j,k] - back_x
                    zerod_arr_y[i, j, k] = (arr_y[i, j, k] - back_y) + iteration
                else:
                    # if we get the value -5 means either paths ended or the paths is completely empty we break the loop
                    break

    # this is all for plotting only
    # we go just through the newly created array and save the values in the list_x and list_y and then directly
    # plot it, by this we get all plots in one figure
    list_x = []
    list_y = []
    for i in range(len(arr_x)):
        for j in range(len(arr_x[i])):
            if len(list_x) != 0:
                plt.plot(list_x, list_y)
            list_x.clear()
            list_y.clear()
            for k in range(dimensions[2]):
                if arr_x[i, j, k] != -5:
                    list_x.append(zerod_arr_x[i,j,k])
                    list_y.append(zerod_arr_y[i,j,k])
                else:
                    break

    # specify what the plot should look like
    plt.title("Kymographs XPB WT with ATP")
    plt.xlabel("Kymograph number")
    plt.ylabel("distance")
    plt.xlim(0,17500)
    plt.show()

def start_point(arr_x, arr_y, dis1):
    # function to define the starting point on the DNA
    # look for the first entries if there are not -5 and calculate the % on the DNA

    # create a list to store all the final datapoints in
    perc = []
    for i in range(len(arr_y)):
        # go through the kymos
        for j in range(len(arr_y[i])):
            # goes through the paths
            if arr_y[i,j,0] != -5:
                # only if the array is not empty save the value for the starting point
                start_point = arr_y[i,j,0]
                # append to the list the values (start_point/distance_of the specific kymo) rounded to 2 decimal number
                perc.append(round(start_point/dis1[i],2))

    # some specifications about the histogram
    plt.hist(perc, color="k")
    plt.title("n = "+ str(len(perc)))
    plt.xlabel("pos. on DNA")
    plt.ylabel("amount")
    plt.show()


    return perc


def duration_of_stay(arr_x, time1):
    # function to calculate how long the protein stays on the DNA
    # create a new list to store all the durations in it
    duration = []
    for i in range(len(arr_x)):
        # goes through the single kymos
        for j in range(len(arr_x[i])):
            # goes through the  paths
            if arr_x[i,j,0] != -5:
                # looks if the paths is empty, if not continue
                for k in range(len(arr_x[i,j])):
                    #iterate through the single points and saves the first one as start_point1
                    start_point1 = arr_x[i,j,0]
                    # both following if sentences are there to stop when the paths ends (either with -5 or the last
                    # entry)
                    if arr_x[i,j,k] == -5:
                        # get the end_point
                        end_point1 = arr_x[i,j,k-1]
                        #calculate the duration
                        duration.append(round((end_point1-start_point1)*time1[i],2))
                        break
                    if k == len(arr_x[i,j]):
                        end_point1 = arr_x[i,j,k]
                        duration.append(round((end_point1-start_point1)*time1[i],2))



    # bins_list to classify the division of the histogram
    # some specification for the histogramm
    bins_list = [0,25,50,75,100,125,150,175,200,225,250,275,300,325,350,375,400,425,450,475,500]
    plt.hist(duration, bins=bins_list)
    plt.title("n = "+str(len(duration)))
    plt.xlim(0,500)
    plt.ylabel("amount")
    fig_text = "mean: "+ str(round(statistics.mean(duration),2)) + "\nstd: "+ str(round(statistics.stdev(duration),2))
    plt.figtext(.7,.7, fig_text)
    plt.xlabel("sec")
    plt.show()


    return duration

def track_movement(arr_x, arr_y):
    # declare the variables for the measurement (track_distance and threshold)
    # here you could change all your parameters for the calculation
    track_iteration = 30
    track_distance = 30
    # threshold
    upper_limit = 4
    lower_limit = -4
    # get the dimensions of the numpy array
    dimensions = arr_x.shape
    # declare some lists
    values_x = []
    values_y = []
    differences = []
    all_differences = []
    all_differences_total = []
    all_differences_y = []
    y_plot = 0
    perc_mobile_ele = []

    for i in range(len(arr_x)):
        # goes through the kymos
        for j in range(len(arr_x[i])):
            # goes through the paths
            # after each paths it clears the list for the next paths
            values_x.clear()
            values_y.clear()
            differences.clear()
            for k in range(dimensions[2]):
                # goes through the single coordinates
                if arr_x[i,j,0] == -5:
                    # if paths starts with -5 the array is empty, so we break the loop
                    break
                if arr_x[i,j,k] != -5:
                    # if there is a paths we store the coordinates inside the lists values_x and values_y
                    values_x.append(arr_x[i,j,k])
                    values_y.append(arr_y[i,j,k])
                else:
                    # at the end, so when the paths ends (we get a -5 value) we can then with the list calculate the
                    # movement
                    start = 0
                    y_plot = y_plot + 10
                    while start < len(values_x):
                        # iterate through the values and save the starting_y value == y1
                        starting_y = values_y[start]
                        for further in range(start, len(values_x)):
                            # then looks for the second datapoint 30 points away == y2
                            if values_x[further] - values_x[start] >= track_distance:
                                # if the second datapoint is furhter than 30 pixels away from the first we can caluclate
                                # the difference
                                # append the difference in the lists for the different plottings
                                differences.append(starting_y-values_y[further])
                                all_differences.append(starting_y-values_y[further])
                                all_differences_total.append(abs(starting_y-values_y[further]))
                                all_differences_y.append(y_plot)
                                #after that break the for loop
                                break
                        # inside the while loop go 30 datapoints up front
                        # note to myself: actually we are not moving 30 pixels but 30 datapoints (often more than 30
                        # pixels!)
                        start = start + track_iteration


                    # at the end of each iteration look at the differences and count the number of events > threshold or
                    # < -threshold
                    amount = 0
                    for ele in differences:
                        # iterates through all elements in the differences list and checks for the threshold
                        if ele > upper_limit or ele < lower_limit:
                            amount = amount + 1
                    try:
                        # calculate the percentage of mobile elements and store it in a list
                        perc_mobile_ele.append(round(amount/len(differences),2))
                    except:
                        m = 0

                    break


    # plot for the mobile elements
    bins_list = [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
    plt.hist(perc_mobile_ele, bins=bins_list)
    plt.title("mobile XPB w.o. ATP")
    plt.ylim(0,120)
    plt.ylabel("amount")
    plt.xlabel("perc of mobile elements")
    plt.show()

    # plot for the differences
    plt.scatter(all_differences, all_differences_y)
    fig_text = ("mean: "+ str(round(statistics.mean(all_differences),2)) + "\nstd: "+str(round(statistics.stdev(all_differences),2)))
    plt.figtext(.8, .8, fig_text)
    plt.xlim(-30,30)
    plt.title("XPB w.o. ATP")
    plt.show()

    # plot for the absolut differences
    plt.scatter(all_differences_total, all_differences_y)
    fig_text = ("mean: " + str(round(statistics.mean(all_differences_total), 2)) + "\nstd: " + str(round(statistics.stdev(all_differences_total), 2)))
    plt.figtext(.8,.8,fig_text)
    plt.title("XPB with ATP abs numbers")
    plt.show()




def starting_function(filename, analysis):
    with open(filename, "r") as result:
        data = result.readlines()
    x,y, arr_x, arr_y, time1, pix1, dis1 = create_lists(data)
    # shows all tracked_kymographs
    show_all(arr_x,arr_y)
    if analysis == "position" or analysis == "all":
        # define start position on DNA
        start_point(arr_x, arr_y, dis1)
    if analysis == "duration" or analysis == "all":
        # define duration on DNA
        duration_of_stay(arr_x, time1)
    if analysis == "movement" or analysis == "all":
        # track movement
        track_movement(arr_x, arr_y)

