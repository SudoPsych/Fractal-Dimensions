"""
Testing for this project
1/10/21
"""


from bs4 import BeautifulSoup
import urllib
import requests
import os
from PIL import Image, ImageChops


def soupTest():

    source = requests.get('https://store.dftba.com/pages/creators').text

    soup = BeautifulSoup(source, 'lxml')

    creatorInfo = soup.find_all('li', class_="grid__item small--one-half medium-up--one-fifth")

    creators = {}

    for creator in creatorInfo:

        name = creator.text.replace('\n', '')
        name = ''.join(x for x in name if x.isalnum() or x == ' ')

        photoLink = 'https:' + creator.img['src']
        creators.update({name : photoLink})

    DFTBA = '/Users/Connor/Desktop/DFTBA Creators'
    os.mkdir(DFTBA)
    os.chdir(DFTBA)

    for key in creators:

        value = creators[key]

        fileType = os.path.splitext(value)[1]
        fileType = fileType.split('?')[0].lower()

        logoImage = open('{}{}'.format(key, fileType), 'wb')
        logoImage.write(urllib.request.urlopen(value).read())
        logoImage.close()

        print(key)
        print(value)

def image():

    texas = Image.open('State Outlines/Texas.jpg')
    os.chdir('newStates/bits')
    texas.show()

    # incr: increment of pixels
    # step: total number of increments along one dimension
    # x1 = (num % step) * incr
    # x2 = x1 + incr
    # y1 = (num // step) * incr
    # y2 = y1 + incr

    step = 5
    incr = 200 / step
    """
    for num in range(step ** 2):

        x1 = (num % step) * incr
        x2 = x1 + incr
        y1 = (num // step) * incr
        y2 = y1 + incr

        chad_bit = chad.crop((x1,y1,x2,y2))

        chad_bit.save('bit_{}.jpg'.format(num))
        print(ImageStat.Stat(chad_bit).stddev)
    """

def deleteBits():

    os.chdir('newStates/bits')
    bits = os.listdir()
    for bit in bits:
        os.remove(bit)

def outlines():

    os.chdir("State Outlines")
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

    os.chdir("State Outlines")
    states = os.listdir()
    new_states_path = "/Users/Connor/PycharmProjects/Random Projects/Fractal Dimensions/newStates/"

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

        print(new_state.size)
        new_state.save("/Users/Connor/PycharmProjects/Random Projects/Fractal Dimensions/newStates/{}".format(name))

def filters():

    os.chdir('newStates')
    states = os.listdir()
    state = Image.open('Rhode Island.jpg')

    state.show()
    image_tint = Image.new('RGB', (2000,2000), (255, 255, 156))
    state = ImageChops.multiply(state, image_tint)
    state.show()


