from django.contrib import admin
from django.urls import path
from spam.views import Register,SearchByName,Contact,SpamUpdation,SearchByNumber,SearchResult,Login


urlpatterns = [
  
  path('register/',Register.as_view(),name='register'),
  path('login/',Login.as_view(),name='login'),
  path('contacts/',Contact.as_view(),name='contacts'),
  path('spams/',SpamUpdation.as_view(),name='spams'),
  path('search_name/',SearchByName.as_view(),name='search_name'),
  path('search_by_number/',SearchByNumber.as_view(),name='search_by_number'),
  path('search_result/',SearchResult.as_view(),name='search_result'),
]

