from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from rest_framework.decorators import action
from datetime import datetime

from .models import Contract
from .serializers import ContractSerializers
from core.permissions import SecurityGroupContracts
from core.logger import log_request

from customers.models import Customer
from events.models import Event


class ContractApiView(viewsets.ModelViewSet):
    """
        SECTION CONTRACTS :
        CRUD => Management
        CRU => Sales (own project)
        R ==> Support & Sales
    """
    serializer_class = ContractSerializers
    queryset = Contract.objects.all()
    permission_classes = (
        IsAuthenticated,
        SecurityGroupContracts
    )
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filter_fields = ['date_create', 'date_updated', 'commitments', 'amount',
                     'payment_due', 'contract_status', 'company_name', 'sales_contact']
    search_fields = ['date_create', 'date_updated', 'commitments', 'amount',
                     'payment_due', 'contract_status', 'company_name', 'sales_contact']

    @action(detail=False, methods=['GET'])
    def my_own_contracts(self, request, **kwargs):
        queryset = self.get_queryset().filter(sales_contact=self.request.user)
        serializer = ContractSerializers(queryset, many=True, context={'request': request})
        log_request(request)
        return Response(serializer.data)

    def perform_create(self, serializer):
        # if sales create contracts, push his account in field sales_contact
        if self.request.user.groups.filter(name="sales").exists():
            serializer.save(sales_contact=self.request.user, date_create = datetime.now)
        # Force contract_status to be "open"
        serializer.validated_data['contract_status'] = 'open'
        # if contract is create, search company_name and push 'transfomed' = True
        company_name = self.request.data.get('company_name', None)
        customer = Customer.objects.filter(company_name=company_name).first()
        # .first() to obtain just one customer obj
        customer.transformed = True
        log_request(self.request)
        customer.save()

    def perform_update(self, serializer):
        if self.request.user.groups.filter(name="sales").exists():
            serializer.save(sales_contact=self.request.user, date_updated = datetime.now)
        # if contract_status push to signed, auto create Event
        # Get the contract status from the request data
        contract_status = self.request.data.get('contract_status', None)
        if contract_status == 'signed':
            # Create a new Event object
            event = Event.objects.create(
                event_name=f"Event for Contract #{self.object.pk}",
                event_status='open',
                created_date= datetime.now,
                company_name=self.object.company_name,
                sales_contact=self.object.sales_contact,
            )

            log_request(self.request)
            event.save()

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