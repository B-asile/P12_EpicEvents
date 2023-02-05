from rest_framework import serializers
from .models import Customer
from django.contrib.auth.models import Group
import re
from email_validator import validate_email, EmailNotValidError


class CustomerSerializers(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = '__all__'

    def validate(self, data):
        # Validate Phone number format
        phone_num = data.get('contact_phone')
        if not re.match(r'^\d{10,15}$', phone_num):
            raise serializers.ValidationError({'contact_phone': "Invalid phone number format."})
        # Validate sales_contact is in 'sales' group
        sales_group = Group.objects.get(name='sales')
        if not sales_group.user_set.filter(id=data['sales_contact'].id).exists():
            raise serializers.ValidationError({'sales_contact': 'Sales contact must be a member of the sales group.'})
        # Validate email format
        try:
            validate_email(data['contact_email'])
        except EmailNotValidError as e:
            raise serializers.ValidationError({'contact_email': str(e)})
        return data