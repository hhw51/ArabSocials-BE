from django.urls import path
from .views import signup,send_otp,verify_otp, login, update_user, get_other_users,get_users_with_same_location, get_users_with_same_Profession, add_favorite
from .views import get_favorite_users

app_name = "users"
urlpatterns = [
    path('signup/', signup, name='signup'),
    path('login/', login, name='login'),
    path('send-otp/', send_otp, name='send_otp'),
    path('verify-otp/', verify_otp, name='verify_otp'),
    path('update-user/', update_user, name='update_user'),
    path('get-other-users/', get_other_users, name='exclude-self'),
    path('same-location/', get_users_with_same_location, name='same-location-users'),
    path('same-profession/', get_users_with_same_Profession, name='same-profession-users'),
    path('favorites/', add_favorite, name='add-favorite'),
    path('get-favorite-users/', get_favorite_users, name='get-favorite-users'),



]
