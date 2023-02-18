import os
import random

dates = {
    '01': {'monthName': 'января', 'n_days': 31},
    '02': {'monthName': 'февраля', 'n_days': 29},
    '03': {'monthName': 'марта', 'n_days': 31},
    '04': {'monthName': 'апреля', 'n_days': 30},
    '05': {'monthName': 'мая', 'n_days': 31},
    '06': {'monthName': 'июня', 'n_days': 30},
    '07': {'monthName': 'июля', 'n_days': 31},
    '08': {'monthName': 'августа', 'n_days': 31},
    '09': {'monthName': 'сентября', 'n_days': 30},
    '10': {'monthName': 'октября', 'n_days': 31},
    '11': {'monthName': 'ноября', 'n_days': 30},
    '12': {'monthName': 'декабря', 'n_days': 31},
}
zxc = []

for monthNumber, val in dates.items():
    monthName, n_days = val.values()
    for day in range(1, n_days):
        month = '.' + \
            str(monthNumber) if random.random() > .5 else ' ' + monthName
        if day < 10:
            zxc.append('0' + str(day) + month)
        zxc.append(str(day) + month)

with open(os.path.dirname(os.path.abspath(__file__)) + '/../../../datasets/dates/dates.txt', 'a') as file:
    file.write('\n'.join(elem for elem in zxc))
