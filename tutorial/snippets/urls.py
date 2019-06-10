"""
URL configs for snippets views.
"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from snippets import views

# Create a router and register our viewsets with it.
ROUTER = DefaultRouter()
ROUTER.register(r'snippets', views.SnippetViewSet)
ROUTER.register(r'users', views.UserViewSet)

urlpatterns = [
    path('', include(ROUTER.urls)),
]
