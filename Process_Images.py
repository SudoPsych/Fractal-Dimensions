"""
1/15/21
In retrospect, this file should have been written as normal functions
rather than as a class. It would have made more sense that way when creating the
GUI but it works fine this way as well.
"""

from PIL import Image, ImageStat, ImageChops
from matplotlib import pyplot as plt
import numpy as np
from math import log
import os
import time
import csv


class Fractal:

    def __init__(self):

        self.steps = [20, 40, 60, 80, 100, 120, 140, 160, 180, 200]



    def split_image(self, display_img, skeleton_img):
        # Split image into bits, make calculations, and return highlighted images.
        # skeleton_img is what the program checks for outline
        # display_img is the image that is highlighted and returned.
        # ^ Usually is the converted binary outline before being skeletonized.
        # They can be the same image, this feature is because the skeletonized image shows up poorly in the GUI.

        display_img = Image.open(display_img)
        skeleton_img = Image.open(skeleton_img)

        display_img = display_img.convert('RGB')
        size = skeleton_img.size

        img_data = []
        pictures = []

        for factor in self.steps:
            # Step is number of squares per row/column
            step = factor
            # Increment is number of pixels per step
            incr = int(size[0] / step)

            outline_in_image = 0

            # Create blank image to paste bits onto
            highlighted_image = Image.new('RGB', size)

            for num in range(step ** 2):

                # Fancy equations to convert list of numbers into grid
                x1 = (num % step) * incr
                x2 = x1 + incr
                y1 = (num // step) * incr
                y2 = y1 + incr

                # Crop image into small bit, add to list
                display_bit = display_img.crop((x1,y1,x2,y2))
                skeleton_bit = skeleton_img.crop((x1,y1,x2,y2))
                # Check if outline is in that bit
                min_value = ImageStat.Stat(skeleton_bit).extrema[0][0]

                if min_value == 0:
                    # If outline is in image, tint its color yellow and save value
                    outline_in_image  += 1

                    image_tint = Image.new('RGB', (incr, incr), (255, 0, 0))
                    display_bit = ImageChops.multiply(display_bit, image_tint)

                # Reconstructs the original image with the new bits (some are tinted now)
                highlighted_image.paste(display_bit, (x1, y1))

            # Store images in list
            pictures.append(highlighted_image)
            # Stores outline ratio data
            img_data.append(outline_in_image)

        return img_data, pictures




    def calculate_fractal_dimensions(self, img_data):
        # Fancy math to calculate fractal dimension and linear regression

        s_f = []
        b_r = []
        f_d = []

        for j in range(len(img_data) - 1):

            # Calculate change in block size between pictures
            scaling_factor = self.steps[j + 1] / self.steps[j]
            scaling_factor = round(scaling_factor, 4)
            # Calculate change in number of highlighted blocks between pictures
            block_ratio = img_data[j + 1] / img_data[j]
            block_ratio = round(block_ratio, 4)
            # Use b_r and s_f with some fancy log math to find f_d
            # This line of code is the focal point of the whole project
            fractal_dimension = log(block_ratio, scaling_factor)
            fractal_dimension = round(fractal_dimension, 4)
            # Store data
            s_f.append(log(scaling_factor))
            b_r.append(log(block_ratio))
            f_d.append(fractal_dimension)

        # Calculate line of best fit
        mean_s_f = sum(s_f) / len(s_f)
        mean_b_r = sum(b_r) / len(b_r)
        numerator = 0
        denominator = 0

        for factor, ratio in zip(s_f, b_r):
            # Linear regression
            numerator += ((factor - mean_s_f) * (ratio - mean_b_r))
            denominator += ((factor - mean_s_f) ** 2)

        # mx + b line of best fit
        m = numerator / denominator
        b = mean_b_r - (m * mean_s_f)
        # Storing the data
        graph_data = [s_f, b_r, f_d, m, b]

        return graph_data


    def data_to_file(self, path, graph_data):
        # Store state data in csv file

        # Extract data from list
        s_f, b_r, f_d, m, b = graph_data
        # Open csv file for storing this data
        f = open(path, 'a')
        write_f = csv.writer(f)
        # Scaling Factors
        write_f.writerow(['Scaling Factors'] + [num for num in s_f])
        # Block Ratio
        write_f.writerow(['Block Ratio'] + [num for num in b_r])
        # Fractal Dimension
        write_f.writerow(['Fractal Dimension'] + [num for num in f_d])
        # Slope of line
        write_f.writerow(['Slope', m])
        # y - intercept of line
        write_f.writerow(['y - intercept', b])

        return


    def get_data(self, file_path):
        # Get data from csv file

        f = open(file_path, newline='')
        read_f = csv.reader(f, delimiter=',')
        s_f = read_f.__next__()[1:]
        b_r = read_f.__next__()[1:]
        f_d = read_f.__next__()[1:]
        m   = read_f.__next__()[1]
        b   = read_f.__next__()[1]

        graph_data = [s_f, b_r, f_d, m, b]
        return graph_data


    def create_plot(self, graph_data):
        # Create the plots from the data

        # Unpack the data
        s_f, b_r, f_d, m, b  = graph_data
        # Turning lists into numpy arrays cuz matplotlib is picky
        s_f = np.array(s_f)
        b_r = np.array(b_r)
        # Axes
        plt.xlabel('log(Scaling Factor)')
        plt.ylabel('log(Block Ratio)')
        # Scatter plot for values and line of best fit
        plt.scatter(s_f, b_r, label = "Calculated Values", color = 'b')
        plt.plot(s_f, (m * s_f) + b, label = "Line of best fit", color = 'r')

        plt.legend()
        plt.show()

        return



    def store_images(self, pictures, name):

        # Check if dir exists first
        if not os.path.exists('image_data/Custom/highlighted/' + name):
            os.mkdir('image_data/Custom/highlighted/' + name)

        # Add each image of different grid size to its designated folder
        for num in range(len(pictures)):
            pic_size = self.steps[num]
            pictures[num].save('image_data/Custom/highlighted/{}/{}_{}.png'.format(name, name, pic_size))




def main():
    # Generate images and data for 50 States, store the data so this function won't need to be run
    # every time the GUI is opened.

    # Fix this code!

    start_time = time.time()

    # Get images from directory
    states = os.listdir('image_data/States/skeleton')
    # Make directory for processed images
    if not os.path.exists('image_data/States/highlighted'):
        os.mkdir('image_data/States/highlighted')
    # Remove previous data from csv file
    open('picture_data.csv', 'w').close()

    for state_name in states:

        state_time1 = time.time()

        print(state_name.split('.')[0])
        # Get path to thick and thin image for processing
        bin_path = 'image_data/states/binary/{}'.format(state_name)
        thin_bin_path = 'image_data/states/skeleton/{}'.format(state_name)
        # Create object with image parameter
        _Fractal = Fractal()
        # Process images and retrieve data
        img_data, pictures = _Fractal.split_image(bin_path, thin_bin_path)
        # Do the fancy math
        graph_data = _Fractal.calculate_fractal_dimensions(img_data)
        # Store processed images in neat directories
        _Fractal.store_images(state_name, pictures)
        # Store state data in csv file
        _Fractal.data_to_file(state_name, graph_data)

        state_time2 = time.time()
        print(str(round((state_time2 - state_time1), 2)))

    # Calculate program run time
    end_time = time.time()
    min = int((end_time - start_time) // 60)
    sec = round((end_time - start_time) % 60, 2)
    print('Time elapsed: {} Minutes, {} seconds'.format(min, sec))


if __name__ == '__main__':
    main()
