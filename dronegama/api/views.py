from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from providers_details.models import ProvidersDetails

from providers_details.serializers import ProvidersDetailsSerializer


# Create your views here.

@api_view(['GET', 'POST'])
def task_list(request):
  if request.method == 'GET':
    return Response("{'something': 'something'}")

@api_view(['GET', 'POST'])
def providers_details(request):
  if request.method == 'GET':
    details = ProvidersDetails.objects.all()
    serializer = ProvidersDetailsSerializer(details, many=True)
    return Response(serializer.data)
  if request.method == 'POST':
    serializer = ProvidersDetailsSerializer(data=request.DATA)
    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data, status=status.HTTP_201_CREATED)
    else:
      return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
