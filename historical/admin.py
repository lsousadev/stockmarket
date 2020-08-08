from django.contrib import admin

from .models import Ticker, Historical

# Register your models here.
admin.site.register(Ticker)
admin.site.register(Historical)