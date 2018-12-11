from django.core.management.base import BaseCommand, CommandError
from fetch.models import Page
from main.models import Contract


class Command(BaseCommand):
    args = '<from_date offset ...>'
    help = 'Fetches the CrossRef metadata'

    # see https://github.com/CrossRef/rest-api-doc/blob/master/rest_api.md

    def __init__(self, *args, **kwargs):
        super(Command, self).__init__(*args, **kwargs)

    def handle(self, *args, **options):
        for contract in Contract.objects.filter(fetch_date__isnull=True):
            page = Page.objects.filter(start__lte=contract.detail_page.order_num).filter(
                end__gte=contract.detail_page.order_num).first()
            if page:
                contract.fetch_date = page.attempt.yesterday()
                contract.save()
