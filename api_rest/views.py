from django.shortcuts import render
from django.http import HttpResponse, JsonResponse

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .models import User
from .serializers import UserSerializer, UserMailSerializer

import json

@api_view(['GET'])
def get_users(request):

  if request.method == 'GET':
    users = User.objects.all()
    serializer = UserSerializer(users, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

  return Response(status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT'])
def get_by_nick(request, nick):

  if request.method == 'GET':
    try:
      user = User.objects.get(pk=nick)
      serializer = UserSerializer(user)
      return Response(serializer.data, status=status.HTTP_200_OK)
    except User.DoesNotExist:
      return Response(status=status.HTTP_404_NOT_FOUND)

  if request.method == 'PUT':
    try:
      user = User.objects.get(pk=nick)
      serializer = UserSerializer(user, data=request.data)

      if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    except User.DoesNotExist:
      return Response(status=status.HTTP_404_NOT_FOUND)

  return Response(status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'POST', 'PUT', 'DELETE'])
def user_manager(request):

  if request.method == 'GET':

    try:

      if request.GET['user']:
        user_nickname = request.GET['user']

        try:
          user = User.objects.get(pk=user_nickname)

        except User.DoesNotExist:
          return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

      else:
        return Response(status=status.HTTP_400_BAD_REQUEST)

    except User.DoesNotExist:
      return Response(status=status.HTTP_404_NOT_FOUND)

  if request.method == 'POST':
    new_user = request.data
    serializer = UserSerializer(data=new_user)

    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data, status=status.HTTP_201_CREATED)

    return Response(status=status.HTTP_400_BAD_REQUEST)

  if request.method == 'PUT':
    nickname = request.data["user_nickname"]

    try:
      updated_user = User.objects.get(pk=nickname)
    except User.DoesNotExist:
      return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = UserSerializer(updated_user, data=request.data)

    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data, status=status.HTTP_200_OK)

    return Response(status=status.HTTP_400_BAD_REQUEST)

  if request.method == 'DELETE':
    try:
      user_to_delete = User.objects.get(pk=request.data["user_nickname"])
      user_to_delete.delete()
      return Response(status=status.HTTP_202_ACCEPTED)
    except User.DoesNotExist:
      return Response(status=status.HTTP_404_NOT_FOUND)

  return Response(status=status.HTTP_400_BAD_REQUEST)
