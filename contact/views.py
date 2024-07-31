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
