from django.core.management.base import BaseCommand
from accounts.models import Account


class Command(BaseCommand):

    def handle(self, *args, **options):
        if not Account.objects.filter(username="admin-martin").exists():
            Account.objects.create_superuser('Martin', 'Serret', 'martin.serret47@gmail.com', 'admin-martin', 'martin10031992')