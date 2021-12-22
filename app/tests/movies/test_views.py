import pytest

from movies.models import Movie


@pytest.mark.django_db
def test_add_movie(client):
    movies = Movie.objects.all()
    assert len(movies) == 0

    resp = client.post(
        '/movies/',
        {
            'title': 'The Matrix',
        },
        content_type='application/json'
    )
    assert resp.status_code == 201
    assert resp.data['title'] == 'The Matrix'
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
        {
            'title': 'ac2mc2cd9s0mc010c'
        },
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
        {
            'title': 'The Matrix',
            'year': '2030'
        },
        content_type='application/json'
    )
    assert resp.status_code == 201
    assert resp.data['title'] == 'The Matrix'
    assert resp.data['year'] != 'The 2030'


@pytest.mark.django_db
def test_list_all_movies(client, add_movie):
    first_movie = add_movie(title='The Matrix', genre='sci-fi', year='1999', runtime='150 min', body={})
    second_movie = add_movie(title='The Witcher', genre='fantasy', year='2019-', runtime='60min', body={})
    resp = client.get(f'/movies/')
    assert resp.data[0]['title'] == first_movie.title
    assert resp.data[1]['title'] == second_movie.title


@pytest.mark.django_db
def test_list_of_all_movies_can_be_filtered_by_genre(client, add_movie):
    first_movie = add_movie(title='The Matrix', genre='sci-fi', year='1999', runtime='150 min', body={})
    second_movie = add_movie(title='The Witcher', genre='fantasy', year='2019-', runtime='60min', body={})
    resp = client.get(f'/movies/?genre=fantasy')
    assert len(resp.data) == 1
    assert resp.data[0]['title'] == second_movie.title


@pytest.mark.django_db
def test_comment_can_be_added(client, add_movie):
    movie = add_movie(title='The Matrix', genre='sci-fi', year='1999', runtime='150 min', body={})
    resp = client.post(
        '/comments/',
        {
            'text': 'Great movie :chefskiss:',
            'movie_id': movie.id
        },
        content_type='application/json'
    )
    assert resp.status_code == 201
    assert resp.data['text'] == 'Great movie :chefskiss:'


@pytest.mark.django_db
def test_comment_is_not_added_if_no_text_is_provided(client, add_movie):
    movie = add_movie(title='The Matrix', genre='sci-fi', year='1999', runtime='150 min', body={})
    resp = client.post(
        '/comments/',
        {
            'movie_id': movie.id
        },
        content_type='application/json'
    )
    assert resp.status_code == 400
    assert resp.data['text'][0] == 'This field is required.'


@pytest.mark.django_db
def test_comment_is_not_added_if_no_movie_id_is_provided(client, add_movie):
    resp = client.post(
        '/comments/',
        {
            'text': 'Great movie :chefskiss:'
        },
        content_type='application/json'
    )
    assert resp.status_code == 400
    assert resp.data['movie_id'][0] == 'This field is required.'


@pytest.mark.django_db
def test_list_all_comments(client, add_comment):
    first_comment = add_comment(text='First movie comment', movie_id=1)
    second_comment = add_comment(text='Second movie comment', movie_id=2)
    resp = client.get(f'/comments/')
    assert resp.data[0]['text'] == first_comment.text
    assert resp.data[1]['text'] == second_comment.text


@pytest.mark.django_db
def test_list_all_comments(client, add_comment):
    first_comment = add_comment(text='First movie comment', movie_id=1)
    second_comment = add_comment(text='Second movie comment', movie_id=2)
    resp = client.get(f'/comments/?movie_id=1')
    assert len(resp.data) == 1
    assert resp.data[0]['text'] == first_comment.text
