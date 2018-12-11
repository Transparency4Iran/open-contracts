from .models import Contract, GeneralRule, Category, CreditSource
from lxml import html
from omid_utils.standard import standard_persian
from omid_utils.jalali import Persian, Gregorian
from omid_utils.date import get_end_date
import re
from datetime import datetime


def read_remaining():
    from fetch.models import Page, Detail
    from org.lib import get_or_create_organizations
    from location.lib import get_or_create_location
    from org.models import Executor, People, Synonym
    max_contract = Contract.objects.order_by('-detail_page__order_num').first()
    if max_contract:
        head = max_contract.detail_page.order_num + 1
    else:
        head = 1
    current_page = None
    while head <= Detail.objects.order_by('-order_num').first().order_num:
        detail_page = Detail.objects.filter(order_num=head).first()
        if detail_page:
            if not current_page or current_page.end < head:
                current_page = Page.objects.filter(start__lte=head).filter(end__gte=head).first()
                tree = html.fromstring(current_page.content.replace("&#13;", ""))
                spans = tree.findall('.//div[@class="row"]/div[1]/span[2]')
            errors = 0
            detail_page_tree = html.fromstring(detail_page.content)
            index = head - current_page.start
            title = standard_persian(detail_page_tree.find('.//span[@id="LblCntrSubject"]').text)
            general_rule = GeneralRule.objects.get_or_create(title=standard_persian(spans[index * 10 + 1].text))[0]
            category = Category.objects.get_or_create(title=standard_persian(spans[index * 10 + 2].text))[0]
            credit_source = CreditSource.objects.get_or_create(title=standard_persian(spans[index * 10 + 3].text))[0]
            top_org, bottom_org = get_or_create_organizations(detail_page_tree.find('.//span[@id="LblName"]').text)
            jalali_date_string = detail_page_tree.find('.//span[@id="LblAgreDate"]').text.strip()
            date = Persian(jalali_date_string).gregorian_datetime()
            if date > datetime.now().date():
                errors = errors | Contract.errors.future_date
            jalali_sp = jalali_date_string.split('/')
            jalali_year = int(jalali_sp[0])
            jalali_month = int(jalali_sp[1])
            jalali_day = int(jalali_sp[2])
            try:
                price = int(re.sub('[^0-9]', '', detail_page_tree.find('.//span[@id="lblAgreAmountRiali"]').text))
            except:
                price = None
                errors = errors | Contract.errors.no_price
            city = get_or_create_location(detail_page_tree.find('.//span[@id="LblProvince"]').text,
                                          detail_page_tree.find('.//span[@id="LblTown"]').text,
                                          detail_page_tree.find('.//span[@id="LblCity"]').text)
            if not city:
                errors = errors | Contract.errors.no_location
            exe_name = standard_persian(spans[index * 10 + 8].text)
            if exe_name:
                syn = Synonym.objects.filter(name=exe_name).filter(executor__isnull=False).first()
                if syn:
                    executor = syn.executor
                else:
                    executor = Executor.objects.get_or_create(name=exe_name)[0]
            else:
                executor = None
                errors = errors | Contract.errors.no_executor
            code = spans[index * 10 + 9].text.strip()
            try:
                contract_number = detail_page_tree.find('.//span[@id="LblCntrNo"]').text.strip()
            except:
                contract_number = None
            duration_year = detail_page_tree.find('.//span[@id="LblCntrDurationYear"]').text
            duration_month = detail_page_tree.find('.//span[@id="LblCntrDurationMonth"]').text
            duration_day = detail_page_tree.find('.//span[@id="LblCntrDurationDay"]').text
            end_date = get_end_date(date, duration_year, duration_month, duration_day)
            if not end_date:
                errors = errors | Contract.errors.no_end_date
            else:
                try:
                    if int(duration_year) > 75 or duration_month == 0 or duration_day == 0:
                        errors = errors | Contract.errors.bad_end_date
                except:
                    errors = errors | Contract.errors.bad_end_date
                if end_date < date:
                    errors = errors | Contract.errors.negative_duration
            registrar = People.objects.get_or_create(
                name=standard_persian(detail_page_tree.find('.//span[@id="lblUserName"]').text))[0]
            Contract.objects.get_or_create(detail_page=detail_page, title=title, organization=bottom_org,
                                           top_organization=top_org, executor=executor, city=city, contract_date=date,
                                           jalali_year=jalali_year, jalali_month=jalali_month, jalali_day=jalali_day,
                                           price=price, code=code, contract_number=contract_number,
                                           end_date=end_date, registrar=registrar, general_rule=general_rule,
                                           category=category, credit_source=credit_source,
                                           fetch_date=current_page.attempt.yesterday(), defaults={'errors': errors})
        head += 1


