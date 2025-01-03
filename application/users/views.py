
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
import random
import time
import hashlib
from django.core.cache import cache
from django.core.mail import send_mail
from django.conf import settings
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from .serializers import EmailSerializer  # Assuming you have an EmailSerializer
from django.views.decorators.csrf import csrf_exempt
from .models import User
from .serializers import UserSerializer


@csrf_exempt
@api_view(['POST'])
@permission_classes([AllowAny])
def signup(request):
    """
    A function-based view to handle user signup, with validation for unique email and phone number.
    It also gracefully handles missing fields in the request.
    """
    if request.method == 'POST':
        # Extract the data from the request
        data = request.data
        
        # Set default values for optional fields if they are missing
        data['phone'] = data.get('phone', None)
        data['location'] = data.get('location', None)
        data['marital_status'] = data.get('marital_status', None)
        data['interests'] = data.get('interests', None)
        data['profession'] = data.get('profession', None)
        data['social_links'] = data.get('social_links', None)

        # Check if email or phone number is already taken
        email = data.get('email')
        phone = data.get('phone')

        # Validate unique email
        if User.objects.filter(email=email).exists():
            return Response({'error': 'Email is already taken.'}, status=status.HTTP_400_BAD_REQUEST)

        # Validate unique phone number
        if phone and User.objects.filter(phone=phone).exists():
            return Response({'error': 'Phone number is already taken.'}, status=status.HTTP_400_BAD_REQUEST)

        # Serialize the data
        serializer = UserSerializer(data=data)
        
        if serializer.is_valid():
            # Save the new user and hash the password
            user=serializer.save()
            token, created = Token.objects.get_or_create(user=user)
            return Response({
                'user': serializer.data,
                'token': token.key
            }, status=status.HTTP_201_CREATED)
        else:
            # Return validation errors
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)







@csrf_exempt
@api_view(['POST'])
@permission_classes([AllowAny])
def send_otp(request):
   
    serializer = EmailSerializer(data=request.data)
    if serializer.is_valid():
        email = serializer.validated_data['email']
        
        # Check if the user exists
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({"detail": "User does not exist"}, status=status.HTTP_404_NOT_FOUND)

        # Rate-limit OTP requests
        last_request = cache.get(f"otp_{email}_last_request")
        if last_request and time.time() - last_request < 60:  # 60 seconds cooldown
            return Response({"detail": "Please wait before requesting a new OTP"}, status=429)
        
        # Generate OTP
        otp = random.randint(100000, 999999)
        hashed_otp = hashlib.sha256(str(otp).encode()).hexdigest()
        cache.set(f"otp_{email}", hashed_otp, timeout=300)
        cache.set(f"otp_{email}_last_request", time.time())

        # Email configuration
        smtp_server = "smtp.gmail.com"
        smtp_port = 587
        smtp_user = "loopsniper786@gmail.com"
        smtp_password = "dlly wymr rjbd cjbe"

        subject = "Your OTP Code"
        message = f"""
Hello,

Your OTP code for login is: {otp}

This code is valid for 5 minutes. Please do not share it with anyone.

Best regards,
Your App Team
"""

        # Set up the MIME
        msg = MIMEMultipart()
        msg['From'] = smtp_user
        msg['To'] = email
        msg['Subject'] = subject
        msg.attach(MIMEText(message, 'plain'))

        # Send email using smtplib
        try:
            server = smtplib.SMTP(smtp_server, smtp_port)
            server.starttls()
            server.login(smtp_user, smtp_password)
            server.sendmail(smtp_user, email, msg.as_string())
            server.quit()
            print("Email sent successfully!")
        except Exception as e:
            print(f"Failed to send email: {e}")
            return Response({"detail": "Failed to send email"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response({"detail": "OTP sent successfully"}, status=status.HTTP_200_OK)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)







@csrf_exempt
@api_view(['POST'])
@permission_classes([AllowAny])
def verify_otp(request):
    email = request.data.get('email')
    otp = request.data.get('otp')

    # Check if email and OTP are provided
    if not email or not otp:
        return Response({"detail": "Email and OTP are required"}, status=status.HTTP_400_BAD_REQUEST)

    try:
        # Check if the user exists
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        return Response({"detail": "User does not exist"}, status=status.HTTP_404_NOT_FOUND)

    # Retrieve the hashed OTP from cache
    cached_otp = cache.get(f"otp_{email}")
    if not cached_otp:
        return Response({"detail": "OTP has expired or is invalid"}, status=status.HTTP_400_BAD_REQUEST)

    # Hash the user-provided OTP and compare it to the cached OTP
    hashed_provided_otp = hashlib.sha256(str(otp).encode()).hexdigest()
    if hashed_provided_otp != cached_otp:
        return Response({"detail": "Invalid OTP"}, status=status.HTTP_400_BAD_REQUEST)

    # OTP is valid, delete it from cache to prevent reuse
    cache.delete(f"otp_{email}")

    # Generate a token for the user
    token, created = Token.objects.get_or_create(user=user)

    # Return success response with token
    return Response({
        "detail": "Authentication successful",
        "token": token.key
    }, status=status.HTTP_200_OK)























