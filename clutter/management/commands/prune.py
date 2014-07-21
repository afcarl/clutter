from django.core.management.base import BaseCommand
from clutter.models import Node

class Command(BaseCommand):
    help = 'Prune idea tree to preset depth'

    def handle(self, *args, **options):
        for n in Node.objects.filter(parent__isnull=True):
            n.prune()
