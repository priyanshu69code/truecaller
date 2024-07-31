from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
import phonenumbers
from django.conf import settings


class Contact(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(blank=True, null=True)
    phone = PhoneNumberField(blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    spam = models.BooleanField(default=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE, default=1)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    def save(self, *args, **kwargs):
        # No need to normalize here as PhoneNumberField takes care of it
        super(Contact, self).save(*args, **kwargs)

    def mark_spam(self):
        self.spam = True
        self.save()

    def mark_not_spam(self):
        self.spam = False
        self.save()

    def is_spam(self):
        return self.spam

    def spam_likelihood(self):
        normalized_phone = str(self.phone)
        total_count = Contact.objects.filter(phone=normalized_phone).count()
        spam_count = Contact.objects.filter(
            phone=normalized_phone, spam=True).count()
        return spam_count / total_count if total_count > 0 else 0

    def get_country(self):
        parsed_phone = phonenumbers.parse(str(self.phone))
        print(parsed_phone)
        return parsed_phone.country_code

    def get_phone_number(self):
        parsed_phone = phonenumbers.parse(self.phone)
        print(parsed_phone)
        return parsed_phone.national_number
