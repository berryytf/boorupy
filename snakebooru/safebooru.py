import json
import urllib.request as urlreq
from random import randint
from typing import *
import xml.etree.ElementTree as ET

class Safebooru:
    def __init__(self):
        self.page_num = randint(0, 19)
        self.booru_url = 'https://safebooru.org/index.php?page=dapi&s=post&q=index'
        self.comment_url = 'https://safebooru.org/index.php?page=dapi&s=comment&q=index'

    # Private function to link images from the various functions above.
    def __link_images(self, response):

        image_list = []
        temp_dict = dict()
        post_url = 'https://safebooru.org/index.php?page=post&s=view&id='
        for i in response:
            post_id = i['id']
            image_url = i['file_url']
            temp_dict['post_url'] = post_url + f'{post_id}'
            temp_dict['image_url'] = image_url
            temp_dict['id'] = post_id
            image_list.append(temp_dict)
            temp_dict = dict()

        return image_list

    # Private function to fix tags so that they work with the image board
    def __tagifier(self, unformated_tags):

        fixed_tags = unformated_tags.replace(', ', r'%20').replace(' ', '_').lower()
        return fixed_tags

    # Returns up too 100 posts and images based on tags the user inputs
    def get_posts(self, tags='', limit=100):
        '''User can pass in tags separated by a comma
        Using a dash before a tag will exclude it 
        e.g. (cat ears, -blue eyes)
        The limit parameter has a default value of 100
        Regardless of limit, this should return a list'''

        posts = []
        if limit > 100:
            raise Exception("Limit cannot be greater than 100")

        tags = self.__tagifier(tags)
        final_url = self.booru_url + f'&tags={tags}&limit={limit}&pid={self.page_num}'
        
        # This error should never happen
        try:
            urlobj = urlreq.urlopen(final_url)
            data = ET.parse(urlobj)
            urlobj.close()
            root = data.getroot()
        except ET.ParseError:
            return None        
        
        temp = 4
        attempts = 5
        while len(root) == 0:
            if attempts == 0:
                return None
            else:
                pass
            self.page_num = randint(0, temp)
            final_url = self.booru_url + f'&tags={tags}&limit={limit}&pid={self.page_num}'
            
            try:
                urlobj = urlreq.urlopen(final_url)
                data = ET.parse(urlobj)
                urlobj.close()
                root = data.getroot()
            except ET.ParseError:
                return None
            
            temp += -1
            attempts += -1

        for post in root:
            posts.append(post.attrib)

        images = self.__link_images(posts)
        return images

    # Return a single post and image based on tags the user inputs
    def get_single_post(self, tags=''):
        '''User can pass in tags separated by a comma
        Using a dash before a tag will exclude it 
        e.g. (cat ears, -blue eyes)
        Has a hard limit of 1'''

        tags = self.__tagifier(tags)
        posts = []
        final_url = self.booru_url + f'&limit=100&tags={tags}&pid={self.page_num}'
        
        try:
            urlobj = urlreq.urlopen(final_url)
            data = ET.parse(urlobj)
            urlobj.close()
            root = data.getroot()
        except ET.ParseError:
            return None

        temp = 4
        attempts =5 
        while len(root) == 0:
            if attempts == 0:
                return None
            else:
                pass
            self.page_num = randint(0, temp)
            final_url = self.booru_url + f'&limit=100&tags={tags}&pid={self.page_num}'
            
            try:
                urlobj = urlreq.urlopen(final_url)
                data = ET.parse(urlobj)
                urlobj.close()
                root = data.getroot()
            except ET.ParseError:
                return None
            
            temp += -1
            attempts += -1
            
        posts.append(root[randint(0, len(root)-1)].attrib)
        image = self.__link_images(posts)
        return image

    # Selects from 3000000+ images!
    def get_random_post(self):
        '''Simply, returns a random image out of 3000000+ possible images'''

        posts = []
        try:
            urlobj = urlreq.urlopen(self.booru_url)
            data = ET.parse(urlobj)
            urlobj.close()
            root_temp = data.getroot()
        except ET.ParseError:
            return None

        post_id = randint(1, int(root_temp.attrib['count']))
        final_url = self.booru_url + f'&id={post_id}'
        try:
            urlobj = urlreq.urlopen(self.booru_url)
            data = ET.parse(urlobj)
            urlobj.close()
            root = data.getroot()
        except ET.ParseError:
            return None

        posts.append(root[0].attrib)
        image = self.__link_images(posts)
        return image[0]

    # Get data from a post
    def get_post_data(self, post_id):
        '''User can pass in a post ID to get all of its data'''

        data_url = f'https://safebooru.org/index.php?page=dapi&s=post&q=index&id={post_id}'

        urlobj = urlreq.urlopen(data_url)
        data = ET.parse(urlobj)
        urlobj.close()
        root = data.getroot()

        return root[0].attrib # Returns a dictionary
