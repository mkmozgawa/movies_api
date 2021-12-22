import django.db.utils
import pytest

from movies.models import Movie, MovieComment


@pytest.mark.django_db
def test_movie_model_is_added():
    movie = Movie(title='The Matrix')
    movie.save()
    assert movie.title == 'The Matrix'
    assert str(movie) == movie.title


@pytest.mark.django_db
def test_movie_model_is_not_added_if_no_title():
    movie = Movie()
    with pytest.raises(django.db.utils.IntegrityError):
        movie.save()


@pytest.mark.django_db
def test_movie_comment_is_added():
    movie = Movie(title='The Matrix')
    movie.save()
    movie_comment = MovieComment(text='Great movie, highly recommended', movie_id=movie.id)
    movie_comment.save()
    assert movie_comment.text == 'Great movie, highly recommended'
    assert str(movie_comment) == movie_comment.text


@pytest.mark.django_db
def test_movie_comment_is_not_added_if_no_comment_text():
    movie = Movie(title='The Matrix')
    movie.save()
    movie_comment = MovieComment(movie_id=movie.id)
    with pytest.raises(django.db.utils.IntegrityError):
        movie_comment.save()


@pytest.mark.django_db
def test_movie_comment_is_not_added_if_no_movie_id():
    movie = Movie(title='The Matrix')
    movie.save()
    movie_comment = MovieComment(text='Great movie, highly recommended')
    with pytest.raises(django.db.utils.IntegrityError):
        movie_comment.save()
