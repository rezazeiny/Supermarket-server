from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from . import views
from django.conf import settings


urlpatterns = [
    path('login/username/', views.UserLoginByUsername.as_view()),
    path('login/email/', views.UserLoginByEmail.as_view()),
    path('signup/username', views.UserSignupByUsername.as_view()),
    path('signup/', views.UserSignup.as_view()),
    path('show/profile', views.ShowProfileUsername.as_view()),
    # path('change/profile', views.ChangeProfile.as_view()),
    # path('change/image', views.ChangeImage.as_view()),
    # path('change/password', views.ChangePassword.as_view()),
    # path('change/email', views.ChangeEmail.as_view()),
    # path('change/phone', views.ChangePhone.as_view()),
    # path('forgot/email', views.ForgotPassEmail.as_view()),
    # path('forgot/phone', views.ForgotPassPhone.as_view()),
    # path('forgot/change', views.ForgotPassChange.as_view()),
    # path('validate/send/phone', views.SendValidatePhone.as_view()),
    # path('validate/check/phone', views.CheckValidatePhone.as_view()),
    # path('validate/send/email', views.SendValidateEmail.as_view()),
    # path('validate/check/email', views.CheckValidateEmail.as_view()),
]

if settings.DEBUG:
    urlpatterns += [
        path('list/', views.UserList.as_view()),
        path('detail/<int:pk>/', views.UserDetail.as_view())
    ]


urlpatterns = format_suffix_patterns(urlpatterns)
