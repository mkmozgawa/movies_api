import pytest

from movies.models import Movie, MovieComment


@pytest.fixture(scope='function')
def add_movie():
    def _add_movie(title, genre=None, year=None, runtime=None, body=None):
        movie = Movie.objects.create(title=title, genre=genre, year=year, runtime=runtime, body=body)
        return movie
    return _add_movie


@pytest.fixture(scope='function')
def add_comment():
    def _add_comment(text, movie_id):
        comment = MovieComment.objects.create(text=text, movie_id=movie_id)
        return comment
    return _add_comment
