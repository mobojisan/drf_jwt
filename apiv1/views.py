from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django.views import generic

from shop.models import Book
from .serializers import BookSerializer


class BookViewSet(viewsets.ModelViewSet, generic.ListView):
    # TODO: specify fields with .filter()
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    pagination_class = PageNumberPagination
