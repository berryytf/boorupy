import json
import urllib.request as urlreq
import random


"""
Works with gelbooru API.
"""

class gbooru:
    def __init__(self, limit=5, page_num=0, tags='', post_id=0):
        self.limit = limit
        self.page_num = page_num
        self.tags = tags
        self.post_id = post_id
        self.booru_url = 'https://gelbooru.com/index.php?page=dapi&s=post&q=index&json=1'

    #Get a bunch of posts based on a limit that the user enters.
    def get_posts(self):
        final_url = self.booru_url + f'&limit={str(self.limit)}&tags={self.tags}&pid={self.page_num}'
        
        urlobj = urlreq.urlopen(final_url)
        json_response = json.load(urlobj)
        urlobj.close()

        test = self.__link_images(json_response)
        return test

    def __link_images(self, response):
        image_list = []
        temp_dict = dict()
        temp = 1
        post_url = 'https://gelbooru.com/index.php?page=post&s=view&id='
        for i in range(len(response)):
            temp_dict[f'Image {temp} URL'] = response[i]['file_url']
            temp_dict[f'Post {temp} URL'] = post_url + f'{response[i]["id"]}'
            image_list.append(temp_dict)
            temp_dict = dict()
            temp += 1
        
        return image_list # Returns image URLs and post URLs in a list
        

