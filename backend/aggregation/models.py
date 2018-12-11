from django.db import models
from org.models import Organization


class DailyFetchPerTopOrganization(models.Model):
    date = models.DateField()
    top_organization = models.ForeignKey(Organization)
    count = models.IntegerField(default=1)

    class Meta:
        unique_together = ('date', 'top_organization')


class ErrorSpectrum(models.Model):
    bit = models.IntegerField(primary_key=True)
    count = models.IntegerField(default=1)

    def label(self):
        from main.models import Contract
        error, label = Contract.ERROR_LIST[self.bit]
        return label
