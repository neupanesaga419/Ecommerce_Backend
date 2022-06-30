from django.test import TestCase
from calendar import monthrange
from datetime import date,timedelta
from .models import *

def year_month(sth):
    year_today = sth.year
    month_today = sth.month
    return year_today,month_today

def month_days(year,month):
    month_day = monthrange(year,month)
    return month_day[1]


def one_month_ago(date_today,month_days):
    date_one_month_ago = date_today - timedelta(month_days)
    return date_one_month_ago

def months_generator():
    twelve_months = []
    date_today = date.today()
    twelve_months.append(date_today)
    for i in range(11):
        year_today,month_today = year_month(date_today)
        month_day = month_days(year_today, month_today)
        date_today = one_month_ago(date_today, month_day)
        # print(date_today)
        twelve_months.append(date_today)
    return twelve_months

twelve_months = months_generator()

sold_products = SoldProducts.objects.filter(added_date__lte=twelve_months[0])
print(sold_products)

# Create your tests here.
