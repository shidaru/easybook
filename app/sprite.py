# coding: utf-8
import datetime


def get_today():
    today = datetime.date.today()
    return today


def get_current_month():
    current_month = get_today().strftime("%Y-%m")
    return current_month


def get_before_month():
    cm = get_current_month()
    year, month = cm.split('-')
    before = '0' + str(int(month) - 1)
    before_month = '-'.join([year, before])
    return before_month
