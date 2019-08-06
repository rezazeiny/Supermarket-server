from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from . import views

urlpatterns = [
    path('menu/search/name/', views.MarketSearchByName.as_view()),
    path('menu/search/address/', views.MarketSearchByAddress.as_view()),
    path('add/', views.MarketAdd.as_view()),
    path('rate/', views.MarketRate.as_view()),
    path('rate/list/', views.MarketShowRates.as_view()),
    path('comment/', views.MarketComment.as_view()),
    path('comment/list/', views.MarketShowComments.as_view()),
    path('detail/', views.MarketShowDetail.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
