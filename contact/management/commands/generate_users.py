import random
from faker import Faker
from django.core.management.base import BaseCommand
from django.utils.crypto import get_random_string
from user.models import User  # Adjust the import based on your app structure


def get_random_phonenumber(length=10):
    number = "+91"
    for _ in range(length):
        number += str(random.randint(0, 9))
    return number


class Command(BaseCommand):
    help = 'Generate random users'

    def add_arguments(self, parser):
        parser.add_argument('count', type=int,
                            help='Indicates the number of users to be created')

    def handle(self, *args, **kwargs):
        count = kwargs['count']
        fake = Faker()

        for _ in range(count):
            first_name = fake.first_name()
            last_name = fake.last_name()
            number = get_random_phonenumber()
            email = fake.email()
            password = get_random_string(8)
            is_active = fake.boolean()
            is_staff = fake.boolean()
            is_verified = fake.boolean()

            user = User(
                first_name=first_name,
                last_name=last_name,
                number=number,
                email=email,
                is_active=is_active,
                is_staff=is_staff,
                is_verified=is_verified,
            )
            user.set_password(password)
            user.save()

        self.stdout.write(self.style.SUCCESS(
            f'Successfully created {count} users'))
