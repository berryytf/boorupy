import asyncio
import aiohttp
import xml.etree.ElementTree as ET
from random import randint
from typing import *
from furl import furl

"""Access Gelbooru"s API"""

class DataContainer:
    """Image container for results
    Meant to be used with get_post_data"""

    def __init__(self, payload: dict):
        self.data           = payload
        self.id             = int(payload.get("id"))
        self.height         = int(payload.get("height"))
        self.width          = int(payload.get("width"))
        self.sample_height  = int(payload.get("sample_height"))
        self.sample_width   = int(payload.get("sample_width"))
        self.preview_width  = int(payload.get("preview_width"))
        self.preview_height = int(payload.get("preview_height"))
        self.score          = int(payload.get("score"))
        self.change         = int(payload.get("change"))
        self.file_url       = payload.get("file_url")
        self.parent_id      = payload.get("parent_id")
        self.sample_url     = payload.get("sample_url")
        self.preview_url    = payload.get("preview_url")
        self.rating         = payload.get("rating")
        self.tags           = payload.get("tags")
        self.md5            = payload.get("md5")
        self.creator_id     = payload.get("creator_id")
        self.has_children   = payload.get("has_children")
        self.created_at     = payload.get("created_at")
        self.status         = payload.get("status")
        self.source         = payload.get("source")
        self.has_notes      = payload.get("has_notes")
        self.has_comments   = payload.get("has_comments")

    async def show_all_data(self) -> dict:
        """Get all data for post"""

        return self.data

    async def show_tags(self) -> tuple:
        """Get all tags for a post including the rating"""

        tags = self.tags.strip().split(" ")
        if self.rating == "s":
            tags.append("rating:safe")
        if self.rating == "q":
            tags.append("rating:questionable")
        if self.rating == "e":
            tags.append("rating:explicit")

        return tuple(tags)

    async def show_comments(self) -> tuple or None:
        """Get comments for a post"""

        if self.has_comments == "false":
            return None

        comments = await Gelbooru().get_comments(self.id)
        return tuple(comments)

    # Each post has a full size image, sample image and preview image.
    async def show_links(self) -> tuple:
        """Get the different image urls for a post"""

        links = (self.file_url, self.sample_url, self.preview_url)

        return links

