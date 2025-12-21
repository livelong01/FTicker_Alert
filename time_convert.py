import re


def duration_to_minutes(duration):
    hours = minutes = 0
    h = re.search(r'(\d+)H', duration)
    m = re.search(r'(\d+)M', duration)

    if h:
        hours = int(h.group(1))
    if m:
        minutes = int(m.group(1))

    return hours * 60 + minutes
