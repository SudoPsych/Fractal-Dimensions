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


class Scraper():

    def us_states(self):
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

    def countries(self):

        source = requests.get('https://www.worldatlas.com/countries').text
        soup = BeautifulSoup(source, 'lxml')

        outline_directory = '/Users/Connor/Desktop/Country Outlines/'
        os.mkdir(outline_directory)
        os.chdir(outline_directory)

        recognized_countries = soup.find('ol')
        country_names = recognized_countries.find_all('h3', id='item_name')
        country_names = [name.get_text() for name in country_names]

        no_image = []

        for name in country_names:

            new_name = name.replace(' ','-').lower()
            print(new_name)

            country_source = requests.get('https://www.worldatlas.com/maps/{}#outline1Section'.format(new_name)).text
            country_soup = BeautifulSoup(country_source, 'lxml')

            outline_div = country_soup.find('div', class_="map_outline_split_media")

            try:
                links = outline_div.find_all('a', class_='print_link')
                for i in range(len(links)):
                    link = links[i]['href']
                    link = 'https://www.worldatlas.com{}'.format(link)
                    print(link)
                    outline_image = open('{}{}.png'.format(name,i), 'wb')
                    outline_image.write(urllib.request.urlopen(link).read())
            except:
                no_image.append(name)

        print(no_image)

