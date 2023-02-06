from rest_framework import serializers
from .models import Event


class EventSerializers(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = "__all__"

        extra_kwargs = {'sales_contact': {'read_only': True}}