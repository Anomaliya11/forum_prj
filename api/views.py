# from django.shortcuts import render
from django.forms import CharField

from rest_framework import viewsets
from api import serializers
from api.models import Checkbox
from api.serializers import CheckboxSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

# class CheckboxViewSet(viewsets.ModelViewSet):
#     queryset = Checkbox.objects.all()
#     serializer_class = CheckboxSerializer

@api_view(['CET'])
def checkbox_list(req):
    checkboxes = Checkbox.objects.all()
    serializer = CheckboxSerializer(checkboxes, many=True)
    return Response(serializer.data)