"""
1/15/21
Next to do:
- Extract the data from the csv file and display with matplotlib
- Tidy everything up into a neat GUI that displays all the images and graphs
- Change the program to accept all different img sizes
- Try out different fractals and country outlines
"""

from PIL import Image, ImageStat, ImageChops
from matplotlib import pyplot as plt
from math import log
import os
import time
import csv


class Fractal:

    def __init__(self, img):

        self.steps = [20, 40, 60, 80, 100, 120, 140, 160, 180, 200]
        self.img = img



    def split_image(self):
        # 50 States
        # Get state name
        state_name = self.img.filename.split('.')[0]
        img = self.img.convert('RGB')
        size = img.size

        img_data = []
        pictures = []

        for factor in self.steps:
            # 10 diff images
            # Step is number of squares per row/column
            step = factor
            # Increment is number of pixels per step
            incr = int(size[0] / step)

            outline_in_image = 0

            image_bits = []
            # Create blank image to paste bits onto
            highlighted_image = Image.new('RGB', size)

            for num in range(step ** 2):
                # Image bits

                # Fancy equations to convert list of numbers into grid
                x1 = (num % step) * incr
                x2 = x1 + incr
                y1 = (num // step) * incr
                y2 = y1 + incr

                # Crop image into small bit, add to list
                image_bit = img.crop((x1,y1,x2,y2))
                image_bits.append(image_bit)
                # Check if outline is in that bit
                min_value = ImageStat.Stat(image_bit).extrema[0][0]

                if min_value == 0:
                    # If outline is in image, tint its color yellow and save value
                    outline_in_image  += 1

                    image_tint = Image.new('RGB', (incr, incr), (255, 0, 0))
                    image_bits[num] = ImageChops.multiply(image_bits[num], image_tint)

                # Reconstructs the original image with the new bits (some are tinted now)
                highlighted_image.paste(image_bits[num], (x1, y1))

            # Store images in list
            pictures.append(highlighted_image)
            #highlighted_image.show()
            # Stores outline ratio data
            img_data.append(outline_in_image)

        return img_data, pictures




    def calculate_fractal_dimensions(self, img_data):

        graph_data = [[],[],[], 0]

        for j in range(len(img_data) - 1):

            # Calculate change in block size between pictures
            scaling_factor = self.steps[j + 1] / self.steps[j]
            scaling_factor = round(scaling_factor, 4)
            # Calculate change in number of highlighted blocks between pictures
            block_ratio = img_data[j + 1] / img_data[j]
            block_ratio = round(block_ratio, 4)
            # Use b_r and s_f with some fancy log math to find f_d
            # This line of code is the focal point of the whole project
            fractal_dimension = log(block_ratio,scaling_factor)
            fractal_dimension = round(fractal_dimension, 4)
            # Store data in one list for return rather than returning 3
            graph_data[0].append(scaling_factor)
            graph_data[1].append(block_ratio)
            graph_data[2].append(fractal_dimension)

        # Get log values of scaling factors and block ratios
        log_s_f = [log(num) for num in graph_data[0]]
        log_b_r = [log(num) for num in graph_data[1]]
        # Calculate line of best fit
        mean_s_f = sum(log_s_f) / len(log_s_f)
        mean_b_r = sum(log_b_r) / len(log_b_r)

        numerator = 0
        denominator = 0
        for factor, ratio in zip(log_s_f, log_b_r):
            # Linear regression
            numerator += ((factor - mean_s_f) * (ratio - mean_b_r))
            denominator += ((factor - mean_s_f) ** 2)
        best_fit = numerator / denominator
        graph_data[3] = best_fit

        return graph_data


    def data_to_file(self, name, graph_data):

        name_ = name.split('.')[0]
        # Extract data from nested list
        s_f = graph_data[0]
        b_r = graph_data[1]
        f_d = graph_data[2]
        # Open csv file for storing this data
        f = open('picture_data.csv', 'a')
        write_f = csv.writer(f)
        # Add header to empty file
        if os.path.getsize('picture_data.csv') == 0:
            write_f.writerow(['Name', 'Grid Size', 'Block Ratio', 'Scaling Factor', 'Fractal Dimension'])
        # The first image will only have a size so write that in
        write_f.writerow([name_, self.steps[0] ** 2])
        # Write the data for each (other) image to the file
        for i in range(len(s_f)):
            write_f.writerow(['', self.steps[i + 1] ** 2, b_r[i], s_f[i], f_d[i]])


    def create_plot(self, graph_data):
        # Create the plots from the data

        # Unpack the data
        s_f, b_r, f_r = graph_data

        log_s_f = [log(num) for num in s_f]
        log_b_r = [log(num) for num in b_r]

        plt.plot(log_s_f, log_b_r)

        return



    def store_images(self, name, pictures):

        # Create a folder for each state within highlighted states
        name = name.split('.')[0]
        if not os.path.exists('Highlighted States/{}'.format(name)):
            os.mkdir('Highlighted States/{}'.format(name))

        # Add each image of different grid size to respective state folder
        for num in range(len(pictures)):
            pic_size = self.steps[num]
            pictures[num].save('Highlighted States/{}/{}_{}.png'.format(name, name, pic_size))



def main():
    # Generate images and data for 50 States, store the data so this function won't need to be run
    # every time the GUI is opened.
    start_time = time.time()

    # Get images from directory
    states = os.listdir('thin_bin_outlines')
    # Make directory for processed images
    if not os.path.exists('Highlighted States'):
        os.mkdir('Highlighted States')
    # Remove previous data from csv file
    open('picture_data.csv', 'w').close()

    for state_name in states:

        state_time1 = time.time()

        # Open image for use
        print(state_name.split('.')[0])
        state_img = Image.open('thin_bin_outlines/{}'.format(state_name))
        # Create object with image parameter
        state_object = Fractal(state_img)
        # Process images and retrieve data
        img_data, pictures = state_object.split_image()
        # Do the fancy math
        graph_data = state_object.calculate_fractal_dimensions(img_data)
        # Store processed images in neat directories
        state_object.store_images(state_name, pictures)
        # Store state data in csv file
        state_object.data_to_file(state_name, graph_data)

        state_time2 = time.time()
        print(str(round((state_time2 - state_time1), 2)))

    # Calculate program run time
    end_time = time.time()
    min = int((end_time - start_time) // 60)
    sec = round((end_time - start_time) % 60, 2)
    print('Time elapsed: {} Minutes, {} seconds'.format(min, sec))


if __name__ == '__main__':
     main()
