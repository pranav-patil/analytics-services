from users.views import UserList, UserDetails, GroupList, UserSignUp
from django.urls import path, include

app_name = 'users'

urlpatterns = [
    path('signup/', UserSignUp.as_view()),
    path('users/', UserList.as_view()),
    path('users/<pk>/', UserDetails.as_view()),
    path('groups/', GroupList.as_view())
]
