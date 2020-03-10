import time
import datetime

def dates(years, months, days):
    t1_l = [1, 3, 5, 7, 8, 10, 12]
    t0_l = [4, 6, 9, 11]
    t8_l = [2]
    for year in range(years, 2020):
        for month in range(months, 13):
            if month in t8_l and years % 4 == 0:
                for day in range(days, 30):
                    print('{0}-{1}-{2}'.format(year, month, day))
            elif month in t8_l:
                for day in range(days, 29):
                    print('{0}-{1}-{2}'.format(year, month, day))
            elif month in t0_l:
                for day in range(days, 31):
                    print('{0}-{1}-{2}'.format(year, month, day))
            else:
                for day in range(days, 32):
                    print('{0}-{1}-{2}'.format(year, month, day))


if __name__ == '__main__':
    years = 2016
    months = 1
    days = 1
    dates(years, months, days)