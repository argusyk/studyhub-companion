from legacy.flask_app.utils import parse_dt, DEBUG


def late_days(deadline, submitted):
    d = parse_dt(deadline)
    s = parse_dt(submitted)
    days = (s - d).days  # повні доби
    if days < 0:
        days = 0
    return days


def calc_final(score, deadline, submitted):
    days = late_days(deadline, submitted)
    if DEBUG:
        print("calc_final", score, days)
    # штраф: 10% за кожен повний день, після 5 днів не приймається
    if days > 5:
        return None
    if days > 0:
        score = score - score * 0.1 * days
    return round(score)  # round() Python: половини до парного
