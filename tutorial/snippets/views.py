"""
Rest views for snippets module.
"""

from django.contrib.auth.models import User
from rest_framework import permissions
from rest_framework import renderers
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from snippets.permissions import IsOwnerOrReadOnly
from snippets.models import Snippet
from snippets.serializers import SnippetSerializer
from snippets.serializers import UserSerializer


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """
    This viewset automatically provides 'list' and 'detail' actions.

    list:
    Returns a list of all **active** users in the system.

    For more details on how users are activated please [see here][ref].

    [ref]: http://example.com/activating-accounts
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer


class SnippetViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides 'list' 'create', 'retrieve', 'update'
    and 'destroy' actions.

    Additionally we also provide an extra 'highlight' action

    list:
    Return a list of all existing snippets.

    create:
    Create a new snippet from params.

    read:
    Return a snippet given its id.

    update:
    Update a snippet completely.

    partial_update:
    Update a snippet partialy.

    delete:
    Delete a snippet given its id.

    highlight:
    Show highlighted representation of code snippet.
    """
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly)

    @action(detail=True, renderer_classes=[renderers.StaticHTMLRenderer])
    def highlight(self, request, *args, **kwargs):
        """
        Retrieve a snippet highlight
        """
        snippet = self.get_object()
        return Response(snippet.highlighted)

    def perform_create(self, serializer):
        """
        Create a new snippet setting the owner
        """
        serializer.save(owner=self.request.user)
