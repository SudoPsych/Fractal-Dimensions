"""
1/15/21
Next to do:
- Extract the data from the csv file and display with matplotlib
- Tidy everything up into a neat GUI that displays all the images and graphs
"""

from PIL import Image, ImageStat, ImageChops
import os
from math import log
import matplotlib.pyplot as plt
import csv


class Fractal:

    def __init__(self):


        self.img_length = 2000
        # Factors of 2000 for perfect grid
        # Factors of 2000:
        # 2, 4, 5, 8, 10, 16, 20, 25, 40, 50, 80, 100, 125, 200, 250, 400, 500, 1000
        self.factors = [2, 4, 5, 8, 10, 16, 20]




    def split_image(self, img):
        # 50 States
        # Get state name
        state_name = img.filename.split('.')[0]

        img_data = []
        pictures = []

        for factor in self.factors:
            # 10 diff images
            # Step is number of squares per row/column
            step = factor
            # Increment is number of pixels per step
            incr = int(self.img_length / step)

            outline_in_image = 0

            image_bits = []
            # Create blank image to paste bits onto
            highlighted_image = Image.new('RGB', (2000, 2000))

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

                if min_value < 3:
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

        graph_data = [[],[],[]]

        for j in range(len(img_data) - 1):

            # Calculate change in block size between pictures
            scaling_factor = self.factors[j + 1] / self.factors[j]
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
        write_f.writerow([name_, self.factors[0] ** 2])
        # Write the data for each (other) image to the file
        for i in range(len(s_f)):
            write_f.writerow(['', self.factors[i + 1] ** 2, b_r[i], s_f[i], f_d[i]])




    def store_images(self, name, pictures):

        # Create a folder for each state within highlighted states
        name = name.split('.')[0]
        if not os.path.exists('Highlighted States/{}'.format(name)):
            os.mkdir('Highlighted States/{}'.format(name))

        # Add each image of different grid size to respective state folder
        for num in range(len(pictures)):
            pictures[num].save('Highlighted States/{}/{}{}.jpg'.format(name, name, num))




    def main(self):
        # Duh main function hur dur

        # Get images from directory
        states = os.listdir('outlines')
        # Make directory for processed images
        if not os.path.exists('Highlighted States'):
            os.mkdir('Highlighted States')

        open('picture_data.csv', 'w').close()

        for state_name in states:

            # Open image for use
            print(state_name.split('.')[0])
            state_img = Image.open('outlines/{}'.format(state_name))
            # Process images and retrieve data
            img_data, pictures = self.split_image(state_img)
            # Do the fancy math
            graph_data = self.calculate_fractal_dimensions(img_data)
            # Write fancy math results to csv file
            self.data_to_file(state_name, graph_data)
            # Store processed images in neat directories
            self.store_images(state_name, pictures)


Fractal().main()
