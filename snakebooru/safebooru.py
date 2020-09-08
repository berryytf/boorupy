import json
import urllib.request as urlreq
from random import randint
from typing import *
import xml.etree.ElementTree as ET

class Safebooru:
    def __init__(self):
        self.page_num = randint(0, 19)
        self.booru_url = 'https://safebooru.org/index.php?page=dapi&s=post&q=index&json=1'
        self.comment_url = 'https://safebooru.org/index.php?page=dapi&s=comment&q=index'

    # Private function to fix tags so that they work with the image board
    def __tagifier(self, unformated_tags):
        fixed_tags = unformated_tags.replace(', ', r'%20').replace(' ', '_').lower()
        return fixed_tags

    # Returns up too 100 posts and images based on tags the user inputs
    def get_posts(self, tags='', limit=100):
        if limit > 100:
            raise Exception("Limit cannot be greater than 100")

        tags = self.__tagifier(tags)

        try:
            final_url = self.booru_url + f'&tags={tags}&limit={limit}&pid={self.page_num}'
            urlobj = urlreq.urlopen(final_url)
            json_response = json.load(urlobj)
            urlobj.close()
        except:
            return None

        temp = 4
        while len(json_response) == 0:
            self.page_num = randint(0, temp)

            if temp > 0:
                temp += -1
            else:
                pass
            try:
                final_url = self.booru_url + f'&tags={tags}&limit={limit}&pid={self.page_num}'
                urlobj = urlreq.urlopen(final_url)
                json_response = json.load(urlobj)
                urlobj.close()
            except:
                return None
            temp = 4
        
        images = self.__link_images(json_response)
        return images

    # Return a single post and image based on tags the user inputs
    def get_single_post(self, tags=''):
        tags = self.__tagifier(tags)
        final_url = self.booru_url + f'&tags={tags}&limit=1&pid={self.page_num}'
        
        try:
            urlobj = urlreq.urlopen(final_url)
            json_response = json.load(urlobj)
            urlobj.close()
        except:
            return None

        temp = 4

        # Reduce search if json_response is empty
        while len(json_response) == 0:
            self.page_num = randint(0, temp)
            
            if temp > 0:
                temp += -1 # Further reduction
            else:
                pass
            final_url = self.booru_url + f'&tags={tags}&limit={1}&pid={self.page_num}'
            try:
                urlobj = urlreq.urlopen(final_url)
                json_response = json.load(urlobj)
                urlobj.close()
            except:
                return None
            temp = 4

        image = self.__link_images(json_response)
        return image

    #Get a random post. This selects a single image out of 20,100 images.
    def get_random_post(self):
        self.page_num = randint(0, 200)
        final_url = self.booru_url + f'&limit={100}&pid={self.page_num}'
        urlobj = urlreq.urlopen(final_url)
        json_response = json.load(urlobj)
        urlobj.close()

        temp = [json_response[randint(0,99)]]
        image = self.__link_images(temp)
        return image

    # Get data from a post
    def get_post_data(self, post_id):
        data_url = f'https://safebooru.org/index.php?page=dapi&s=post&q=index&id={post_id}'

        urlobj = urlreq.urlopen(data_url)
        data = ET.parse(urlobj)
        urlobj.close()
        root = data.getroot()

        return root[0].attrib # Returns a dictionary

    # Private function to link images from the various functions above.
    def __link_images(self, response):
        image_list = []
        temp_dict = dict()
        temp = 1
        post_url = 'https://safebooru.org/index.php?page=post&s=view'

        for i in response:
            directory = i['directory']
            post_id = i['id']
            image_ext = i['image']
            image_url = f'https://safebooru.org/images/{directory}/{image_ext}'
            temp_dict[f'post {temp} url'] = post_url + f'&id={post_id}'
            temp_dict[f'image {temp} url'] = image_url
            image_list.append(temp_dict)
            temp += 1
            temp_dict = dict()

        return image_list