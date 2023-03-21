from django.db import router
from django.urls import path, include
from rest_framework import routers

from api import views
# from api.views import CheckboxViewSet

# router = routers.DefaultRouter()
# router.register('checkbox', CheckboxViewSet)

urlpatterns = [
    # path('', include(router.urls)),
    path('checkbox_list', views.checkbox_list, name='checkbox_list'),
]