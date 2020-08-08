from django import forms
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse

from datetime import date

from .models import Ticker, Historical
from .helpers import yf, hist_render

class StudyForm(forms.Form):
    ticker = forms.CharField(label="Ticker")
    startdate = forms.CharField(label="Start Date")
    enddate = forms.CharField(label="End Date")

# Create your views here.
def index(request):
    return render(request, "historical/index.html", {
        "studyform": StudyForm()
    })

def study(request):
    studyform = StudyForm(request.POST)
    if studyform.is_valid():
        error_message = []
        # get ticker name from form and create/update it in "Ticker" table
        ticker = studyform.cleaned_data['ticker']
        t = Ticker(symbol=ticker)
        t.save()
        # add 1 year of historical data from ticker to "Historical" table
        # t is needed because it is a model/foreign key)
        yf(ticker, t)
        date_range = Historical.objects.filter(ticker=ticker).values_list('date', flat=True)
        if not date_range[1]:
            error_message.append("Ticker does not exist or not supported by Yahoo Finance.")
        startdate = studyform.cleaned_data['startdate']
        if startdate < date_range[0]:
            error_message.append("The start date cannot be over a year in the past.")
        enddate = studyform.cleaned_data['enddate']
        if enddate > date_range[len(date_range) - 1]:
            error_message.append("The end date has to be the last day the stock was traded (" + date_range[len(date_range) - 1] + ") or earlier.")
        if error_message:
            return render(request, "historical/index.html", {
                "studyform": studyform,
                "error": error_message
            })
        response_data = hist_render(ticker, startdate, enddate)
    print(response_data)
    return render(request, "historical/study.html", {
            "ticker": ticker,
            "response": response_data
        })
