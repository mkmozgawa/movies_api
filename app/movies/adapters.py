import requests

from drf_project.settings import OMDB_API_KEY, OMDB_API_URL


class OMDBApiAdapter:
    def __init__(self):
        self.api_key = OMDB_API_KEY
        self.api_url = OMDB_API_URL

    def get_movie_data(self, title):
        response = requests.get(f'{self.api_url}?t={title}&apikey={self.api_key}').json()
        if 'Error' in response.keys():
            raise KeyError
        movie_data = {'title': response['Title'],
                      'genre': response['Genre'],
                      'year': response['Year'],
                      'runtime': response['Runtime'],
                      'body': response
                      }
        return movie_data
