"""
1/10/21
"""

from PIL import Image
import time
from skimage.morphology import skeletonize
import numpy


def resize_(img_path):
    # Change image to be given size

    img = Image.open(img_path)
    # Get length of image sides
    major_len = max(img.size)
    img_size = img.size

    new_img = Image.new('RGB', (major_len, major_len), color=(255, 255, 255))
    new_img.paste(img, (int((major_len - img_size[0]) / 2),
                        int((major_len - img_size[1]) / 2)))

    new_img = new_img.resize((2000, 2000))

    return new_img


def convert_to_binary(img_path):
    # Convert all the pixels in the image to either black or white

    time1 = time.time()
    count = 0
    img = Image.open(img_path)
    size = img.size
    new_img = Image.new('1', size)

    for x in range((img.size)[0]):
        for y in range((img.size)[0]):
            # Loop through each pixel
            count += 1
            print(count)
            # Get average value of pixel from RGB bands
            pixel = img.getpixel((x,y))
            avg = (pixel[0] + pixel[1] + pixel[2]) / 3
            # Check if pixel is relatively black or white and sets absolute value
            if avg < 150:
                new_img.putpixel((x,y), (0))
            else:
                new_img.putpixel((x,y), (1))

    time2 = time.time()
    print(round((time2 - time1), 2))

    return new_img


def skeletonize_(img_path):
    # Turn ugly fat lines into easy to work with thin ones

    time1 = time.time()
    print('...')
    img = Image.open(img_path)
    size = img.size
    thinned_img = Image.new('1', size)
    image_list = [[] for _ in range(size[0])]

    for x in range(size[0]):
        for y in range(size[0]):
            # Loop through each pixel in image
            # Turn image into nested list of values
            pixel = img.getpixel((x,y))
            # Invert colors as well (fuckin' love if/else statements with boolean values)
            image_list[x].append(False if pixel else True)
    # Convert to array
    image_array = numpy.array(image_list)
    # Runs algorithm from handy dandy library idk wtf happens here tbh
    # Removes excess pixels from outline while preserving it's relative shape/roughness
    skeleton = skeletonize(image_array)
    # Back to list
    thinned_image = [list(array) for array in skeleton]

    for x in range(size[0]):
        for y in range(size[0]):
            # Create new, skeletonized image. (Re-invert colors)
            thinned_img.putpixel((x,y), 0 if not thinned_image[x][y] else 1)

    time2 = time.time()
    total_time = str(round((time2 - time1), 2))
    print('Time elapsed: {}'.format(total_time))

    return thinned_img

