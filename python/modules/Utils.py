from datetime import datetime
from datetime import timedelta


def check_date_range_by_days(start: str, end: str):
    start = datetime.strptime(start, "%Y-%m-%d")
    end = datetime.strptime(end, "%Y-%m-%d")
    delta = end - start
    return delta.days


def get_range_dates_by_chunks(start: str, end: str, window: int):
    start = datetime.strptime(start, "%Y-%m-%d")
    end = datetime.strptime(end, "%Y-%m-%d")

    i = True
    chunk_final_date = start
    while chunk_final_date < end:
        if chunk_final_date != start:
            start = chunk_final_date + timedelta(days=1)

        chunk_final_date = chunk_final_date + timedelta(days=window)
        if chunk_final_date > end:
            chunk_final_date = end
        yield str(start.strftime("%Y-%m-%d")), str(chunk_final_date.strftime("%Y-%m-%d"))
