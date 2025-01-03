from django.urls import path
from .views import create_event,register_event

app_name = "events"
urlpatterns = [
    path('create-event/', create_event, name='create_event'),
    path('register-event/', register_event, name='register_event'),

]
