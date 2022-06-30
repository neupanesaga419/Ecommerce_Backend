
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
    month_short = []
    date_today = date.today()
    twelve_months.append(date_today)
    month_short.append(date_today.strftime("%b"))
    for i in range(12):
        year_today,month_today = year_month(date_today)
        month_day = month_days(year_today, month_today)
        date_today = one_month_ago(date_today, month_day)
        month_short.append(date_today.strftime("%b"))
        twelve_months.append(date_today)
        
    return twelve_months,month_short

def get_total_sold_monthly(model,date_list,short_month):
    short_month.pop()
    monthly_sold_data = []
    for i in range(len(date_list)-1):
        sold_products = model.objects.filter(added_date__lte=date_list[i],
                                                    added_date__gt=date_list[i+1])
        total_sold_yesterday = 0
        for item in sold_products:
            total_sold_yesterday = total_sold_yesterday + item.total_on_each_item()
        monthly_sold_data.append(total_sold_yesterday)
    return monthly_sold_data,short_month


        

