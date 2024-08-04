import random
from faker import Faker
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
# Adjust the import based on your app structure
from contact.models import Contact
from phonenumber_field.serializerfields import to_python


def get_random_phonenumber(length=10):
    number = "+91"
    for _ in range(length):
        number += str(random.randint(0, 9))
    return number


class Command(BaseCommand):
    help = 'Generate random contacts'

    def add_arguments(self, parser):
        parser.add_argument(
            'count', type=int, help='Indicates the number of contacts to be created')

    def handle(self, *args, **kwargs):
        count = kwargs['count']
        fake = Faker()
        User = get_user_model()
        users = list(User.objects.all())

        if not users:
            self.stdout.write(self.style.ERROR(
                'No users found in the database.'))
            return

        for _ in range(count):
            first_name = fake.first_name()
            last_name = fake.last_name()
            email = fake.email()
            phone = get_random_phonenumber()
            user = random.choice(users)
            spam = fake.boolean()

            phone_number_instance = to_python(phone)
            if not phone_number_instance.is_valid():
                print(f'Invalid phone number: {phone_number_instance}')
                continue
            phone = phone_number_instance.as_e164
            print(phone)

            Contact.objects.create(
                first_name=first_name,
                last_name=last_name,
                email=email,
                phone=phone,
                user=user,
                spam=spam,
            )

        self.stdout.write(self.style.SUCCESS(
            f'Successfully created {count} contacts'))
