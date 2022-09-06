from cgitb import lookup
from dataclasses import fields
from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django.views import generic
from django_filters import rest_framework as filters
from shop.models import Book
from .serializers import BookSerializer


class BookFilter(filters.FilterSet):
    price__gte = filters.NumberFilter(field_name='price', lookup_expr='gte')
    
    class Meta:
        model = Book
        fields = '__all__'

class BookViewSet(viewsets.ModelViewSet, generic.ListView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = BookFilter
    filterset_fields = '__all__'
    permission_classes = [IsAuthenticatedOrReadOnly]
    pagination_class = PageNumberPagination
