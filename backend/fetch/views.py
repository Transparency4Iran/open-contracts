from django.shortcuts import render
from .models import Page, Attempt, Detail
from rest_framework import generics
from .serilazers import AttemptSerializer


class AttemptList(generics.ListAPIView):
    queryset = Attempt.objects.order_by('-date')
    serializer_class = AttemptSerializer


def raw(request, id):
    page = Page.objects.get(id=id)
    # print(page.content)
    return render(request, 'raw.html', {'page': page})


def raw_detail(request, id):
    page = Detail.objects.get(id=id)
    # print(page.content)
    return render(request, 'raw_details.html', {'page': page})


def force_check(request):
    Attempt.new_attempt()


def force_fetch_detail_pages(request):
    from .lib import fetch_remaining_detail_pages
    fetch_remaining_detail_pages()
    # content = page.content.replace("&#13;", "")
    # import re
    # content = re.sub('\s+', ' ', content).strip()
    # values = tree.findall('.//div[@class="row"]/div[1]/span[2]')
