from django.shortcuts import render

from django.forms import CharField

from rest_framework import viewsets
from api.models import Checkbox
from api.serializers import CheckboxSerializer

class CheckboxViewSet(viewsets.ModelViewSet):
    queryset = Checkbox.objects.all()
    serializer_class = CheckboxSerializer
