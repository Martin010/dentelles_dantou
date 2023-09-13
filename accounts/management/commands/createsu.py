from django.core.management.base import BaseCommand
from accounts.models import Account


class Command(BaseCommand):

    def handle(self, *args, **options):
        if not Account.objects.filter(is_superadmin=True).exists():
            Account.objects.create_superuser('Admin First Name', 'Admin Last Name', 'Admin Username', 'adminemail@gmail.com', 'adminpassword')