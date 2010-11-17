# -*- coding: utf-8 -*-

# The MIT License
#
# Copyright (c) 2008 M. Nasimul Haque
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

import datetime

from django import template

from utils import bangla_date as bdate, BANGLA_MONTHS, bangla_number

register = template.Library()

class BengaliLocaleException:
    pass

@register.filter
def bangla_numeral(value):
    from django.utils.translation import get_language
    if not get_language() == 'bn':
        return value

    return bangla_number(value)

@register.filter
def bangla_date(eng_date, show_time=True):
    beng_date = bdate(eng_date)
    # beng_date = '%(day)02d-%(month)02d-%(year)4d' % (beng_date)
    beng_date['month'] = BANGLA_MONTHS[beng_date['month']]
    beng_date = '%(day)d %(month)s, %(year)d' % (beng_date)
    if show_time:
        beng_date += '; %02d:%02d' % (eng_date.hour, eng_date.minute)

    return beng_date

@register.simple_tag
def bangla_today(zone):
    from pytz import timezone

    zone = timezone(zone)
    today = datetime.datetime.today()
    today = zone.localize(today)
    today = bdate(today)
    today = u'%02d %s, %4d বঙ্গাব্দ' % (today['day'],
                                 BANGLA_MONTHS[today['month']],
                                 today['year'])
    return bangla_number(today)

@register.filter
def bangla_month(value):
    from django.utils.translation import get_language
    if not get_language() == 'bn':
        raise BengaliLocaleException

    return BANGLA_MONTHS[value]

@register.filter
def bangla_greg_month(value):
    from django.utils.translation import get_language
    if not get_language() == 'bn':
        month_names = {
            1: u'January',
            2: u'February',
            3: u'March',
            4: u'April',
            5: u'May',
            6: u'June',
            7: u'July',
            8: u'August',
            9: u'September',
           10: u'October',
           11: u'November',
           12: u'December',
        }

        return month_names[value]

    month_names = {
        1: u'জানুয়ারি',
        2: u'ফেব্রুয়ারি',
        3: u'মার্চ',
        4: u'এপ্রিল',
        5: u'মে',
        6: u'জুন',
        7: u'জুলাই',
        8: u'আগষ্ট',
        9: u'সেপ্টেম্বর',
       10: u'অক্টোবর',
       11: u'নভেম্বর',
       12: u'ডিসেম্বর',
    }

    return month_names[value]

@register.filter
def bangla_weekday(value):
    from django.utils.translation import get_language
    if not get_language() == 'bn':
        weekdays = {
            0: u'Monday',
            1: u'Tuesday',
            2: u'Wednesday',
            3: u'Thursday',
            4: u'Friday',
            5: u'Saturday',
            6: u'Sunday',
        }
        return weekdays[value]

    weekdays = {
        0: u'সোমবার',
        1: u'মঙ্গলবার',
        2: u'বুধবার',
        3: u'বৃহস্পতিবার',
        4: u'শুক্রবার',
        5: u'শনিবার',
        6: u'রবিবার',
    }

    return weekdays[value]
