"""
1/15/21

Notes:
- Min/max value is not a good way to find outlines, find some other way.
- Alaska is stupid lol she needs special treatment
 TO DO:
Calculation time :D (use notes)
"""

from PIL import Image, ImageStat, ImageChops
import os


class Fractal:

    def __init__(self):


        self.img_length = 2000
        # Factors of 2000 for perfect grid
        self.factors = [5, 8, 10, 16, 20, 25, 40, 50, 100, 200]
        self.factors = [200]
        print(os.getcwd())
        os.chdir("newStates")



    # Jesus Christ this function is a hot mf mess you gotta pretty this up
    def split_image(self, img):
        # 50 States
        # Get state name
        state_name = img.filename.split('.')[0]
        print(state_name)

        img_data = []

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

            highlighted_image.show()
            # Stores outline ratio data
            img_data.append(outline_in_image)
        return img_data




    def calculate_fractal_dimensions(self, img_data):

        for i in range(len(self.factors)):

            num_blocks = self.factors[i] ** 2

            block_ratio = img_data[i] / num_blocks

            # left off here



    def main(self):

        states = os.listdir()

        for state_name in states:
            # Fuck Alaska lol
            if True:

                state_img = Image.open(state_name)

                img_data = self.split_image(state_img)

                self.calculate_fractal_dimensions(img_data)



Fractal().main()
