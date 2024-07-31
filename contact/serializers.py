from phonenumber_field.serializerfields import PhoneNumberField
from .models import Contact
from rest_framework import serializers


class ContactSerializer(serializers.ModelSerializer):
    phone = PhoneNumberField()

    class Meta:
        model = Contact
        fields = ['phone', 'email', 'first_name', 'last_name', 'spam']
        extra_kwargs = {
            'email': {'required': False, },
            'first_name': {'required': True},
            'last_name': {'required': True},
            "spam": {"read_only": True}
        }

    def create(self, validated_data):
        contact = Contact.objects.create(
            phone=validated_data.get('phone', None),
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            user=self.context['request'].user
        )
        return contact


class ListContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = '__all__'


class MarkSpamContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = ['spam']
        extra_kwargs = {
            'spam': {'required': True}
        }
