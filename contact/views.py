from .serializers import ContactDocumentSerializer
from .documents import ContactDocument
from django_elasticsearch_dsl_drf.filter_backends import (
    FilteringFilterBackend,
    OrderingFilterBackend,
    DefaultOrderingFilterBackend,
    SearchFilterBackend
)
from django_elasticsearch_dsl_drf.viewsets import DocumentViewSet
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_403_FORBIDDEN
from .models import Contact
from rest_framework import generics, permissions
from .serializers import ContactSerializer, ListContactSerializer, MarkSpamContactSerializer


# Create your views here.


class AddContactView(generics.CreateAPIView):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer
    permission_classes = []


class ContactListView(generics.ListAPIView):
    serializer_class = ListContactSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        print(Contact.objects.filter(user=self.request.user))
        return Contact.objects.filter(user=self.request.user)


class UpdateContactView(generics.UpdateAPIView):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Contact.objects.filter(user=self.request.user)


class DeleteContactView(generics.DestroyAPIView):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Contact.objects.filter(user=self.request.user)


class MarkSpamContactView(generics.UpdateAPIView):
    queryset = Contact.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = MarkSpamContactSerializer

    def get_queryset(self):
        return Contact.objects.filter(user=self.request.user)


class DetailContactView(generics.RetrieveAPIView):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Contact.objects.filter(user=self.request.user)


# views.py


class ContactDocumentViewSet(DocumentViewSet):
    document = ContactDocument
    serializer_class = ContactDocumentSerializer
    lookup_field = 'id'
    filter_backends = [
        FilteringFilterBackend,
        OrderingFilterBackend,
        DefaultOrderingFilterBackend,
        SearchFilterBackend,
    ]
    search_fields = (
        'first_name',
        'last_name',
        'email',
        'phone',
    )
    filter_fields = {
        'first_name': 'first_name.keyword',
        'last_name': 'last_name.keyword',
        'email': 'email',
        'phone': 'phone',
    }
    ordering_fields = {
        'first_name': 'first_name.keyword',
        'last_name': 'last_name.keyword',
        'email': 'email',
        'phone': 'phone',
    }
    ordering = ('first_name.keyword', 'last_name.keyword',)
