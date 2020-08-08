from django.db import models
from django.utils import timezone

# Create your models here.
class Ticker(models.Model):
    symbol = models.CharField(max_length=8, primary_key=True)
    lastedit = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return f"{self.symbol} - Last edit: {self.lastedit}"

class Historical(models.Model):
    ticker = models.ForeignKey('Ticker', on_delete=models.CASCADE)
    date = models.CharField(max_length=10, primary_key=True)
    weekday = models.CharField(max_length=3)
    priceopen = models.DecimalField(max_digits=6, decimal_places=2)
    priceclose = models.DecimalField(max_digits=6, decimal_places=2)
    overnight = models.DecimalField(max_digits=6, decimal_places=2)
    intraday = models.DecimalField(max_digits=6, decimal_places=2)
    sum24 = models.DecimalField(max_digits=6, decimal_places=2)
    volume = models.PositiveIntegerField()
    high = models.DecimalField(max_digits=6, decimal_places=2)
    low = models.DecimalField(max_digits=6, decimal_places=2)
    
    def __str__(self):
        return f"{self.ticker.symbol} - {self.date}"




# Historical.objects.filter(date__gte="2020-06-11").filter(weekday="MON").values(priceopen)
# Historical.objects.filter(date__gte="2020-06-11").filter(weekday="MON").values('date','priceopen')
# o = Historical.objects.filter(date__gte="2020-06-11").filter(weekday="MON").aggregate(Avg('priceopen'))
# o = o['priceopen__avg']
