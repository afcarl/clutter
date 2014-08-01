from django.core.management.base import BaseCommand
from os.path import isfile, join
from clutter.models import Item, Node
from os import listdir

class Command(BaseCommand):
    help = 'imports the images in the images folder'

    def handle(self, *args, **options):
        Item.objects.all().delete()
        Node.objects.all().delete()

        images_path = 'images'
        onlyfiles = [f for f in listdir(images_path) if isfile(join(images_path, f))]

        for f in onlyfiles:
            item = Item(image=join(images_path, f))
            item.save()
            print(join(images_path, f))
