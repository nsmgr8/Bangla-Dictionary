# -*- coding: utf-8 -*-

import datetime
import calendar

BANGLA_MONTHS = {
    1: u'বৈশাখ',
    2: u'জৈষ্ঠ্য',
    3: u'আষাড়',
    4: u'শ্রাবণ',
    5: u'ভাদ্র',
    6: u'আশ্বিন',
    7: u'কার্তিক',
    8: u'অগ্রহায়ণ',
    9: u'পৌষ',
   10: u'মাঘ',
   11: u'ফাল্গুন',
   12: u'চৈত্র',
}

BANGLA_DIGITS = {
    u'1': u'১',
    u'2': u'২',
    u'3': u'৩',
    u'4': u'৪',
    u'5': u'৫',
    u'6': u'৬',
    u'7': u'৭',
    u'8': u'৮',
    u'9': u'৯',
    u'0': u'০',
}

def bangla_number(value):
    value = unicode(value)
    for e, b in BANGLA_DIGITS.iteritems():
        value = value.replace(e, b)

    return value

def eng_number(value):
    value = unicode(value)
    for e, b in BANGLA_DIGITS.iteritems():
        value = value.replace(b, e)

    return value

def bangla_date(eng_date):
    eng_day = eng_date.day
    eng_month = eng_date.month
    eng_year = eng_date.year

    eng_days = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    diffs = ((17, 13), (18, 12), (17, 14), (17, 13), (17, 14), (17, 14),
             (16, 15), (16, 15), (16, 15), (15, 15), (16, 14), (16, 14))

    beng_days = [31 for i in range(6)] + [30 for i in range(6)]

    leap_year = calendar.isleap(eng_year)

    if leap_year:
        eng_days[1] += 1
        beng_days[10] += 1

    beng_year = eng_year - 594
    days_passed = eng_day
    for i in range(eng_month-1):
        days_passed += eng_days[i]
    if days_passed > 103:
        beng_year += 1

    beng_month = eng_month + 8 if eng_month < 5 else eng_month - 4
    beng_day = eng_day + diffs[eng_month - 1][0]

    if beng_day > beng_days[beng_month - 1]:
        beng_day = eng_day - diffs[eng_month - 1][1]
        beng_month += 1
        if beng_month > 12:
            beng_month -= 12

    if eng_day < 14 and eng_month == 3 and not leap_year:
        beng_day -= 1
    if eng_day == 14 and eng_month == 3 and not leap_year:
        beng_day, beng_month = 30, 11

    return {'day': beng_day, 'month': beng_month, 'year': beng_year,}

