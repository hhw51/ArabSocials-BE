from django.urls import path
from .views import signup,send_otp

app_name = "users"
urlpatterns = [
    path('signup/', signup, name='signup'),
    path('send-otp/', send_otp, name='send_otp'),
]
