import urllib.request as urlreq
from random import randint
from typing import *
import xml.etree.ElementTree as ET

"""
Works with the gelbooru API.
You don't need a API key or User ID but searching may be limited without them so it is recommended
You can find your API key and User ID at https://gelbooru.com/index.php?page=account&s=options. Account is required
Since this uses f-strings this module only works in Python 3.6+
"""

class Gelbooru:

    def __init__(self, api_key: Optional[str] = None, user_id: Optional[str] = None):

        self.api_key = api_key
        self.user_id = user_id
        self.page_num = randint(0, 200)
        self.booru_url = 'https://gelbooru.com/index.php?page=dapi&s=post&q=index'
        self.comment_url = 'https://gelbooru.com/index.php?page=dapi&s=comment&q=index'
    
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

        return image_list

    def __tagifier(self, unformated_tags):

        fixed_tags = unformated_tags.replace(', ', r'%20').replace(' ', '_').lower()
        return fixed_tags
    
    # Get a bunch of posts based on a limit and tags that the user enters.
    def get_posts(self, tags='', limit=100):
        '''User can pass in tags separated by a comma.
        Using a dash before a tag will exclude it 
        e.g. (cat ears, blue eyes, rating:safe, -nude).
        The limit parameter has a default value of 100.
        Regardless of limit, this should return a list.'''

        posts = []
        tags = self.__tagifier(tags)
        final_url = self.booru_url + f'&limit={limit}&tags={tags}&pid={self.page_num}&api_key={self.api_key}&user_id={self.user_id}'
        
        # This error should not ever happen.
        try:
            urlobj = urlreq.urlopen(final_url)
            data = ET.parse(urlobj)
            urlobj.close()
            root = data.getroot()
        except ET.ParseError:
            return None

        # Reduce search if length of root is 0. Gives up if pid=0 has 0 results 
        temp = 4
        attempts = 5
        while len(root) == 0:
            if attempts == 0:
                return None
            else:
                pass
            self.page_num = randint(0, temp)
            final_url = self.booru_url + f'&limit={limit}&tags={tags}&pid={self.page_num}&api_key={self.api_key}&user_id={self.user_id}'

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

    # Get a single image based on tags that the user enters.
    def get_single_post(self, tags=''):
        '''Pass in tags separated by a comma
        Using a dash before a tag will exclude it
        e.g. (cat ears, blue eyes, rating:safe, -nude)'''

        tags = self.__tagifier(tags)
        posts = []
        final_url = self.booru_url + f'&limit=100&tags={tags}&pid={self.page_num}&api_key={self.api_key}&user_id={self.user_id}'

        # This error should not ever happen
        try:
            urlobj = urlreq.urlopen(final_url)
            data = ET.parse(urlobj)
            urlobj.close()
            root = data.getroot()
        except ET.ParseError:
            return None
        
        # Reduce search if length of root is 0. Gives up if pid=0 has 0 results
        temp = 4
        attempts = 5
        while len(root) == 0:
            if attempts == 0:
                return None
            else:
                pass
            self.page_num = randint(0, temp)
            final_url = self.booru_url + f'&limit=100&tags={tags}&pid={self.page_num}&api_key={self.api_key}&user_id={self.user_id}'

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
        return image[0]
    
    # Chooses an image out of 5000000+ images!
    def get_random_post(self):
        '''Simply, returns a random image out of 5000000+ possible images.'''

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
            urlobj = urlreq.urlopen(final_url)
            data = ET.parse(urlobj)
            urlobj.close()
            root = data.getroot()
        except ET.ParseError:
            return None
        
        posts.append(root[0].attrib)
        image = self.__link_images(posts)
        return image[0]
        
    # Get comments from a post using post_id
    def get_comments(self, post_id):
        '''Pass in a post ID to get the comments for the post.
        If no comments are found, returns None.'''

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
            return None
        else:
            return comment_list
    
    # Get data for a post
    def get_post_data(self, post_id):
        '''Pass in a post ID to get ALL of the post's data.
        This includes the direct image url.'''

        data_url = f'https://gelbooru.com/index.php?page=dapi&s=post&q=index&id={post_id}'
        try:
            urlobj = urlreq.urlopen(data_url)
            data = ET.parse(urlobj)
            urlobj.close()
        except:
            return None

        root = data.getroot()

        return root[0].attrib
