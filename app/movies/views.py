import json

from django.shortcuts import render

# Create your views here.
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

import requests

from movies.serializers import MovieSerializer
from drf_project.settings import OMDB_API_KEY


class MovieList(APIView):
    def post(self, request, format=None):
        if 'title' not in request.data.keys():
            return Response(
                           {'Error': 'Movie title missing, please add one like this: {"title": "your title"} and try '
                                     'again.'},
                           status=status.HTTP_400_BAD_REQUEST
            )
        api_data = requests.get(f'http://www.omdbapi.com/?t={request.data["title"]}&apikey={OMDB_API_KEY}').json()
        if 'Error' in api_data.keys():
            return Response(
                            {'Error': 'Could not fetch movie data, please change your query and try again.'},
                            status=status.HTTP_400_BAD_REQUEST
            )
        movie_data = {'title': api_data['Title'],
                      'genre': api_data['Genre'],
                      'year': api_data['Year'],
                      'runtime': api_data['Runtime']
        }
        serializer = MovieSerializer(data=movie_data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
