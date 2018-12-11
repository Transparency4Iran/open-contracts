from django.db import models
from fetch.models import Detail
from org.models import Organization, Executor, People
from location.models import City
from bitfield import BitField


class GeneralRule(models.Model):
    title = models.CharField(max_length=1024)

    def __str__(self):
        return self.title


class Category(models.Model):
    title = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.title


class CreditSource(models.Model):
    title = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.title


class Contract(models.Model):
    detail_page = models.OneToOneField(Detail, related_name="contract")
    title = models.CharField(max_length=1024)
    organization = models.ForeignKey(Organization, related_name="contracts")
    top_organization = models.ForeignKey(Organization, related_name="all_contracts")
    executor = models.ForeignKey(Executor, related_name="contracts", null=True, blank=True)
    city = models.ForeignKey(City, related_name="contracts", null=True, blank=True)
    contract_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    jalali_year = models.IntegerField()
    jalali_month = models.IntegerField()
    jalali_day = models.IntegerField()
    price = models.BigIntegerField(null=True, blank=True)
    code = models.CharField(max_length=32)
    contract_number = models.CharField(max_length=32, null=True, blank=True)
    registrar = models.ForeignKey(People)
    general_rule = models.ForeignKey(GeneralRule, related_name="contracts", null=True, blank=True)
    category = models.ForeignKey(Category, related_name="contracts")
    credit_source = models.ForeignKey(CreditSource, related_name="contracts")
    fetch_date = models.DateField(null=True, blank=True)
    ERROR_LIST = (
        ('conceptual', 'خطای مفهومی ثبت شده توسط دبیر'),
        ('future_date', 'تاریخ انعقاد در آینده'),
        ('no_end_date', 'فیلد خالی مهلت'),
        ('bad_end_date', 'ثبت نادرست مهلت'),
        ('negative_duration', 'مهلت زودتر از انعقاد'),
        ('no_location', 'فیلد خالی مکان'),
        ('no_price', 'فیلد خالی قیمت'),
        ('no_executor', 'فیلد خالی مجری'),
    )
    errors = BitField(flags=ERROR_LIST)

    def error_displays(self):
        ans = []
        for error, has in self.errors:
            if has:
                ans.append(self.errors.get_label(error))
        return ans

    def __str__(self):
        return self.detail_page.url_code

    def link(self):
        return "https://cdb.mporg.ir/ContractViewIndex?ctrId=" + self.detail_page.url_code

    def organizations(self):
        org = self.organization
        ans = [org]
        while org.id != self.top_organization_id:
            org = org.father
            ans.append(org)
        return ans[::-1]

    def update_aggregations(self):
        org = self.top_organization
        registrar = self.registrar
        org.contracts_count += 1
        registrar.contracts_count += 1
        if int(self.errors) > 0:
            org.errors_count += 1
            registrar.errors_count += 1
            page = self.detail_page.page()
            if page:
                attempt = page.attempt
                attempt.with_errors_count += 1
                attempt.save()
        org.save()
        registrar.save()

        from aggregation.models import DailyFetchPerTopOrganization, ErrorSpectrum
        record, created = DailyFetchPerTopOrganization.objects.get_or_create(date=self.fetch_date,
                                                                             top_organization=self.top_organization)
        if not created:
            record.count += 1
            record.save()

        for i in range(0, len(self.ERROR_LIST)):
            if self.errors & (2 ** i):
                record, created = ErrorSpectrum.objects.get_or_create(bit=i)
                if not created:
                    record.count += 1
                    record.save()


from django.db.models.signals import post_save
from django.dispatch import receiver


@receiver(post_save, sender=Contract)
def housekeeping_after_contract(sender, instance, created, **kwargs):
    if created:
        instance.update_aggregations()
