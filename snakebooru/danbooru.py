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
        self.page_num = randint(0, 19)
        self.booru_url = 'https://danbooru.donmai.us/posts.json?'
        self.post_url = 'https://danbooru.donmai.us/posts/'

    def __tagifier(self, unformated_tags):
        fixed_tags = unformated_tags.replace(', ', r'%20').replace(' ', '_').lower()
        return fixed_tags

    # Get posts based on tags the user inputs
    def get_posts(self, tags='', limit=100):
        tags = self.__tagifier(tags)
        final_url = self.booru_url + f'&login={self.login}&api_key={self.api_key}&limit={limit}&tags={tags}'
        urlobj = urlreq.urlopen(final_url)
        json_response = json.load(urlobj)
        urlobj.close()

        if not json_response:
            return None # Return None if no images found

        images = self.__link_images(json_response)
        
        return images

    # Danbooru API has a "random" keyword :D
    def get_random_post(self):
        final_url = self.booru_url + f'&login={self.login}&api_key={self.api_key}&random=true&limit=1'
        
        urlobj = urlreq.urlopen(final_url)
        json_response = json.load(urlobj)
        urlobj.close()
        
        image = self.__link_images(json_response)

        return image

    def get_image_data(self, post_id):
        final_url = self.post_url + f'{post_id}.json'

        try: 
            urlobj = urlreq.urlopen(final_url)
            json_response = json.load(urlobj)
            urlobj.close()
        except:
            return None
        
        return json_response

    # Private function to create dictionaries of posts/images
    def __link_images(self, response):
        image_list = []
        temp_dict = dict()
        temp = 1
        post_url = 'https://danbooru.donmai.us/posts/'

        for i in response:
            post_id = i['id']
            file_url = i['file_url']
            temp_dict[f'post {temp} url'] = post_url + str(post_id)
            temp_dict[f'image {temp} url'] = file_url
            image_list.append(temp_dict)
            temp += 1
            temp_dict = dict()
        
        return image_list