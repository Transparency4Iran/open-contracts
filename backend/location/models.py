from django.db import models


class Province(models.Model):
    name = models.CharField(max_length=64, unique=True)

    def __str__(self):
        return self.name


class Town(models.Model):
    name = models.CharField(max_length=64)
    province = models.ForeignKey(Province, related_name="towns")
    lat = models.DecimalField(max_digits=10, decimal_places=8, null=True, blank=True)
    lon = models.DecimalField(max_digits=11, decimal_places=8, null=True, blank=True)

    def geocode(self):
        if not self.lat or not self.lon:
            try:
                import googlemaps
                gmaps = googlemaps.Client(key='AIzaSyAkfJif6SGvLjSeqN-ehE4X_8c4KsegNO8')
                address = 'ایران, استان '
                address += self.province.name
                address += ', شهرستان '
                address += self.name
                geocode_result = gmaps.geocode(address)
                self.lat = geocode_result[0]['geometry']['location']['lat']
                self.lon = geocode_result[0]['geometry']['location']['lng']
                self.save()
            except:
                pass

    class Meta:
        unique_together = ('name', 'province')

    def __str__(self):
        return self.name


class City(models.Model):
    name = models.CharField(max_length=64)
    town = models.ForeignKey(Town, related_name='cities')
    lat = models.DecimalField(max_digits=10, decimal_places=8, null=True, blank=True)
    lon = models.DecimalField(max_digits=11, decimal_places=8, null=True, blank=True)

    class Meta:
        unique_together = ('name', 'town')

    def __str__(self):
        return self.name

    def province(self):
        return self.town.province

    def geocode(self):
        if not self.lat or not self.lon:
            try:
                import googlemaps
                gmaps = googlemaps.Client(key='AIzaSyAkfJif6SGvLjSeqN-ehE4X_8c4KsegNO8')
                address = 'ایران, استان '
                address += self.town.province.name
                address += ', شهرستان '
                address += self.town.name
                address += ', '
                address += self.name
                geocode_result = gmaps.geocode(address)
                self.lat = geocode_result[0]['geometry']['location']['lat']
                self.lon = geocode_result[0]['geometry']['location']['lng']
                self.save()
            except:
                pass


from django.db.models.signals import post_save
from django.dispatch import receiver


@receiver(post_save, sender=City)
def migrate_after_synonym(sender, instance, created, **kwargs):
    if created:
        instance.geocode()


@receiver(post_save, sender=Town)
def migrate_after_synonym(sender, instance, created, **kwargs):
    if created:
        instance.geocode()
