from django.urls import path

from testapp.views import index

urlpatterns = [
    path('', index, name='index'),
]
