from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Customer
from .serializers import CustomerSerializers
from core.permissions import SecurityGroupCustomers


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
        SecurityGroupCustomers
    )
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filter_fields = ['company_name', 'address', 'contact_name', 'contact_phone', 'contact_job',
                     'contact_email', 'comments']
    search_fields = ['company_name', 'address', 'contact_name', 'contact_phone', 'contact_job',
                     'contact_email', 'comments']

    def potential_customer(self, request, **kwargs):
        queryset = self.get_queryset().filter(transformed=False)
        serializer = CustomerSerializers(queryset, many=True, context={'request': request})
        return Response(serializer.data)

    def transformed_customer(self, request, **kwargs):
        queryset = self.get_queryset().filter(transformed=True)
        serializer = CustomerSerializers(queryset, many=True, context={'request': request})
        return Response(serializer.data)

    def my_own_customers(self, request, **kwargs):
        queryset = self.get_queryset().filter(sales_contact=self.request.user)
        serializer = CustomerSerializers(queryset, many=True, context={'request': request})
        return Response(serializer.data)

    def my_own_customers_potential(self, request, **kwargs):
        queryset = self.get_queryset().filter(sales_contact=self.request.user, transformed=False)
        serializer = CustomerSerializers(queryset, many=True, context={'request': request})
        return Response(serializer.data)

    def my_own_customers_transformed(self, request, **kwargs):
        queryset = self.get_queryset().filter(sales_contact=self.request.user, transformed=True)
        serializer = CustomerSerializers(queryset, many=True, context={'request': request})
        return Response(serializer.data)

    def perform_create(self, serializer):
        if self.request.user.groups.filter(name="sales").exists():
            serializer.save(sales_contact=self.request.user)

    def perform_update(self, serializer):
        if self.request.user.groups.filter(name="sales").exists():
            serializer.save(sales_contact=self.request.user)

