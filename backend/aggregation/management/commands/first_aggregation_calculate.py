from django.core.management.base import BaseCommand, CommandError
from main.models import Contract
from org.models import Organization, People
from fetch.models import Attempt
from aggregation.models import ErrorSpectrum, DailyFetchPerTopOrganization


class Command(BaseCommand):
    args = '<from_date offset ...>'
    help = 'Fetches the CrossRef metadata'

    # see https://github.com/CrossRef/rest-api-doc/blob/master/rest_api.md

    def __init__(self, *args, **kwargs):
        super(Command, self).__init__(*args, **kwargs)

    def handle(self, *args, **options):
        ErrorSpectrum.objects.all().delete()
        DailyFetchPerTopOrganization.objects.all().delete()
        Organization.objects.all().update(contracts_count=0, errors_count=0)
        People.objects.all().update(contracts_count=0, errors_count=0)
        for contract in Contract.objects.all():
            contract.update_aggregations()
