"""
This program scours the internet for a webpage that I found with good (enough)
outlines for the borders of the 50 US states. It shoves em in a file and bobs ya
uncle.
1/14/21
"""

from bs4 import BeautifulSoup
import urllib
import requests
import os


source = requests.get('https://gisgeography.com/state-outlines-blank-maps-united-states/').text
soup = BeautifulSoup(source, 'lxml')

outline_directory = '/Users/Connor/Desktop/State Outlines/'
os.mkdir(outline_directory)
os.chdir(outline_directory)

state_info = soup.find_all('span', class_='su-lightbox')

for state in state_info:

    link = state['data-mfp-src']
    name = os.path.basename(link)
    name = name.split('-')[:-2]
    name = ' '.join(name)

    outline_image = open('{}.jpg'.format(name), 'wb')
    outline_image.write(urllib.request.urlopen(link).read())

    print(name)
    print(link)
    print('')