class Gelbooru:

    def __init__(self, api_key: Optional[str] = None,
                    user_id: Optional[str] = None,
                    loop: Optional[asyncio.AbstractEventLoop] = None):

        self.api_key        = api_key
        self.user_id        = user_id
        self.booru_url      = "https://gelbooru.com/"
        self.loop           = loop

    async def __fetch(self, session, url) -> bytes or tuple:
        async with session.get(url) as response:
            return response.status, await response.read()

    async def __request(self, url):
        async with aiohttp.ClientSession(loop=self.loop) as session:
            code, response = await self.__fetch(session, url)

        if code not in [200, 201]:
            raise Exception(f"""Site returned a non-200 status code: {response}""")

        # This error will probably never be raised
        if response.decode("utf-8") == "Too deep! Pull it back some. Holy fuck.":
            raise Exception("Site returned an error. Try lowering the offset.")

        return response

    def __endpoint(self, s) -> furl:

        endpoint = furl(self.booru_url)
        endpoint.args["page"] = "dapi"
        endpoint.args["s"] = s
        endpoint.args["q"] = "index"

        # Add api key and user ID if possible
        if self.api_key:
            endpoint.args["api_key"] = self.api_key
        if self.user_id:
            endpoint.args["user_id"] = self.user_id

        return endpoint

    # Private function to create a post URL and a related image URL
    def __link_images(self, response):

        image_list = []
        temp_dict = dict()

        post_url = "https://gelbooru.com/index.php?page=post&s=view&id="
        for i in response:
            post_id = i['id']
            image_url = i['file_url']
            temp_dict['post_url'] = post_url + f'{post_id}'
            temp_dict['image_url'] = image_url
            temp_dict['id'] = post_id
            image_list.append(temp_dict)
            temp_dict = dict()

        return image_list

    def __tagifier(self, tags, rating) -> list:

        if rating:
            tags = tags + f""", rating:{rating}"""

        tags = [tag.strip().lower().replace(" ", "_") for tag in tags.split(", ")] if tags else []
        return tags

    # Get a bunch of posts based on a limit and tags that the user enters.
    async def get_posts(self, tags="", limit=100, offset=0, rating="") -> list or None:
        """Raises:
            Exception: Limit parameter cannot be greater than 100
            Exception: Offset is too high

        Keyword Arguments:
            tags (str, optional): tags separated by a comma. Defaults to ""
            limit (int, optional): limit number of posts. defaults to 100
            offset (int, optional): defaults to 0. Cannot be higher than (100 - limit) + 200
            rating (str, optional): safe, questionable or explicit

        Returns:
            [type]: list

        Notes:
            If limit = 50 then offset can be 250"""

        if limit > 100:
            raise Exception("Limit parameter cannot be greater than 100")
        if offset > (100 - limit) + 200:
            raise Exception("Offset is too high.")

        posts = []
        tags = self.__tagifier(tags, rating)
        endpoint = self.__endpoint("post")
        endpoint.args["limit"] = limit
        endpoint.args["pid"] = offset
        endpoint.args["tags"] = " ".join(tags)

        results = await self.__request(str(endpoint))
        try:
            results = ET.fromstring(results)
        except ET.ParseError:
            raise Exception("Parsing error. Endpoint may be inappropriate.")

        temp = 4
        attempts = 5

        # Offset is randomly set between 0 and 4 until results are found
        # If no results found at offset = 0: returns none
        # This is so no results are missed if obscure tags are passed
        while not results:
            if attempts == 0:
                return None

            endpoint.args["pid"] = randint(0, temp)
            results = await self.__request(str(endpoint))
            try:
                results = ET.fromstring(results)
            except ET.ParseError:
                raise Exception("Parsing error. Endpoint may be inappropriate.")

            temp += -1
            attempts += -1

        for post in results:
            posts.append(post.attrib)

        images = self.__link_images(posts)
        return images

    # Get a single image based on tags that the user enters.
    # Similar to get_random_post but you pass in tags
    async def get_single_post(self, tags="", rating="") -> dict or str:
        """Keyword Arguments:
            tags (str, optional): tags separated by a comma. Defaults to "".
            rating (str, optional): safe, questionable or explicit

        Returns:
            [type]: dict"""

        tags = self.__tagifier(tags, rating)
        posts = []
        endpoint = self.__endpoint("post")
        endpoint.args["limit"] = 100

        # Random offset to get a random image based on tags
        endpoint.args["pid"] = randint(0, 200)
        endpoint.args["tags"] = " ".join(tags)

        results = await self.__request(str(endpoint))

        try:
            results = ET.fromstring(results)
        except ET.ParseError:
            raise Exception("Parsing error. Endpoint may be inappropriate.")

        temp = 4
        attempts = 4
        while not results:
            if attempts == 0:
                return "No results after 5 attempts."

            endpoint.args["pid"] = randint(0, temp)
            results = await self.__request(str(endpoint))
            try:
                results = ET.fromstring(results)
            except ET.ParseError:
                raise Exception("Parsing error. Endpoint may be inappropriate.")
            temp += -1
            attempts += -1

        for post in results:
            posts.append(post.attrib)

        posts = [posts[randint(0, len(results)-1)]]
        image = self.__link_images(posts)
        return image[0]

    # Random image :D
    async def get_random_post(self) -> dict:
        """Returns:
            [type]: dict"""

        posts = []
        endpoint = self.__endpoint("post")
        endpoint.args["limit"] = 100
        endpoint.args["pid"] = randint(0, 200)
        results = await self.__request(str(endpoint))

        try:
            results = ET.fromstring(results)
        except ET.ParseError:
            raise Exception("Parsing error. Endpoint may be inappropriate.")

        posts.append(results[randint(0,99)].attrib)
        image = self.__link_images(posts)
        return image[0]

    # Get comments from a post using post_id
    async def get_comments(self, post_id) -> tuple or None:
        """Keyword Arguments:
            post_id (int): post id

        Returns:
            [type]: tuple"""

        comment_list = []
        endpoint = self.__endpoint("comment")
        endpoint.args["post_id"] = post_id

        results = await self.__request(str(endpoint))
        try:
            results = ET.fromstring(results)
        except ET.ParseError:
            raise Exception("Parsing error. Endpoint may be inappropriate.")

        temp = dict()

        # Iterate through comments
        for i in range(len(results)):
            temp["id"] = results[i].attrib["id"]
            temp["author"] = results[i].attrib["creator"]
            temp["date"] = results[i].attrib["created_at"]
            temp["comment"] = results[i].attrib["body"]

            comment_list.append(temp)
            temp = dict()

        # Returns None no comments
        if not comment_list:
            return None
        else:
            return tuple(comment_list)

    # Get data for a post
    async def get_post_data(self, post_id) -> Optional[DataContainer]:
        """Args:
            post_id (int): post id

        Returns:
            DataContainer (object)"""

        endpoint = self.__endpoint("post")
        endpoint.args["id"] = post_id
        results = await self.__request(str(endpoint))

        try:
            results = ET.fromstring(results)
        except ET.ParseError:
            raise Exception("Parsing error. Endpoint may be inappropriate.")

        return DataContainer(results[0].attrib)
