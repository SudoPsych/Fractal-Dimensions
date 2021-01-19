"""
Temporary code used to refine the images
1/10/21
"""

import os
from PIL import Image, ImageChops,ImageStat
import time
from skimage.morphology import skeletonize, thin
from skimage import data
import matplotlib.pyplot as plt
from skimage.util import invert
import numpy

def image():

    texas = Image.open('State Outlines/Texas.jpg')
    os.chdir('outlines/bits')
    texas.show()

    # incr: increment of pixels
    # step: total number of increments along one dimension
    # x1 = (num % step) * incr
    # x2 = x1 + incr
    # y1 = (num // step) * incr
    # y2 = y1 + incr

    step = 5
    incr = 200 / step

    for num in range(step ** 2):

        x1 = (num % step) * incr
        x2 = x1 + incr
        y1 = (num // step) * incr
        y2 = y1 + incr

        chad_bit = texas.crop((x1,y1,x2,y2))

        chad_bit.save('bit_{}.jpg'.format(num))
        print(ImageStat.Stat(chad_bit).stddev)


def deleteBits():

    os.chdir('outlines/bits')
    bits = os.listdir()
    for bit in bits:
        os.remove(bit)

def outlines():

    os.chdir("outlines")
    states = os.listdir()
    for state in states:
        state = Image.open(state)

        if 2000 not in state.size:
            print(state.filename)
            print(state.size)

def resize():

    os.chdir('State Outlines')
    state = Image.open('Colorado.jpg')
    size = state.size
    print(state.size)
    state = state.resize()
    state.save('Colorado.jpg')
    state.show()
    print(state.size)

def standardize():

    os.chdir("outlines")
    states = os.listdir()
    new_states_path = "/Users/Connor/PycharmProjects/Random Projects/Fractal Dimensions/outlines/"

    if not os.path.exists(new_states_path):
        os.mkdir(new_states_path)


    new_size = (2000, 2000)

    for state in states:

        state = Image.open(state)
        name = state.filename

        old_size = state.size

        new_state = Image.new('RGB', new_size, color=(255,255,255))

        new_state.paste(state,( int((new_size[0]-old_size[0]) / 2),
                                int((new_size[1]-old_size[1]) / 2)))

        new_state.save("/Users/Connor/PycharmProjects/Random Projects/Fractal Dimensions/outlines/{}".format(name))

def filters():

    os.chdir('outlines')
    states = os.listdir()
    state = Image.open('Rhode Island.jpg')

    state.show()
    image_tint = Image.new('RGB', (2000,2000), (255, 255, 156))
    state = ImageChops.multiply(state, image_tint)
    state.show()

def booleanize():
    # Convert all the pixels in the image to either black or white

    states = os.listdir('outlines')
    time1 = time.time()

    for state in states:

        count = 0
        state = Image.open('outlines/{}'.format(state))
        new_state = Image.new('1', (2000, 2000))

        for x in range((state.size)[0]):
            for y in range((state.size)[0]):

                count += 1
                print(count)

                pixel = state.getpixel((x,y))

                avg = (pixel[0] + pixel[1] + pixel[2]) / 3

                if avg < 150:
                    new_state.putpixel((x,y), (0))
                else:
                    new_state.putpixel((x,y), (1))

        name = os.path.basename(state.filename)
        name = name.split('.')[0]
        print(name)
        new_state.save('bin_outlines/{}.png'.format(name))

    time2 = time.time()
    print(round((time2 - time1), 2))

def skeletonizing():

    state = ('bin_outlines/Rhode Island.png')
    # Invert the horse image
    image = invert(data.horse())
    print(type(data.horse()))
    mylist = image.tolist()
    print(mylist)
    # perform skeletonization
    skeleton = skeletonize(image)

skeletonizing()
