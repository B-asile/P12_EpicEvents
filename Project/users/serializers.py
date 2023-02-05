from rest_framework import serializers
from . import models


class UserSerializer(serializers.ModelSerializer):
    """Serialization de l'objet du profil utilisateur"""

    class Meta:
        model = models.User
        fields = ('id', 'email', 'first_name', 'last_name', 'password', 'group')
        """define security exception for API function with password"""
        extra_kwargs = {
            'password': {
                'write_only': True,
                'style': {'input_type': 'password'}
            }
        }

    def create(self, validated_data):
        """data validation"""
        user = models.User.objects.create_user(
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            password=validated_data['password'],
            group=validated_data['group']
        )
        return user

    def update(self, instance, validated_data):
        """Manage update user account"""
        if 'password' in validated_data:
            password = validated_data.pop('password')
            instance.set_password(password)

        return super().update(instance, validated_data)