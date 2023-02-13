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
from core.logger import log_request

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
    filter_fields = ['company_name', 'contact_name', 'contact_email']
    filterset_fields = {
        'contact_email': ["exact"],
        'contact_name': ["exact"],
        'company_name': ["exact"],
    }

    @action(detail=False, methods=['GET'])
    def potential_customer(self, request, **kwargs):
        queryset = self.get_queryset().filter(transformed=False)
        serializer = CustomerSerializers(queryset, many=True, context={'request': request})
        log_request(request)
        return Response(serializer.data)

    @action(detail=False, methods=['GET'])
    def transformed_customer(self, request, **kwargs):
        queryset = self.get_queryset().filter(transformed=True)
        serializer = CustomerSerializers(queryset, many=True, context={'request': request})
        log_request(request)
        return Response(serializer.data)

    @action(detail=False, methods=['GET'])
    def my_own_customers(self, request, **kwargs):
        queryset = self.get_queryset().filter(sales_contact=self.request.user)
        serializer = CustomerSerializers(queryset, many=True, context={'request': request})
        log_request(request)
        return Response(serializer.data)

    @action(detail=False, methods=['GET'])
    def my_own_customers_potential(self, request, **kwargs):
        queryset = self.get_queryset().filter(sales_contact=self.request.user, transformed=False)
        serializer = CustomerSerializers(queryset, many=True, context={'request': request})
        log_request(request)
        return Response(serializer.data)

    @action(detail=False, methods=['GET'])
    def my_own_customers_transformed(self, request, **kwargs):
        queryset = self.get_queryset().filter(sales_contact=self.request.user, transformed=True)
        serializer = CustomerSerializers(queryset, many=True, context={'request': request})
        log_request(request)
        return Response(serializer.data)

    # Over-write request.user on field sales_contact
    def perform_create(self, serializer):
        if self.request.user.groups.filter(name="sales").exists():
            log_request(self.request)
            new_customer = serializer.save(sales_contact=self.request.user)
            new_customer.save()

    # Over-write request.user on field sales_contact because user could change this field
    def perform_update(self, serializer):
        if self.request.user.groups.filter(name="sales").exists():
            log_request(self.request)
            update_customer = serializer.save(sales_contact=self.request.user)
            update_customer.save()

    def list(self, request, *args, **kwargs):
        log_request(request)
        return super().list(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        log_request(request)
        return super().retrieve(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        log_request(request)
        return super().create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        log_request(request)
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        log_request(request)
        return super().destroy(request, *args, **kwargs)