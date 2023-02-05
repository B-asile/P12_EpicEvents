from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Customer
from .serializers import CustomerSerializers
from core.permissions import SecurityGroupGlobalview, SecurityGroupWorkSpaceCustomers


class CustomerApiView(viewsets.ModelViewSet):
    """
    SECTION CUSTOMER :
                CRUD => Management
                CRU => Sales (own project)
                SAFE_METHODS ==> Support & Sales
    """
    serializer_class = CustomerSerializers
    queryset = Customer.objects.all()
    permission_classes = (
        IsAuthenticated,
        SecurityGroupGlobalview
    )
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filter_fields = ['company_name', 'address', 'contact_name', 'contact_phone', 'contact_job',
                     'contact_email', 'comments']
    search_fields = ['company_name', 'address', 'contact_name', 'contact_phone', 'contact_job',
                     'contact_email', 'comments']

    @action(detail=False, methods=['GET', 'POST', 'PUT', 'PATCH', 'DELETE'],
            permission_classes=[SecurityGroupGlobalview])
    def potential_customer(self, request, **kwargs):
        queryset = self.get_queryset().filter(transformed=False)
        serializer = CustomerSerializers(queryset, many=True, context={'request': request})
        return Response(serializer.data)

    @action(detail=False, methods=['GET', 'POST', 'PUT', 'PATCH', 'DELETE'],
            permission_classes=[SecurityGroupGlobalview])
    def transformed_customer(self, request, **kwargs):
        queryset = self.get_queryset().filter(transformed=True)
        serializer = CustomerSerializers(queryset, many=True, context={'request': request})
        return Response(serializer.data)

    @action(detail=False, methods=['GET', 'POST', 'PUT', 'PATCH'],
            permission_classes=[SecurityGroupWorkSpaceCustomers])
    def my_own_customers(self, request, **kwargs):
        queryset = self.get_queryset().filter(sales_contact=self.request.user)
        serializer = CustomerSerializers(queryset, many=True, context={'request': request})
        return Response(serializer.data)

    @action(detail=False, methods=['GET', 'POST', 'PUT', 'PATCH'],
            permission_classes=[SecurityGroupWorkSpaceCustomers])
    def my_own_customers_potential(self, request, **kwargs):
        queryset = self.get_queryset().filter(sales_contact=self.request.user, transformed=False)
        serializer = CustomerSerializers(queryset, many=True, context={'request': request})
        return Response(serializer.data)

    @action(detail=False, methods=['GET', 'POST', 'PUT', 'PATCH'],
            permission_classes=[SecurityGroupWorkSpaceCustomers])
    def my_own_customers_transformed(self, request, **kwargs):
        queryset = self.get_queryset().filter(sales_contact=self.request.user, transformed=True)
        serializer = CustomerSerializers(queryset, many=True, context={'request': request})
        return Response(serializer.data)
