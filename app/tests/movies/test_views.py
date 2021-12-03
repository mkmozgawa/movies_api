import pytest

from movies.models import Movie


@pytest.mark.django_db
def test_add_movie(client):
    movies = Movie.objects.all()
    assert len(movies) == 0

    resp = client.post(
        '/movies/',
        {
            'title': 'Matrix',
        },
        content_type='application/json'
    )
    assert resp.status_code == 201
    assert resp.data['title'] == 'Matrix'
    assert resp.data['genre']
    assert resp.data['year']
    assert resp.data['runtime']
    assert resp.data['body']

    movies = Movie.objects.all()
    assert len(movies) == 1


@pytest.mark.django_db
def test_add_movie_with_missing_data(client):
    movies = Movie.objects.all()
    assert len(movies) == 0

    resp = client.post(
        '/movies/',
        {},
        content_type='application/json'
    )
    assert resp.status_code == 400
    assert resp.data['Error'] == 'Could not fetch movie data, please change your query and try again.'

    movies = Movie.objects.all()
    assert len(movies) == 0


@pytest.mark.django_db
def test_add_movie_with_nonexistent_title(client):
    movies = Movie.objects.all()
    assert len(movies) == 0

    resp = client.post(
        '/movies/',
        {'title': 'ac2mc2cd9s0mc010c'},
        content_type='application/json'
    )
    assert resp.status_code == 400
    assert resp.data[
               'Error'] == 'Could not fetch movie data, please change your query and try again.'

    movies = Movie.objects.all()
    assert len(movies) == 0


@pytest.mark.django_db
def test_add_movie_other_user_provided_parameters_are_ignored(client):
    resp = client.post(
        '/movies/',
        {'title': 'Matrix',
         'year': '2030'},
        content_type='application/json'
    )
    assert resp.status_code == 201
    assert resp.data['title'] == 'Matrix'
    assert resp.data['year'] != '2030'
