import json
import urllib.request as urlreq
import random


"""
Works with gelbooru API.
"""

class gbooru:
    def __init__(self, limit=5, tags='', post_id=0):
        self.limit = limit
        self.tags = tags
        self.post_id = post_id
        self.page_num = random.randint(0, 19)
        self.booru_url = 'https://gelbooru.com/index.php?page=dapi&s=post&q=index&json=1'

    # Get a bunch of posts based on a limit that the user enters.
    def get_posts(self):
        final_url = self.booru_url + f'&limit={str(self.limit)}&tags={self.tags}&pid={self.page_num}'
        urlobj = urlreq.urlopen(final_url)
        json_response = json.load(urlobj)
        urlobj.close()
        temp = 4
        # Reduces search if json_response is an empty list
        while len(json_response) == 0: 
            self.page_num = random.randint(0, temp) 
            # Further reduction if random integer fails again
            if temp > 0:
                temp += -1
            else:
                pass
            final_url = self.booru_url + f'&limit={str(self.limit)}&tags={self.tags}&pid={self.page_num}'
            urlobj = urlreq.urlopen(final_url)
            json_response = json.load(urlobj)
            urlobj.close()

        images = self.__link_images(json_response)
        return images

    # Get a single image based on tags that the user enters.
    def get_single_post(self):
        post_url = self.booru_url + f'&limit={1}&tags={self.tags}&pid={self.page_num}'
        urlobj = urlreq.urlopen(post_url)
        json_response = json.load(urlobj)
        urlobj.close()
        temp = 4
        # Reduces search if json_response is an empty list
        while len(json_response) == 0:
            self.page_num = random.randint(0, temp)
            # Further reduction if random integer fails again
            if temp > 0:
                temp += -1
            else:
                pass
            post_url = self.booru_url + f'&limit={1}&tags={self.tags}&pid={self.page_num}'
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