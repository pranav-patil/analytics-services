from django.db import models
from decimal import Decimal


class VideoGameSales(models.Model):
    rank = models.IntegerField()
    name = models.CharField(max_length=120)
    platform = models.CharField(max_length=50)
    year = models.CharField(max_length=4, blank=True, null=True)
    genre = models.CharField(max_length=50, null=True, blank=True, default='')
    publisher = models.CharField(max_length=70, null=True, blank=True, default='')
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
        return 'name:'+str(self.name)+' platform: '+str(self.platform)

    objects = models.Manager()

