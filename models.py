'''Data models for movie trailer website'''

from collections import namedtuple

Movie = namedtuple('Movie', 'title, trailer_youtube_url, poster_image_url')
