from rest_framework import serializers
from .models import Contract


class ContractSerializers(serializers.ModelSerializer):

    class Meta:
        model = Contract
        fields = "__all__"

        extra_kwargs = {
            'date_created': {'read_only': True}
        }