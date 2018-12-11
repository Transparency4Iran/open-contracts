from django.db import models


class Organization(models.Model):
    name = models.CharField(max_length=128)
    father = models.ForeignKey('self', related_name="children", null=True, blank=True)
    correct_name = models.CharField(max_length=128, null=True, blank=True)
    contracts_count=models.IntegerField(default=0)
    errors_count=models.IntegerField(default=0)

    class Meta:
        unique_together = ('name', 'father')

    def display_name(self):
        if self.correct_name:
            return self.correct_name
        return self.name
    def __str__(self):
        return self.display_name()

    def path(self):
        org = self
        ans = []
        while org:
            ans.append(org)
            org = org.father
        return ans[::-1]

    def leaves(self):
        ans = []
        list_to_iterate = list(self.children.all())
        for child in list_to_iterate:
            children = child.children.all()
            if children:
                list_to_iterate += list(child.children.all())
            elif child not in ans:
                ans.append(child)
        return ans

    def implicit_contracts(self):
        orgs = self.leaves()
        orgs.append(self)
        from main.models import Contract
        return Contract.objects.filter(organization__in=orgs)

    def implicit_sum(self):
        return self.implicit_contracts().aggregate(models.Sum('price'))["price__sum"]

    def implicit_count(self):
        return self.implicit_contracts().aggregate(models.Count('price'))["price__count"]


class Budget(models.Model):
    organization = models.ForeignKey(Organization, related_name='budgets')
    year = models.IntegerField()
    amount = models.IntegerField()

    def __str__(self):
        return self.organization.display_name()+'-'+str(self.year)
    class Meta:
        unique_together = ('organization', 'year')


class Executor(models.Model):
    name = models.CharField(max_length=128, unique=True)

    def provinces(self):
        ids = self.contracts.filter(executor=self).values_list('city__town__province', flat=True)
        from location.models import Province
        return Province.objects.filter(id__in=ids)

    def top_organizations(self):
        ids = self.contracts.filter(executor=self).values_list('top_organization', flat=True)
        return Organization.objects.filter(id__in=ids)

    def __str__(self):
        return self.name


class People(models.Model):
    name = models.CharField(max_length=64, unique=True)
    correct_name = models.CharField(max_length=128, null=True, blank=True)
    contracts_count = models.IntegerField(default=0)
    errors_count = models.IntegerField(default=0)

    def display_name(self):
        if self.correct_name:
            return self.correct_name
        return self.name

    def __str__(self):
        return self.display_name()


class Synonym(models.Model):
    name = models.CharField(max_length=64)
    executor = models.ForeignKey(Executor, related_name="synonyms", null=True, blank=True)

    def __str__(self):
        return self.name


from django.db.models.signals import post_save
from django.dispatch import receiver


@receiver(post_save, sender=Synonym)
def migrate_after_synonym(sender, instance, created, **kwargs):
    if instance.executor:
        previous = Executor.objects.filter(name=instance.name).first()
        if previous:
            for contract in previous.contracts.all():
                contract.executor = instance.executor
                contract.save()
            previous.delete()
