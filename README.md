# SnakeBooru
[![License: GPL v3](https://img.shields.io/badge/License-GPL%20v3-blue.svg)](http://www.gnu.org/licenses/gpl-3.0)

Module to access booru sites APIs.

Working on Gelbooru support at the moment.

```
python -m pip install snakebooru
```

# Gelbooru

## Currently developing this part

### Searching

Currently, you can use the module to search images on Gelbooru.

This can be done as such
```python
from snakebooru.gelbooru import Gelbooru
# User ID and API key are optional. Access may be limited without them
# You can find both of these at https://gelbooru.com/index.php?page=account&s=home in Options
# Registration is required to obtain them. 
gelbooru = Gelbooru(api_key='API KEY', user_id='USER ID')

# Default limit is 100 images. 
results = gelbooru.get_posts(tags='cat ears, blue eyes, rating:safe', limit=5)

[{'Image 1 URL': 'https://img2.gelbooru.com/images/e9/a9/e9a9b46ca394abd8143ca766fa813852.png',
  'Post 1 URL': 'https://gelbooru.com/index.php?page=post&s=view&id=5440322'},
 {'Image 2 URL': 'https://img2.gelbooru.com/images/8c/c4/8cc44492be9b110e8110a7b75323f7f5.jpg',
  'Post 2 URL': 'https://gelbooru.com/index.php?page=post&s=view&id=5439959'},
 {'Image 3 URL': 'https://img2.gelbooru.com/images/d2/be/d2bed385da400e54baa37a394aae4531.png',
  'Post 3 URL': 'https://gelbooru.com/index.php?page=post&s=view&id=5439457'},
 {'Image 4 URL': 'https://img2.gelbooru.com/images/57/a8/57a8828055fe0f5dbdadc46f20fcc6fb.jpg',
  'Post 4 URL': 'https://gelbooru.com/index.php?page=post&s=view&id=5439388'},
 {'Image 5 URL': 'https://img2.gelbooru.com/images/4b/bb/4bbb1e77f8725f3664433836dec6a983.png',
  'Post 5 URL': 'https://gelbooru.com/index.php?page=post&s=view&id=5438978'},
  ...
```

### Search single post

Search single post with tags without having to use limit
Works similarly to get_random_post if you do not pass any arguments.

```python

from snakebooru.gelbooru import Gelbooru
# User ID and API key are optional. Access may be limited without them
# You can find both of these at https://gelbooru.com/index.php?page=account&s=home in Options
# Registration is required to obtain them. 
gelbooru = Gelbooru(api_key='API KEY', user_id='USER ID')

result = gelbooru.get_single_post(tags='cat ears, blue eyes, rating:safe')
[{'Image 1 URL': 'https://img2.gelbooru.com/images/9a/39/9a39574450f624d137411f274dff50dc.jpg',
  'Post 1 URL': 'https://gelbooru.com/index.php?page=post&s=view&id=5518121'}]

```

### Search random post

Search a random post. No arguments.

```python

from snakebooru.gelbooru import Gelbooru
# User ID and API key are optional. Access may be limited without them
# You can find both of these at https://gelbooru.com/index.php?page=account&s=home in Options
# Registration is required to obtain them. 
gelbooru = Gelbooru(api_key='API KEY', user_id='USER ID')

result = gelbooru.get_random_post()
[{'Image 1 URL': 'https://img2.gelbooru.com/images/4d/89/4d89189f94f42accc798ef38485c0e73.jpg',
  'Post 1 URL': 'https://gelbooru.com/index.php?page=post&s=view&id=5519568'}]

```


