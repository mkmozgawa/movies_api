# Create your views here.
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .adapters import OMDBApiAdapter
from .serializers import MovieSerializer


class MovieList(APIView):
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
