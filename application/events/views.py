import logging
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.authentication import get_authorization_header
from .models import Event, EventRegistration
from .serializers import EventSerializer, EventRegistrationSerializer
from rest_framework.authtoken.models import Token
from django.views.decorators.csrf import csrf_exempt
from rest_framework.permissions import AllowAny
from django.contrib.auth.models import User
logger = logging.getLogger(__name__)

@csrf_exempt  # Exempt CSRF for API views (use with caution in production)
@api_view(['POST'])
@permission_classes([AllowAny])
def create_event(request):
    """
    A function-based view to handle event creation.
    It receives a Bearer token in the header and event details in the body.
    The event is created for the authenticated user.
    """
    if request.method == 'POST':
        # Extract event data from request body
        data = request.data

        # Check if all required fields are provided in the request
        required_fields = ['title', 'event_type', 'location', 'description', 'event_date']
        for field in required_fields:
            if field not in data:
                return Response({'error': f'{field} is required.'}, status=status.HTTP_400_BAD_REQUEST)

        # Extract the token from the request headers
        token = get_authorization_header(request).split()

        if len(token) != 2 or token[0].lower() != b'bearer':
            raise AuthenticationFailed('Invalid token header. No credentials provided.')

        try:
            # Validate the token
            token = token[1].decode('utf-8')
            user_token = Token.objects.get(key=token)
            user = user_token.user  # Get the user associated with the token
        except Token.DoesNotExist:
            raise AuthenticationFailed('Invalid token.')

        # Create the event
        try:
            event = Event.objects.create(
                title=data['title'],
                event_type=data['event_type'],
                location=data['location'],
                flyer=data.get('flyer', None),  # Optional: flyer can be None
                description=data['description'],
                event_date=data['event_date'],
                ticket_link=data.get('ticket_link', None),  # Optional: ticket link can be None
                promo_code=data.get('promo_code', None),  # Optional: promo code can be None
                user=user  # Associate the event with the authenticated user
            )

            # Serialize the event data
            event_serializer = EventSerializer(event)

            # Return the created event details and a success response
            return Response(event_serializer.data, status=status.HTTP_201_CREATED)  # Correct usage of status.HTTP_201_CREATED

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)







@csrf_exempt  
@api_view(['POST'])
@permission_classes([AllowAny])
def register_event(request):
    """
    A function-based view to handle event registration.
    It receives a Bearer token in the header and event_id and status in the body.
    The user is registered for the event with the provided status.
    """
    if request.method == 'POST':
        # Extract event data from request body
        data = request.data

        # Check if event_id and status are provided
        if 'event_id' not in data or 'status' not in data:
            logger.warning("Missing required fields: event_id or status")
            return Response({'error': 'event_id and status are required.'}, status=status.HTTP_400_BAD_REQUEST)

        event_id = data['event_id']
        status1 = data['status']  # Expected status: 'registered' or 'cancelled'

        # Extract the token from the request headers
        token = get_authorization_header(request).split()

        if len(token) != 2 or token[0].lower() != b'bearer':
            logger.error("Invalid token header: No credentials provided")
            raise AuthenticationFailed('Invalid token header. No credentials provided.')

        try:
            # Validate the token
            token = token[1].decode('utf-8')
            user_token = Token.objects.get(key=token)
            user = user_token.user  # Get the user associated with the token
            logger.info(f"Token validated successfully for user: {user.username}")
        except Token.DoesNotExist:
            logger.error("Invalid token: Token does not exist")
            raise AuthenticationFailed('Invalid token.')

        # Check if the event exists
        try:
            event = Event.objects.get(id=event_id)
            logger.info(f"Event found: {event.title}")
        except Event.DoesNotExist:
            logger.error(f"Event with ID {event_id} not found")
            return Response({'error': 'Event not found.'}, status=status.HTTP_404_NOT_FOUND)

        # Check if the user is already registered for the event
        registration = EventRegistration.objects.filter(user=user, event=event).first()

        if registration:
            # If the user is already registered, update the status
            registration.status = status1
            registration.save()
            logger.info(f"Registration status updated for user {user.username} for event {event.title} to {status}")
            return Response(EventRegistrationSerializer(registration).data, status=status.HTTP_200_OK)
        else:
            
            logger.info(f"Registration status before registration_data {user.username} for event {event.title} to {status1}")
            # If the user is not registered, create a new registration
            registration_data = {
                'user': user.id,
                'event': event.id,
                'status': status1
            }
            logger.info(f"Registration status after registration_data {user.username} for event {event.title} to {status1}")
            serializer = EventRegistrationSerializer(data=registration_data)
            logger.info(f"Registration status after Serialization {user.username} for event {event.title} to {status1}")
            if serializer.is_valid():
                serializer.save()  # Save the new registration to the database
                logger.info(f"User  successfully registered for event {event.title}")
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                logger.error(f"Registration validation failed: {serializer.errors}")
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            









@api_view(['GET'])
@permission_classes([AllowAny])
def get_approved_events(request):
    """
    API to fetch all approved events.
    Returns a list of events with approval_status='approved'.
    """
    try:
        # Fetch all events with approval_status set to 'approved'
        approved_events = Event.objects.filter(approval_status='approved')
        
        # Serialize the events
        serializer = EventSerializer(approved_events, many=True)
        
        # Return the serialized data
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    except Exception as e:
        # Handle any unexpected errors
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)            