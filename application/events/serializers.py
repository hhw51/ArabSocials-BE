from rest_framework import serializers
from .models import Event
from .models import EventRegistration
from django.contrib.auth import get_user_model
User = get_user_model()


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ['id', 'title', 'event_type', 'location', 'flyer', 'description', 'event_date', 'ticket_link', 'promo_code', 'user', 'approval_status', 'created_at', 'updated_at']


class EventRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventRegistration
        fields = ['id', 'status', 'registered_at', 'event', 'user',]

