import pytest

from movies.models import Movie


@pytest.fixture(scope='function')
def add_movie():
    def _add_movie(title, genre=None, year=None, runtime=None, body=None):
        movie = Movie.objects.create(title=title, genre=genre, year=year, runtime=runtime, body=body)
        return movie
    return _add_movie
