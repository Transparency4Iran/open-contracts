# -*- coding: utf-8 -*-
import requests
from lxml import html, etree


def change(current, where, session=None):
    if not session:
        session = requests.session()
    while True:
        try:
            tree = html.fromstring(current.text)
            # info = tree.find('.//td[@id="tdServer"]')
            # rows = tree.findall('.//div[@class="row"]')
            form1 = tree.find('.//form[@id="form1"]')
            data = dict(form1.form_values())
            del data['Button2']
            data["hsco"] = ""
            data["hsub"] = ""
            data["hdiv"] = ""
            data["hcln"] = ""
            data["__ASYNCPOST	"] = True
            data['ScriptManager1'] = 'pnlData1|' + where
            data['__EVENTTARGET'] = where
            new_page = session.post('https://cdb.mporg.ir/', data=data,verify=False)
            # print(new_page.text)
            if new_page.status_code == 200:
                return new_page
        except:
            print('fail')


def previous(current, session=None):
    return change(current, 'lbPrevious', session=session)


def last(current, session=None):
    return change(current, 'lbLast', session=session)


def first(current, session=None):
    return change(current, 'lbFirst', session=session)


def next(current, session=None):
    return change(current, 'lbNext', session=session)


def fetch_detail_page(link, session):
    for i in range(0, 10):
        try:
            detail_page = session.get('https://cdb.mporg.ir/' + link,verify=False)
            if detail_page.status_code == 200:
                container = html.fromstring(detail_page.text).find('.//div[@class="content1"]')
                return etree.tostring(container, encoding='UTF-8')
        except:
            print('failed')
    return None


def fetch_remaining_detail_pages(session=None):
    if not session:
        session = requests.session()
        temp = session.get('https://cdb.mporg.ir/',verify=False)
    from .models import Detail, Page
    last_fetched = Detail.objects.order_by('-order_num').first()
    if last_fetched:
        head = last_fetched.order_num + 1
    else:
        head = 1
    max_page_end = Page.objects.order_by('-end').first().end
    current_page = None
    while head <= max_page_end:
        if not current_page or current_page.end < head:
            current_page = Page.objects.filter(start__lte=head).filter(end__gte=head).first()
            tree = html.fromstring(current_page.content)
            links = tree.findall('.//a[@target="CDBHomePage"]')
        index = head - current_page.start
        link = links[index].attrib['href']
        url_code = link.split('ctrId=')[1]
        if not Detail.objects.filter(url_code=url_code).exists():
            content = fetch_detail_page(link, session)
            if content:
                Detail.objects.create(url_code=url_code, content=content, order_num=head)
            else:
                print('error on fetching detail pages and break')
                break
        head += 1
