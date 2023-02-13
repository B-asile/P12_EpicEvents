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
from rest_framework.exceptions import PermissionDenied

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
    filter_fields = [
        '^company_name__contact_name',
        '^company_name__contact_email',
        '^company_name__company_name',
    ]
    filterset_fields = {
        'date_created': ['gte', 'lte'],
        'amount': ['gte', 'lte'],
        'contract_status': ['exact'],
        'company_name': ['exact'],
        'company_name__contact_email': ['exact'],
    }

    @action(detail=False, methods=['GET'])
    def my_own_contracts(self, request, **kwargs):
        queryset = self.get_queryset().filter(sales_contact=self.request.user)
        serializer = ContractSerializers(queryset, many=True, context={'request': request})
        log_request(request)
        return Response(serializer.data)

    def perform_create(self, serializer):
        # Search company_name requested in Customer list
        contract_customer_id = self.request.data.get('company_name', None)
        customer = Customer.objects.filter(id=contract_customer_id).first()
        # if sales_contact of customer searched == requester name
        if self.request.user.groups.filter(name='sales').exists():
            # create contracts, push his account in contract field: sales_contact
            if str(customer.sales_contact) == str(self.request.user.email) :
                new_contract = serializer.save(sales_contact=self.request.user,
                                               date_created = datetime.now().strftime("%Y-%m-%d"),
                                               contract_status='open')
                new_contract.save()

        # if requester superadmin or manager
        if self.request.user.is_superuser or \
                self.request.user.groups.filter(name='management').exists():
            new_contract = serializer.save(date_created = datetime.now().strftime("%Y-%m-%d"),
                                           contract_status='open')
            new_contract.save()
        # if contract is create, search company_name(at top of function) and push 'transfomed' = True
        customer.transformed = True
        log_request(self.request)
        customer.save()

    def perform_update(self, serializer):
        if self.request.user.groups.filter(name='sales').exists():
            update_contract = serializer.save(sales_contact=self.request.user,
                                              date_updated = datetime.now().strftime("%Y-%m-%d"))
            update_contract.save()
        # if contract_status push to signed, auto create Event
        # Get the contract status from the request data
        contract_status = self.request.data.get('contract_status', None)
        if contract_status == 'signed':
            # Create a new Event object
            event = Event.objects.create(
                event_name=f"Event for Contract #{serializer.instance.id}",
                event_status='open',
                created_date=datetime.now().strftime("%Y-%m-%d"),
                company_name=serializer.instance.company_name,
                sales_contact=serializer.instance.sales_contact,
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