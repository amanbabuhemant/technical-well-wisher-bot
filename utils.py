
MONTH_MAP = {
    # 0: (shortname, fullname, maxdaycount)
    1:  ("jan", "january",   31),
    2:  ("feb", "february",  29),
    3:  ("mar", "march",     31),
    4:  ("apr", "april",     30),
    5:  ("may", "may",       31),
    6:  ("jun", "june",      30),
    7:  ("jul", "july",      31),
    8:  ("aug", "august",    31),
    9:  ("sep", "september", 30),
    10: ("oct", "october",   31),
    11: ("nov", "november",  30),
    12: ("dec", "december",  31),
}

def get_month_index_by_name(month: str) -> int: # 1 based index
    month = month.casefold()
    for key in MONTH_MAP.keys():
        if month in MONTH_MAP[key]:
            return key
    return 0


def sanitize_date(date_input: str) -> str | None:
    """
    Sanatize date in `MM-DD` format
    accepts:
        day with or without ziro prefix
        month with or without ziro prefix
        mmm format months, case insansitive
        full name of months, case insansitive
    """

    if "-" not in date_input:
        return None

    if len(date_input) < 3:
        return None

    month, day = date_input.split("-")

    try:
        day = int(day)
    except:
        return None

    if month.isnumeric():
        month = int(month)
    else:
        month = get_month_index_by_name(month)
    
    if not 12 >= month >= 1:
        return None

    return f"{str(month).zfill(2)}-{str(day).zfill(2)}"


