from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

urlpatterns = [
    path('list/', views.UserList.as_view()),
    path('login/username/', views.UserLoginByUsername.as_view()),
    path('login/email/', views.UserLoginByEmail.as_view()),
    path('signup/', views.UserSignupByUsername.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
