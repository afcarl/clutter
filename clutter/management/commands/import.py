from django.core.management.base import BaseCommand
from clutter.models import Item, Node

class Command(BaseCommand):
    help = 'import contents of data.txt file'

    def handle(self, *args, **options):
        Item.objects.all().delete()
        Node.objects.all().delete()

        with open('data.txt') as f:
            for row in f:
                if row.strip() == "":
                    continue
                item = Item(content=row.strip())
                item.save()
                print(item)
