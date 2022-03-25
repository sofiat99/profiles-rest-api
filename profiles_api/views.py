# from dataclasses import dataclasses
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets
# no deja put patch delete
from rest_framework.authentication import TokenAuthentication
from rest_framework import filters

from profiles_api import serializers
from profiles_api import models
from profiles_api import permissions


class HelloApiView(APIView):
    """Test API VIEW"""
    serializer_class = serializers.HelloSerializer

    def get(self, request, format=None):
        """Return a list of APIView features"""
        an_apiview = [
            'Uses HTTP methods as function (get,post,patch,put,delete)',
            'Is similar to a traditional Django view',
            'Gives you the most control over you application logic',
            'Is mapped manually to URLs',
        ]

        return Response({'message': 'Hello!', 'an_apiview': an_apiview})

    def post(self, request):
        """create a hello message with our name"""
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            name = serializer.validated_data.get('name')
            message = f'hello {name}'
            return Response({"message": message})
        else:
            return Response(serializer.errors,
                            # porque daría 200 status entonces lo cambio con status
                            status=status.HTTP_400_BAD_REQUEST
                            )

    def put(self, request, pk=None):
        """Handle update object"""
        return Response({"method": "PUT"})

    def patch(self, request, pk=None):
        """Handle a partial update object, only update the fields provider in the request"""
        return Response({"method": "patch"})

    def delete(self, request, pk=None):
        """Delete an object"""
        return Response({'method': 'DELETE'})


class HelloViewSet(viewsets.ViewSet):
    """Test API ViewSet"""
    serializer_class = serializers.HelloSerializer  # importar validación del name

    def list(self, request):
        """Return a hello message"""
        a_viewset = [
            'Uses actions (list,create, retrieve, update, partial_update)',
            'Automatially maps to URLs using Routers',
            'Provides more functionality with less code',
        ]
        return Response({'message': 'Hello!', 'a_viewset': a_viewset})

    def create(self, request):
        """Create a new hello message"""
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            name = serializer.validated_data.get('name')
            message = f'Hello {name}!'
            return Response({'message': message})
        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

    def retrieve(self, request, pk=None):
        http_method_names = ['get', 'head']
        """Handle getting an object by its ID"""
        return Response({'http_method': 'GET'})

    def update(self, request, pk=None):
        """Handle updating an object"""
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            return Response({'http_method': 'PUT'})
        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

    def partial_update(self, request, pk=None):
        """Handle updating part of an object"""
        return Response({'http_method': 'PATCH'})

    def destroy(self, request, pk=None):
        """Handle removing an object"""
        return Response({'http_method': 'DELETE'})


class UserProfileViewSet(viewsets.ModelViewSet):
    """Handle creating and updating profiles"""
    serializer_class = serializers.UserProfileSerializer
    # debido a esto no pongo base name en url
    queryset = models.UserProfile.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.UpdateOwnProfile,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name', 'email',) #puedo filtrar por name or email en url es ?search=Nombre
