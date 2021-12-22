# Create your views here.
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .adapters import OMDBApiAdapter
from .serializers import MovieSerializer, MovieCommentSerializer
from .models import Movie, MovieComment


class MovieList(APIView):
    def get(self, request, format=None):
        movies = Movie.objects.all()
        if genre := self.request.query_params.get('genre'):
            movies = movies.filter(genre=genre)
        serializer = MovieSerializer(movies, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        try:
            api_data = OMDBApiAdapter().get_movie_data(request.data['title'])
        except KeyError:
            return Response(
                {'Error': 'Could not fetch movie data, please change your query and try again.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        serializer = MovieSerializer(data=api_data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MovieCommentList(APIView):
    def get(self, request, format=None):
        comments = MovieComment.objects.all()
        if movie_id := self.request.query_params.get('movie_id'):
            comments = comments.filter(movie_id=movie_id)
        serializer = MovieCommentSerializer(comments, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = MovieCommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
