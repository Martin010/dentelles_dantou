from django.core.management.base import BaseCommand
from accounts.models import Account


class Command(BaseCommand):

    def handle(self, *args, **options):
        if not Account.objects.filter(username="admin-martin").exists():
            Account.objects.create_superuser('Martin', 'Serret', 'admin-martin', 'martin.serret47@gmail.com', 'martin10031992')