from django.contrib.auth.models import AbstractUser
from django.db import models

from decimal import Decimal

# Create your models here.
class User(AbstractUser):
    pass


class Transaction(models.Model):
    user = models.ForeignKey("User", on_delete=models.CASCADE, related_name="trades_u")
    contract = models.ForeignKey("Contract", on_delete=models.CASCADE, related_name="trades_c")
    side = models.CharField(max_length=4)
    qty = models.SmallIntegerField()
    avg = models.DecimalField(max_digits=7, decimal_places=2)
    total = models.DecimalField(max_digits=8, decimal_places=2)
    timestamp = models.DateTimeField()

    def __str__(self):
        return f"{self.contract.ticker} {self.contract.strike} {self.contract.opt} {self.contract.exp} - {self.side} - QTY: {self.qty} AVG: ${self.avg} TOTAL ${self.total} - {self.timestamp} - {self.user}"


class Contract(models.Model):
    user = models.ForeignKey("User", on_delete=models.CASCADE, related_name="contracts")
    ticker = models.CharField(max_length=8)
    exp = models.DateField()
    opt = models.CharField(max_length=4)
    strike = models.CharField(max_length=8)
    open_avg = models.DecimalField(max_digits=7, decimal_places=2)
    open_qty = models.SmallIntegerField()
    ref = models.CharField(max_length=45)

    def __str__(self):
        return f"{self.ticker} {self.strike} {self.opt} {self.exp} - QTY OPEN: {self.open_qty} AVG: ${self.open_avg} OPEN TOTAL: ${self.open_qty * self.open_avg} - {self.user}"