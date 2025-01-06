from django.urls import path
from .views import signup,send_otp,verify_otp, login, update_user

app_name = "users"
urlpatterns = [
    path('signup/', signup, name='signup'),
    path('login/', login, name='login'),
    path('send-otp/', send_otp, name='send_otp'),
    path('verify-otp/', verify_otp, name='verify_otp'),
    path('update-user/', update_user, name='update_user'),

]
