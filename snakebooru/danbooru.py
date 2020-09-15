import json
import urllib.request as urlreq
from random import randint
from typing import *
import xml.etree.ElementTree as ET

class Danbooru:
    # Danbooru needs an API key unlike other boorus like Gelbooru and Safebooru
    def __init__(self, api_key, login):

        self.api_key = api_key
        self.login = login
        self.page_num = randint(0, 200)
        self.booru_url = 'https://danbooru.donmai.us/posts.json?'
        self.post_url = 'https://danbooru.donmai.us/posts/'

    # Private function to create dictionaries of posts/images
    def __link_images(self, response):

        image_list = []
        temp_dict = dict()
        post_url = 'https://danbooru.donmai.us/posts/'

        for i in response:
            post_id = i['id']
            file_url = i['file_url']
            temp_dict['post_url'] = post_url + str(post_id)
            temp_dict['image_url'] = file_url
            image_list.append(temp_dict)
            temp_dict = dict()
        
        return image_list

    def __tagifier(self, unformated_tags):

        fixed_tags = unformated_tags.replace(', ', r'%20').replace(' ', '_').lower()
        return fixed_tags

    # Get posts based on tags the user inputs
    def get_posts(self, tags='', limit=100):
        '''User can pass in tags separated by a comma
        Using a dash before a tag will exclude it 
        e.g. (cat ears, blue eyes, rating:safe, -nude)
        The limit parameter has a default value of 100
        Regardless of limit, this should return a list'''

        tags = self.__tagifier(tags)
        final_url = self.booru_url + f'&login={self.login}&api_key={self.api_key}&limit={limit}&tags={tags}&page={self.page_num}'
        try:
            urlobj = urlreq.urlopen(final_url)
            json_response = json.load(urlobj)
            urlobj.close()
        except json.JSONDecodeError:
            return None

        temp = 5
        attempts = 5
        while not json_response:
            if attempts == 0:
                return None
            else:
                pass

            self.page_num = randint(1, temp)
            final_url = self.booru_url + f'&login={self.login}&api_key={self.api_key}&limit={limit}&tags={tags}&page={self.page_num}'
            try:
                urlobj = urlreq.urlopen(final_url)
                json_response = json.load(urlobj)
                urlobj.close()
            except json.JSONDecodeError:
                return None
            
            temp += -1
            attempts += -1

        images = self.__link_images(json_response)
        return images

    def get_single_post(self, tags=''):
        '''User can pass in tags separated by a comma
        Using a dash before a tag will exclude it
        e.g. (cat ears, blue eyes, rating:safe, -nude)
        Has a hard limit of 1'''

        posts = []
        tags = self.__tagifier(tags)
        self.page_num = randint(0, 1000)
        final_url = self.booru_url + f'&login={self.login}&api_key={self.api_key}&limit=100&page={self.page_num}'

        try:
            urlobj = urlreq.urlopen(final_url)
            json_response = json.load(urlobj)
            urlobj.close()
        except json.JSONDecodeError:
            return None

        temp = 5
        attempts = 5
        while not json_response:
            if attempts == 0:
                return None
            else:
                pass

            self.page_num = randint(1, temp)
            final_url = self.booru_url + f'&login={self.login}&api_key={self.api_key}&limit=100&tags={tags}&page={self.page_num}'
            try:
                urlobj = urlreq.urlopen(final_url)
                json_response = json.load(urlobj)
                urlobj.close()
            except json.JSONDecodeError:
                return None
            
            temp += -1
            attempts += -1
        posts.append(json_response[randint(0,99)])
        image = self.__link_images(posts)
        return image[0]

    # Danbooru API has a "random" keyword :D
    def get_random_post(self):
        '''Simply, returns a random image out of 5000000+ possible images.'''

        final_url = self.booru_url + f'&login={self.login}&api_key={self.api_key}&random=true&limit=1'
        try:
            urlobj = urlreq.urlopen(final_url)
            json_response = json.load(urlobj)
            urlobj.close()
        except json.JSONDecodeError:
            return None
        
        image = self.__link_images(json_response)

        return image

    def get_image_data(self, post_id):
        '''User can pass in a post ID to get all of its data'''
        
        final_url = self.post_url + f'{post_id}.json'

        try: 
            urlobj = urlreq.urlopen(final_url)
            json_response = json.load(urlobj)
            urlobj.close()
        except:
            return None
        
        return json_response
