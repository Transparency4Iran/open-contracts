from django.db import models
from datetime import timedelta


class Attempt(models.Model):
    date = models.DateTimeField(auto_now_add=True)
    all_count = models.IntegerField()
    with_errors_count = models.IntegerField(default=0)

    @staticmethod
    def new_attempt():
        import requests
        from lxml import html, etree
        from fetch import lib
        session = requests.session()
        resp = session.get('https://cdb.mporg.ir/', headers={
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/601.3.9 (KHTML, like Gecko) Version/9.0.2 Safari/601.3.9'},
                           verify=False)
        tree = html.fromstring(resp.text)
        all_count = int(tree.find('.//span[@id="lblTotal"]').text)
        max_count = Page.objects.order_by('-end').first().end
        attempt = Attempt.objects.create(all_count=all_count)
        if all_count > max_count:
            remaining_pages = ((all_count - max_count - 1) // 5) + 1
            # print(remaining_pages)
            list_pages = []
            for i in range(0, remaining_pages):
                container = html.fromstring(resp.text).find('.//td[@id="tdServer"]')
                content = etree.tostring(container, encoding='UTF-8')
                # print(content)
                end = all_count - (i * 5)
                start = end - 4
                list_pages.append({
                    'content': content,
                    'start': start,
                    'end': end
                })
                resp = lib.next(resp, session=session)
            for p in list_pages:
                Page.objects.create(attempt=attempt, **p)

        return session

    def __str__(self):
        return str(self.date)

    def yesterday(self):
        return (self.date - timedelta(days=1)).date()

    def new_count(self):
        previous = Attempt.objects.filter(date__lt=self.date).order_by('date').last()
        if previous:
            previous_count = previous.all_count
        else:
            previous_count = 0
        return self.all_count - previous_count


class Page(models.Model):
    attempt = models.ForeignKey(Attempt, related_name="pages")
    content = models.TextField()
    start = models.IntegerField()
    end = models.IntegerField()

    def __str__(self):
        return str(self.start) + "-" + str(self.end)


class Detail(models.Model):
    order_num = models.IntegerField()
    fetch_date = models.DateTimeField(auto_now_add=True)
    url_code = models.CharField(max_length=32)
    content = models.TextField()

    def __str__(self):
        return self.url_code + "-" + str(self.order_num)

    def page(self):
        return Page.objects.filter(start__lte=self.order_num).filter(
            end__gte=self.order_num).first()
