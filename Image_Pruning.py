"""
Temporary code used to refine the images
1/10/21
"""

import os
from PIL import Image, ImageChops,ImageStat
import time
from skimage.morphology import skeletonize
import numpy
from Process_Images import Fractal

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
    return


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
    return

def resize(img, size):

    img = Image.open(img)
    major_length = max(img.size)
    minor_length = min(img.size)
    major_index = img.size.index(major_length)
    minor_index = img.size.index(minor_length)

    multiplier = size / major_length
    new_major = int(multiplier * major_length)
    new_minor = int(multiplier * minor_length)
    print(new_minor)
    print(new_major)
    new_size = [0, 0]
    new_size[major_index] = new_major
    new_size[minor_index] = new_minor
    new_size = tuple(new_size)

    new_img = Image.new('RGB', (size, size), color=(255, 255, 255))
    new_img.paste(img, (int((size - new_size[0]) / 2),
                        int((size - new_size[1]) / 2)))
    return new_img


def booleanize(img):
    # Convert all the pixels in the image to either black or white

    time1 = time.time()
    count = 0
    size = img.size
    new_img = Image.new('1', size)

    for x in range((img.size)[0]):
        for y in range((img.size)[0]):

            count += 1
            print(count)

            pixel = img.getpixel((x,y))

            avg = (pixel[0] + pixel[1] + pixel[2]) / 3

            if avg < 150:
                new_img.putpixel((x,y), (0))
            else:
                new_img.putpixel((x,y), (1))

    name = os.path.basename(img.filename)
    name = name.split('.')[0]
    print(name)
    new_img.save('serp.png'.format(name))

    time2 = time.time()
    print(round((time2 - time1), 2))
    return


def thinning(img):

    time1 = time.time()
    print('...')
    img_path = img
    img = Image.open(img)
    size = img.size
    thinned_img = Image.new('1', size)
    image_list = [[] for _ in range(size[0])]

    for x in range(size[0]):
        for y in range(size[0]):
            pixel = img.getpixel((x,y))
            image_list[x].append(True if pixel == 0 else False)

    image_array = numpy.array(image_list)
    skeleton = skeletonize(image_array)
    thinned_image = [list(array) for array in skeleton]

    for x in range(size[0]):
        for y in range(size[0]):
            thinned_img.putpixel((x,y), not thinned_image[x][y])

    thinned_img.save(img_path)

    time2 = time.time()
    total_time = str(round((time2 - time1), 2))
    print('Time elapsed: {}'.format(total_time))
    return


path = "/Users/Connor/PycharmProjects/Random Projects/Fractal Dimensions/serp.png"
tri = Image.open(path)
triangle = Fractal(tri)
data, pics = triangle.split_image()
numbas = triangle.calculate_fractal_dimensions(data)

for pic in pics:
    pic.show()
print(numbas[2])
print(numbas[3])

