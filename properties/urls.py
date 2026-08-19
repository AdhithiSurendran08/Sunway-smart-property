from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('find/', views.finder, name='finder'),
    path('explore/', views.explore, name='explore'),
    path('property/<int:property_id>/', views.property_detail, name='property_detail'),
    path('sustainability/', views.sustainability, name='sustainability'),
    path('assistant/', views.assistant, name='assistant'),
    path('api/assistant-query/', views.assistant_query, name='assistant_query'),
]
