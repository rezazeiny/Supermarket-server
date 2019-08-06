from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from . import views

urlpatterns = [
    path('menu/search/name/', views.ModelSearchByName.as_view()),
    path('menu/search/category/', views.ModelSearchByCategory.as_view()),
    path('add/', views.ModelAdd.as_view()),
    path('rate/', views.ModelRate.as_view()),
    path('rate/list/', views.ModelShowRates.as_view()),
    path('comment/', views.ModelComment.as_view()),
    path('comment/list/', views.ModelShowComments.as_view()),
    path('detail/', views.ModelShowDetail.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
