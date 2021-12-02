import pytest

from movies.models import Movie


@pytest.mark.django_db
def test_movie_model():
    movie = Movie(title='Matrix')
    movie.save()
    assert movie.title == 'Matrix'
    assert str(movie) == movie.title
