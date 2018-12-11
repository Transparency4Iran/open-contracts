from django.core.management.base import BaseCommand, CommandError
from fetch.models import Attempt, Page
from fetch import lib
import requests
from lxml import html, etree


class Command(BaseCommand):
    args = '<from_date offset ...>'
    help = 'Fetches the CrossRef metadata'

    # see https://github.com/CrossRef/rest-api-doc/blob/master/rest_api.md

    def __init__(self, *args, **kwargs):
        super(Command, self).__init__(*args, **kwargs)

    def handle(self, *args, **options):
        Attempt.objects.all().delete()

        first_page = requests.get('https://cdb.mporg.ir/', headers={
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/601.3.9 (KHTML, like Gecko) Version/9.0.2 Safari/601.3.9'},verify=False)
        tree = html.fromstring(first_page.text)
        all_count = int(tree.find('.//span[@id="lblTotal"]').text)
        attempt = Attempt.objects.create(all_count=all_count)
        start = 1
        end = ((all_count - 1) % 5) + 1
        last = lib.last(first_page)
        while True:
            container = html.fromstring(last.text).find('.//td[@id="tdServer"]')
            content = etree.tostring(container, encoding='UTF-8')
            # print(content)
            Page.objects.create(content=content, start=start, end=end, attempt=attempt)
            last = lib.previous(last)
            start = end + 1
            end = end + 5
