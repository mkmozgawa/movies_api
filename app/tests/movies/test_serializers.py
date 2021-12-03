from movies.serializers import MovieSerializer


def test_valid_movie_serializer():
    valid_serializer_data = {
        'title': 'Matrix',
        'genre': 'Action, Drama, Fantasy',
        'year': '1993',
        'runtime': '60 min',
        'body': {},
    }
    serializer = MovieSerializer(data=valid_serializer_data)
    assert serializer.is_valid()
    assert serializer.validated_data == valid_serializer_data
    assert serializer.data == valid_serializer_data
    assert serializer.errors == {}


def test_invalid_movie_serializer():
    invalid_serializer_data = {}
    serializer = MovieSerializer(data=invalid_serializer_data)
    assert not serializer.is_valid()
    assert serializer.validated_data == {}
    assert serializer.errors['title']
