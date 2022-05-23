import datetime


class DateHelper:
    def __init__(self, start_date, end_date):
        self.start_date = start_date
        self.end_date = end_date

    def get_date_range(self):
        start_date = self.start_date
        end_date = self.end_date
        date_range = []
        while start_date <= end_date:
            date_range.append(start_date)
            start_date += datetime.timedelta(days=1)
        return

    def is_between(self, date):
        return self.start_date <= date <= self.end_date


