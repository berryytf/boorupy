import json
import urllib.request as urlreq
from random import randint
from typing import *

"""
Works with gelbooru API.
"""

class Gelbooru:
    def __init__(self, api_key: Optional[str] = None, user_id: Optional[str] = None):
        self.api_key = api_key
        self.user_id = user_id
        self.page_num = randint(0, 19)
        self.booru_url = 'https://gelbooru.com/index.php?page=dapi&s=post&q=index&json=1'

    # Get a bunch of posts based on a limit and tags that the user enters.
    def get_posts(self, tags='', limit=100):
        final_url = self.booru_url + f'&limit={str(limit)}&tags={tags}&pid={self.page_num}&api_key={self.api_key}&user_id={self.user_id}'
        urlobj = urlreq.urlopen(final_url)
        json_response = json.load(urlobj)
        urlobj.close()
        temp = 4
        # Reduces search if json_response is an empty list
        while len(json_response) == 0: 
            self.page_num = randint(0, temp) 
            # Further reduction if random integer fails again
            if temp > 0:
                temp += -1
            else:
                pass
            final_url = self.booru_url + f'&limit={str(limit)}&tags={tags}&pid={self.page_num}&api_key={self.api_key}&user_id={self.user_id}'
            urlobj = urlreq.urlopen(final_url)
            json_response = json.load(urlobj)
            urlobj.close()

        images = self.__link_images(json_response)
        return images

    # Get a single image based on tags that the user enters.
    def get_single_post(self, tags=''):
        post_url = self.booru_url + f'&limit={1}&tags={tags}&pid={self.page_num}&api_key={self.api_key}&user_id={self.user_id}'
        urlobj = urlreq.urlopen(post_url)
        json_response = json.load(urlobj)
        urlobj.close()
        temp = 4
        # Reduces search if json_response is an empty list
        while len(json_response) == 0:
            self.page_num = randint(0, temp)
            # Further reduction if random integer fails again
            if temp > 0:
                temp += -1
            else:
                pass
            post_url = self.booru_url + f'&limit={1}&tags={tags}&pid={self.page_num}&api_key={self.api_key}&user_id={self.user_id}'
            urlobj = urlreq.urlopen(post_url)
            json_response = json.load(urlobj)
            urlobj.close()
        
        image = self.__link_images(json_response)
        return image
    
    def get_random_post(self):
        self.page_num = randint(0, 999)
        post_url = self.booru_url + f'&limit={1}&pid={self.page_num}&api_key={self.api_key}&user_id={self.user_id}'
        urlobj = urlreq.urlopen(post_url) 
        json_response = json.load(urlobj)
        urlobj.close()

        image = self.__link_images(json_response)
        return image
        
    # Private function to create a post URL and a related image URL
    def __link_images(self, response):
        image_list = []
        temp_dict = dict()
        temp = 1
        post_url = 'https://gelbooru.com/index.php?page=post&s=view&id='
        for i in range(len(response)):
            temp_dict[f'Post {temp} URL'] = post_url + f'{response[i]["id"]}'
            temp_dict[f'Image {temp} URL'] = response[i]['file_url']
            image_list.append(temp_dict)
            temp_dict = dict()
            temp += 1
        
        return image_list # Returns image URL(s) and post URL(s) in a list
    
    def testing(self):
        print(self.api_key)