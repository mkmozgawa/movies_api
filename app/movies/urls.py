from django.urls import path

from .views import MovieList, MovieCommentList

urlpatterns = [
    path('movies/', MovieList.as_view()),
    path('comments/', MovieCommentList.as_view()),
]
