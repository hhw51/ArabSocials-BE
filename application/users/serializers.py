from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id', 
            'name', 
            'email', 
            'phone', 
            'location', 
            'marital_status', 
            'interests', 
            'profession', 
            'social_links',
            'image', 
            'password'
        ]
        extra_kwargs = {
            'password': {'write_only': True},  # To make password write-only
        }

    def create(self, validated_data):
        """
        Override create method to hash the password before saving
        """
        user = User(**validated_data)
        user.set_password(validated_data['password'])  # Hash the password
        user.save()
        return user

    def update(self, instance, validated_data):
        """
        Override update method to handle password hashing on update if password is changed
        """
        password = validated_data.get('password', None)
        if password:
            instance.set_password(password)  # Hash the password if it's being updated
        return super().update(instance, validated_data)







class EmailSerializer(serializers.Serializer):
    email = serializers.EmailField()