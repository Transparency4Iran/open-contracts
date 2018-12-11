from django.core.management.base import BaseCommand, CommandError
from location.models import City,Town


class Command(BaseCommand):
    args = '<from_date offset ...>'
    help = 'Fetches the CrossRef metadata'

    # see https://github.com/CrossRef/rest-api-doc/blob/master/rest_api.md

    def __init__(self, *args, **kwargs):
        super(Command, self).__init__(*args, **kwargs)

    def handle(self, *args, **options):
        for town in Town.objects.all():
                    town.geocode()
        for city in City.objects.all():
            city.geocode()

