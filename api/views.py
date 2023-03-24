# from django.shortcuts import render
from django.forms import CharField

from rest_framework import viewsets
from api import serializers
from api.models import Checkbox
from api.serializers import CheckboxSerializer, DataSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from django.contrib.auth.models import User
from rest_framework import authentication, permissions
from rest_framework import generics, mixins
from api.utils import Sum

class CheckboxViewSet(viewsets.ModelViewSet):
    queryset = Checkbox.objects.all()
    serializer_class = CheckboxSerializer

class CheckboxList(generics.ListCreateAPIView):
    queryset = Checkbox.objects.all()
    serializer_class = CheckboxSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
        
    def post(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


    # def get(self, req, format=None):
    #     checkboxes = Checkbox.objects.all()
    #     serializer = CheckboxSerializer(checkboxes, many=True)
    #     return Response(serializer.data)

    # def post(self, req, format=None):
    #     serializer = CheckboxSerializer(data=req.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #     return Response(serializer.data, status=status.HTTP_201_CREATED)

class CheckboxDetailed(APIView):

    permission_classes = [permissions.IsAdminUser]

    def delete(self, req, pk, format=None):
        checkbox = Checkbox.objects.get(id=pk)
        checkbox.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    
class DataView(APIView):

    @staticmethod
    def get(req):
        serializer = DataSerializer(data=req.query_params)
        serializer.is_valid(raise_exception=True)
        result = Sum(serializer.validated_data).call()
        return Response(result, status=status.HTTP_200_OK)

@api_view(['GET'])
def checkbox_list(req):
    checkboxes = Checkbox.objects.all()
    serializer = CheckboxSerializer(checkboxes, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def checkbox_detail(req, pk):
    try:
        checkbox = Checkbox.objects.get(id=pk)
        serializer = CheckboxSerializer(checkbox)
    except Checkbox.DoesNotExist:
        return Response((f"error: Checkbox with id = {pk} is not found"), status = status.HTTP_404_NOT_FOUND)
    return Response(serializer.data)

@api_view(['POST'])
def checkbox_create(req):
    serializer = CheckboxSerializer(data=req.data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data, status=status.HTTP_201_CREATED)

@api_view(['PUT'])
def checkbox_update(req, pk):
    try:
        checkbox = Checkbox.objects.get(id=pk)
        serializer = CheckboxSerializer(checkbox, data=req.data)
        if serializer.is_valid():
            serializer.save()
    except Checkbox.DoesNotExist:
        return Response((f"error: Checkbox with id = {pk} is not found"), status = status.HTTP_404_NOT_FOUND)
    return Response(serializer.data)

@api_view(['DELETE'])
def checkbox_delete(req, pk):
    checkbox = Checkbox.objects.get(id=pk)
    checkbox.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)
