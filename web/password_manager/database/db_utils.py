from datetime import datetime


def validate_reset_link_date(experience_date_string):
    exp = datetime.strptime(experience_date_string, '%Y-%m-%d %H:%M:%S.%f')
    now = datetime.now()
    hours = _count_difference_in_hours(now, exp)
    if hours > 0:
        return True
    return False


def _count_difference_in_hours(datetime1, datetime2):
    diff = datetime2 - datetime1
    days, seconds = diff.days, diff.seconds
    hours = days * 24 + seconds // 3600
    return hours
