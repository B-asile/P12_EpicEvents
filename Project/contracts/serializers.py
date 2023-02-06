from rest_framework import serializers
from .models import Contract


class ContractSerializers(serializers.ModelSerializer):

    class Meta:
        model = Contract
        fields = "__all__"

        extra_kwargs = {'sales_contact': {'read_only': True}}