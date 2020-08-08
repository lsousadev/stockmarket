from django.contrib.auth.models import AbstractUser
from django.db import models

from decimal import Decimal

# Create your models here.
class User(AbstractUser):
    profit = models.DecimalField(max_digits=8, decimal_places=2, default=Decimal('0.00'))


class Transaction(models.Model):
    user = models.ForeignKey("User", on_delete=models.CASCADE, related_name="transactions")
    ticker = models.CharField(max_length=8)
    exp = models.DateField()
    opt = models.CharField(max_length=4)
    strike = models.CharField(max_length=8)
    side = models.CharField(max_length=4)
    qty = models.SmallIntegerField()
    avg = models.DecimalField(max_digits=7, decimal_places=2)
    total = models.DecimalField(max_digits=8, decimal_places=2)
    datetime = models.DateTimeField()
    og_line = models.ForeignKey("Contract", on_delete=models.CASCADE, related_name="trades", null=True, blank=True)

    def __str__(self):
        return f"{self.ticker} {self.strike} {self.opt} {self.exp}, {self.qty} contract(s), average ${self.avg} ($ {self.total})."


class Contract(models.Model):
    user = models.ForeignKey("User", on_delete=models.CASCADE, related_name="contracts")
    og_line = models.CharField(max_length=45)
    exp = models.DateField()
    avg = models.DecimalField(max_digits=7, decimal_places=2)
    open_qty = models.SmallIntegerField()
    open_total = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self):
        return f"{self.og_line} - {self.open_qty} at average ${self.avg} ($ {self.open_total})."