def export(queryset=Contract.objects.all()):
    import pandas, collections
    contracts_to_export = []
    for contract in queryset:
        obj = collections.OrderedDict()
        obj['ردیف'] = contract.id
        obj['کد قرارداد'] = contract.code
        obj['عنوان'] = contract.title
        obj['مبلغ'] = contract.price
        obj['تاریخ قرارداد'] = Gregorian(contract.contract_date).persian_string()
        obj['شماره قرارداد'] = contract.contract_number
        obj['لینک سامانه قراردادها'] = 'https://cdb.mporg.ir/ContractViewIndex?ctrId=' + contract.detail_page.url_code
        try:
            obj['شهر'] = contract.city.name
            obj['شهرستان'] = contract.city.town.name
            obj['استان'] = contract.city.town.province.name
        except:
            pass
        try:
            obj['تاریخ خاتمه قرارداد'] = Gregorian(contract.end_date).persian_string()
        except:
            pass
        obj['کارفرما'] = '/'.join([x.name for x in contract.organization.path()])
        try:
            obj['مجری'] = contract.executor.name
        except:
            pass
        obj['ثبت‌کننده قرارداد'] = contract.registrar.name
        obj['تاریخ ثبت در سیستم'] = Gregorian(contract.fetch_date).persian_string()
        obj['طبقه‌بندی'] = contract.category.title
        obj['منبع تامین اعتبار'] = contract.credit_source.title
        obj['شرایط عمومی قرارداد'] = contract.general_rule.title
        i = 0
        for error, label in contract.ERROR_LIST:
            obj[label] = 'بلی' if (contract.errors & (2 ** i)) else 'خیر'
            i += 1
        contracts_to_export.append(obj)
    #        print(str(contract.id))
    df = pandas.DataFrame(contracts_to_export)

    df.to_excel('../all_contracts.xlsx', index=False, sheet_name=Gregorian(datetime.now().date()).persian_string())


def get_path(path):
    import requests
    from django.conf import settings
    requests.get(settings.PROTOCOL + '://' + settings.BACK_DOMAIN + '/' + path)


def warm_cache():
    from django.core.cache import cache
    from datetime import datetime,timedelta
    two_month_ago=datetime.now()-timedelta(days=60)
    two_month_ago=str(two_month_ago.date())
    cache.clear()
    get_path('aggregate/stat')
    get_path('attempts?limit=60')
    get_path('aggregate/daily_fetch_per_top_organization?limit=10000&date__gte='+two_month_ago)
    get_path('categories/?limit=100000')
    get_path('credit_sources/?limit=100000')
    get_path('general_rules/?limit=100000')
    get_path('provinces/?limit=100000')
    get_path('top_organizations/')
    get_path('people')
    get_path('contracts/?limit=10&ordering=-id&page=1')
    get_path('aggregate/province/?limit=10000')
    get_path('aggregate/town/?limit=10000')
    get_path('aggregate/top_organization/year/?limit=100000')
    get_path('aggregate/top_organization/month/?limit=100000')
