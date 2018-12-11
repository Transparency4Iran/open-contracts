from django.core.management.base import BaseCommand, CommandError
from fetch.models import Attempt
from fetch.lib import fetch_remaining_detail_pages
from main.lib import read_remaining,export,warm_cache
from omid_utils.sitemap import notify_sitemap_to_google

class Command(BaseCommand):
    args = '<from_date offset ...>'
    help = 'Fetches the CrossRef metadata'

    # see https://github.com/CrossRef/rest-api-doc/blob/master/rest_api.md

    def __init__(self, *args, **kwargs):
        super(Command, self).__init__(*args, **kwargs)

    def handle(self, *args, **options):
        session = Attempt.new_attempt()
        fetch_remaining_detail_pages(session=session)
        read_remaining()
        export()
        warm_cache()
        notify_sitemap_to_google()
