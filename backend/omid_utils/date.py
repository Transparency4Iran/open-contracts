from datetime import timedelta, datetime
from omid_utils.standard import standard_persian
from .jalali import Persian, Gregorian

WEEK_DAYS = {
    0: "دوشنبه",
    1: "سه‌شنبه",
    2: "چهارشنبه",
    3: "پنجشنبه",
    4: "جمعه",
    5: "شنبه",
    6: "یکشنبه",
}


def week_day_to_weekday(d):
    return (d - 2) % 7


def weekday_to_week_day(d):
    return ((d + 1) % 7) + 1


def find_first_friday(jalali_year):
    noruz = Persian(jalali_year, 1, 1).gregorian_datetime()
    while noruz.weekday() != 4:
        noruz = noruz + timedelta(days=1)
    return noruz


def get_week_num(jalali_year, friday_date):
    return (((friday_date - find_first_friday(jalali_year)).days) / 7) + 1


def persian_week_day_to_num(string):
    string = standard_persian(string.strip())
    if string.startswith("شنبه"):
        return 5
    elif string.startswith("یک"):
        return 6
    elif string.startswith("دو"):
        return 0
    elif string.startswith("سه"):
        return 1
    elif string.startswith("چهار"):
        return 2
    elif string.startswith("پنج"):
        return 3
    elif string.startswith("جمع"):
        return 4


def get_date_with_persian_day(day):
    day_num = persian_week_day_to_num(day)
    now = datetime.now()
    today = now.date()
    today_num = today.weekday()
    diff = day_num - today_num
    if diff > 4:
        diff -= 7
    if diff < -4:
        diff += 7
    return (now + timedelta(days=diff)).date()


def get_end_date(start, year, month, day):
    try:
        if not year and not month and not day:
            return None
        year = int(year)
        month = int(month)
        day = int(day)
        if year > 75:
            if year < 100:
                year = 1300 + year
            if month > 0 and day > 0:
                return Persian(year, month, day).gregorian_datetime()
            if month <= 0 or month == 12:
                tomorrow = Persian(year + 1, 1, 1).gregorian_datetime()
            else:
                tomorrow = Persian(year, month + 1, 1).gregorian_datetime()
            return tomorrow - timedelta(days=1)
        start = start + timedelta(days=day)
        start_year, start_month, start_day = Gregorian(start).persian_tuple()
        new_year = start_year + year
        new_month = start_month + month
        if new_month > 12:
            new_year += (new_month // 12)
            new_month = new_month % 12
        if new_month == 0:
            new_month = 12
            new_year -= 1
        return Persian(new_year, new_month, start_day).gregorian_datetime()
    except:
        return None
    return None
