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

    # Fix tags so that they work with the image board
    def __tagifier(self, unformated_tags):
        fixed_tags = unformated_tags.replace(', ', r'%20').replace(' ', '_').lower()
        return fixed_tags

    def get_posts(self, tags='', limit=100):
        if limit > 100:
            raise Exception("Limit cannot be greater than 100")

        tags = self.__tagifier(tags)
        final_url = self.booru_url + f'&tags={tags}&limit={limit}&pid={self.page_num}'
        urlobj = urlreq.urlopen(final_url)
        json_response = json.load(urlobj)
        urlobj.close()
        temp = 4

        while len(json_response) == 0:
            self.page_num = randint(0, temp)

            if temp > 0:
                temp += -1
            else:
                pass
            final_url = self.booru_url + f'&tags={tags}&limit={limit}&pid={self.page_num}'
            urlobj = urlreq.urlopen(final_url)
            json_response = json.load(urlobj)
            urlobj.close()
            temp = 4
        
        self.__link_images(json_response)
        
    
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
            temp_dict[f'Post {temp} URL'] = post_url + f'&id={post_id}'
            temp_dict[f'Image {temp} URL'] = image_url
            image_list.append(temp_dict)
            temp += 1
            temp_dict = dict()
        print(image_list)



        
