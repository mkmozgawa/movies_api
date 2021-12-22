from rest_framework import serializers

from .models import Movie, MovieComment


class MovieSerializer(serializers.ModelSerializer):
    title = serializers.CharField()

    class Meta:
        model = Movie
        fields = '__all__'
        read_only_fields = ('id', 'created_date', 'updated_date',)


class MovieCommentSerializer(serializers.ModelSerializer):
    text = serializers.CharField()
    movie_id = serializers.IntegerField()

    class Meta:
        model = MovieComment
        fields = ['text', 'movie_id']
        read_only_fields = ('id', 'created_date',)
