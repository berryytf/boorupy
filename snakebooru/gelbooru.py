import json
import urllib.request as urlreq
from random import randint
from typing import *
import xml.etree.ElementTree as ET

"""
Works with gelbooru API.
"""

class Gelbooru:

    def __init__(self, api_key: Optional[str] = None, user_id: Optional[str] = None):
        self.api_key = api_key
        self.user_id = user_id
        self.page_num = randint(0, 19)
        self.booru_url = 'https://gelbooru.com/index.php?page=dapi&s=post&q=index'
        self.comment_url = 'https://gelbooru.com/index.php?page=dapi&s=comment&q=index'

    def __tagifier(self, unformated_tags):
        fixed_tags = unformated_tags.replace(', ', r'%20').replace(' ', '_').lower()
        return fixed_tags
    
    # Get a bunch of posts based on a limit and tags that the user enters.
    def get_posts(self, tags='', limit=100):
        posts = []
        tags = self.__tagifier(tags)
        final_url = self.booru_url + f'&limit={str(limit)}&tags={tags}&pid={self.page_num}&api_key={self.api_key}&user_id={self.user_id}'
        
        try:
            urlobj = urlreq.urlopen(final_url)
            data = ET.parse(urlobj)
            urlobj.close()
            root = data.getroot()
        except ET.ParseError:
            return None

        for post in root:
            posts.append(post.attrib)
        
        temp = 4
        attempts = 5
        while len(posts) == 0:
            self.page_num = randint(0, temp)
            if temp > 0:
                temp -= 1
            else:
                pass
            final_url = self.booru_url + f'&limit={str(limit)}&tags={tags}&pid={self.page_num}&api_key={self.api_key}&user_id={self.user_id}' 
            try:
                urlobj = urlreq.urlopen(final_url)
                data = ET.parse(urlobj)
                urlobj.close()
                root = data.getroot()
            except ET.ParseError:
                return None

            attempts -= 1
            if attempts == 0:
                return None
            else:
                continue
            for post in root:
                posts.append(post.attrib)
        
        images = self.__link_images(posts)
        return images

    # Get a single image based on tags that the user enters.
    def get_single_post(self, tags=''):
        tags = self.__tagifier(tags)
        posts = []
        final_url = self.booru_url + f'&limit=1&tags={tags}&pid={self.page_num}&api_key={self.api_key}&user_id={self.user_id}'
        try:
            urlobj = urlreq.urlopen(final_url)
            data = ET.parse(urlobj)
            urlobj.close()
            root = data.getroot()
        except ET.ParseError:
            return None
        
        for post in root:
            posts.append(post.attrib)
        
        # reduces search if no results found
        temp = 4
        attempts = 5
        while len(posts) == 0:
            self.page_num = randint(0, temp)
            if temp > 0:
                temp -= 1
            else:
                pass
            final_url = self.booru_url + f'&limit=1&tags={tags}&pid={self.page_num}&api_key={self.api_key}&user_id={self.user_id}' 
            try:
                urlobj = urlreq.urlopen(final_url)
                data = ET.parse(urlobj)
                urlobj.close()
                root = data.getroot()
            except ET.ParseError:
                return None

            attempts -= 1
            if attempts == 0:
                return None
            else:
                continue
        
        image = self.__link_images(posts)
        return image
    
    def get_random_post(self):
        self.page_num = randint(0, 200)
        posts = []
        final_url = self.booru_url + f'&pid={self.page_num}&api_key={self.api_key}&user_id={self.user_id}'
        
        try:
            urlobj = urlreq.urlopen(final_url)
            data = ET.parse(urlobj)
            urlobj.close()
            root = data.getroot()
        except ET.ParseError:
            return None
        
        posts.append(root[randint(0,99)].attrib)
        image = self.__link_images(posts)
        return image
        
    # Get comments from a post using post_id
    def get_comments(self, post_id):
        comment_list = []
        final_url = self.comment_url + f'&post_id={post_id}&api_key={self.api_key}&user_id={self.user_id}'
        try:
            urlobj = urlreq.urlopen(final_url)
            data = ET.parse(urlobj)
            urlobj.close()
        except:
            return None

        root = data.getroot()
        temp = dict()
        
        # Iterate through comments
        for i in range(len(root)):
            temp['author'] = root[i].attrib['creator']
            temp['comment'] = root[i].attrib['body']
            comment_list.append(temp)
            temp = dict()

        if len(comment_list) == 0:
            return "No comments found"
        else:
            return comment_list
    
    # Get data for a post
    def get_post_data(self, post_id):
        data_url = f'https://gelbooru.com/index.php?page=dapi&s=post&q=index&id={post_id}'
        try:
            urlobj = urlreq.urlopen(data_url)
            data = ET.parse(urlobj)
            urlobj.close()
        except:
            return None

        root = data.getroot()

        return root[0].attrib

    # Private function to create a post URL and a related image URL
    def __link_images(self, response):
        image_list = []
        temp_dict = dict()

        post_url = 'https://gelbooru.com/index.php?page=post&s=view&id='
        for i in range(len(response)):
            temp_dict['post url'] = post_url + f'{response[i]["id"]}'
            temp_dict['image url'] = response[i]['file_url']
            temp_dict['id'] = response[i]['id']
            image_list.append(temp_dict)
            temp_dict = dict()

        return image_list # Returns image URL(s) and post URL(s) in a list