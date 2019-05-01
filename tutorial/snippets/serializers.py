"""
Django Rest Frameworks serializers for snippets module.
"""

from django.contrib.auth.models import User
from rest_framework import serializers
from snippets.models import Snippet


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for System User.
    """
    snippets = serializers.PrimaryKeyRelatedField(many=True, queryset=Snippet.objects.all())

    class Meta:
        model = User
        fields = ('id', 'username', 'snippets')


class SnippetSerializer(serializers.ModelSerializer):
    """
    Serializer for Snippet model.
    """
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Snippet
        fields = ('id', 'title', 'code', 'linenos', 'language', 'style', 'owner')
