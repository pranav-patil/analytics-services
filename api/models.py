from django.db import models
from decimal import Decimal


class VideoGameSales(models.Model):
    rank = models.IntegerField()
    name = models.CharField(max_length=200)
    platform = models.CharField(max_length=100)
    year = models.CharField(max_length=4, blank=True, null=True)
    genre = models.CharField(max_length=80, null=True, blank=True, default='')
    publisher = models.CharField(max_length=100, null=True, blank=True, default='')
    usa_sales = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, default=Decimal('0.00'))
    europe_sales = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, default=Decimal('0.00'))
    japan_sales = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, default=Decimal('0.00'))
    other_sales = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, default=Decimal('0.00'))
    global_sales = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, default=Decimal('0.00'))

    class Meta:
        ordering = ['rank']
        verbose_name = "Video Game Sales"
        verbose_name_plural = "Video Game Sales"

    def __str__(self):
        return 'name:' + str(self.name) + ' platform: ' + str(self.platform)

    objects = models.Manager()


class SuicideStatistics(models.Model):
    SEX_CHOICES = (('female', 'female'), ('male', 'male'))

    country = models.CharField(max_length=50, null=False, blank=False)
    year = models.CharField(max_length=4, blank=False, null=False)
    sex = models.CharField(max_length=10, choices=SEX_CHOICES)
    age = models.CharField(max_length=20, null=False, blank=False)
    suicides_no = models.IntegerField(null=False, blank=False, default=0)
    population = models.IntegerField(null=False, blank=False, default=0)

    class Meta:
        ordering = ['country']
        verbose_name = "WHO Suicide Statistics"
        verbose_name_plural = "WHO Suicide Statistics"

    def __str__(self):
        return f"country = {self.country}, year = {self.year}, sex = {self.sex}, age = {self.age}"

    objects = models.Manager()
