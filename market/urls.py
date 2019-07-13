from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from . import views

urlpatterns = [
    path('list/', views.MarketList.as_view()),
    path('add/', views.MarketAdd.as_view()),
    path('full_add/', views.MarketFullAdd.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
