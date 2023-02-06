from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from rest_framework.decorators import action

from .models import Event
from .serializers import EventSerializers
from core.permissions import SecurityGroupEvents
from core.logger import log_request
from datetime import datetime


class EventApiView(viewsets.ModelViewSet):
    """
        SECTION EVENT :
        CRUD => Management
        CRU => Sales (own project)
        RU => Support
    """
    serializer_class = EventSerializers
    queryset = Event.objects.all()
    permission_classes = (
        IsAuthenticated,
        SecurityGroupEvents
    )
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filter_fields = ['event_name', 'event_status', 'start_date', 'end_date', 'attendees', 'description', 'company_name']
    search_fields = ['event_name', 'event_status', 'start_date', 'end_date', 'attendees', 'description', 'company_name']

    @action(detail=False, methods=['GET'])
    def my_sales_events(self, request, **kwargs):
        queryset = self.get_queryset().filter(sales_contact=self.request.user)
        serializer = EventSerializers(queryset, many=True, context={'request': request})
        log_request(request)
        return Response(serializer.data)

    @action(detail=False, methods=['GET'])
    def my_support_events(self, request, **kwargs):
        queryset = self.get_queryset().filter(support_contact=self.request.user)
        serializer = EventSerializers(queryset, many=True, context={'request': request})
        log_request(request)
        return Response(serializer.data)

    def perform_update(self, serializer):
        if self.request.user.groups.filter(name='sales').exists():
            update_contract = serializer.save(sales_contact=self.request.user,
                                              updated_date = datetime.now().strftime("%Y-%m-%d"))
            update_contract.save()
        if self.request.user.groups.filter(name='support').exists():
            update_contract = serializer.save(support_contact=self.request.user,
                                              updated_date = datetime.now().strftime("%Y-%m-%d"))
            update_contract.save()

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