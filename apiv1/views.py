from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from shop.models import Book
from .serializers import BookSerializer


class BookViewSet(viewsets.ModelViewSet):
    # TODO: specify fields with .filter()
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    # TODO: specify a number as a query parameter, like /?limit=1
    pagination_class = PageNumberPagination
