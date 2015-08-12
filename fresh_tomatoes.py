import webbrowser
import os
import re
import csv
import models


CONFIG = {'STATIC_FILE_DIR': 'static',
          'TEMPLATE_DIR': 'templates'}


def load_template(template):
    '''load a template into a string object'''
    with open(os.path.join(CONFIG['TEMPLATE_DIR'], template)) as f:
        return f.read()


def render_template(template, **kwargs):
    '''load a template into a string object and substitute placeholders'''
    with open(os.path.join(CONFIG['TEMPLATE_DIR'], template)) as f:
        return f.read().format(**kwargs)


def create_movie_tiles_content(movies):
    # The HTML content for this section of the page
    content = ''

    # load_template once only to avoid unnecessary file access
    movie_tile_content = load_template('movie_tile.html')

    for movie in movies:
        # Extract the youtube ID from the url
        youtube_id_match = re.search(
            r'(?<=v=)[^&#]+', movie.trailer_youtube_url)
        youtube_id_match = youtube_id_match or re.search(
            r'(?<=be/)[^&#]+', movie.trailer_youtube_url)
        trailer_youtube_id = (youtube_id_match.group(0) if youtube_id_match
                              else None)

        # Append the tile for the movie with its content filled in
        content += movie_tile_content.format(
            movie_title=movie.title,
            poster_image_url=movie.poster_image_url,
            trailer_youtube_id=trailer_youtube_id
        )
    return content


def generate_movies_page(movies, output_filename='fresh_tomatoes.html'):
    '''Create or overwrite the output file and return its full path'''

    with open(output_filename, 'w') as output_file:

        # Replace the movie tiles placeholder generated content
        movie_tiles = create_movie_tiles_content(movies)
        rendered_content = render_template('main.html',
                                           movie_tiles=movie_tiles)

        output_file.write(rendered_content)
        return os.path.abspath(output_filename)


def open_movies_page(html_filename):
    '''open an html file in the browser (in a new tab, if possible)'''
    webbrowser.open('file://%s' % html_filename, new=2)


def main():
    '''Read movies from database, build static website and send to browser'''
    movies = [models.Movie._make(m) for m in csv.reader(open('movies.csv', 'r'))]
    html_filename = generate_movies_page(movies)
    open_movies_page(html_filename)


if __name__ == '__main__':

    main()
