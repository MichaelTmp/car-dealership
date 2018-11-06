from django.shortcuts import render
from django.views import generic
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework.pagination import PageNumberPagination

from showroom.models import Car, Manufacturer, Brand
from showroom.serializers import CarSerializer

class CarListPageNumberPagination(PageNumberPagination):
    page_size = 4
    page_size_query_param = 'page_size'
    max_page_size = 10

class CarViewSet(viewsets.ModelViewSet):
    serializer_class = CarSerializer
    pagination_class = CarListPageNumberPagination

    def get_queryset(self):
        queryset = Car.objects.all()

        manufacturer = self.request.query_params.get('manufacturer', None)
        brand = self.request.query_params.get('brand', None)
        order = self.request.query_params.get('order_by', None)

        if manufacturer is not None:
            manufacturer_id = Manufacturer.objects.get(name__iexact=manufacturer)
            queryset = queryset.filter(manufacturer=manufacturer_id)
        if brand is not None:
            brand_id = Brand.objects.get(name__iexact=brand)
            queryset = queryset.filter(brand=brand_id)
        if order is not None:
            if order == 'min_price':
                queryset = queryset.order_by('price')
            elif order == 'max_price':
                queryset = queryset.order_by('-price')
            
        return queryset


