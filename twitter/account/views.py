from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions, status
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from . import models


class RelationAPIView(APIView):
    """
    View to list all users in the system.

    * Requires token authentication.
    * Only admin users are able to access this view.
    """

    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, format=None):
        pass

    def post(self, request, format=None, *args, **kwargs):
        """
        Create a new relation 
        """
        from_user = request.user.id
        to_user = get_object_or_404(User, pk=self.kwargs['to_user_id'])
        if User.objects.filter(from_user=from_user, to_user=to_user).exists():
            return Response(status=status.HTTP_400_BAD_REQUEST)
        models.Relation(from_user=from_user, to_user=to_user)
        return Response(status=status.HTTP_200_OK)
    
    def delete(self, request, format=None, *args, **kwargs):
        """
        Delete a new relation 
        """
        from_user = request.user.id
        to_user = get_object_or_404(User, pk=self.kwargs['to_user_id'])
        relation = User.objects.filter(from_user=from_user, to_user=to_user)
        if relation:
           relation.delete()
           return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)
