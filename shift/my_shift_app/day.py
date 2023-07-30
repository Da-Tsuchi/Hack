from calendar import monthcalendar
import calendar

def get_days_with_weekday(year, month):
    # 曜日名を日本語で定義
    weekdays_japanese = ["月", "火", "水", "木", "金", "土", "日"]
    
    cal = monthcalendar(year, month)
    days_with_weekday = []
    for week in cal:
        for day in week:
            if day != 0:  # monthcalendarは月の外側の日付を0で埋める
                weekday = weekdays_japanese[calendar.weekday(year, month, day)]
                days_with_weekday.append((day, weekday))
    return days_with_weekday