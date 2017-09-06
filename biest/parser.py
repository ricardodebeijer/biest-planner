import datetime
import os

import xlrd
from xlrd import xldate_as_tuple

from biestplanner import settings

book_date_format = None
bookings = None
last_relatie = None


def getbookings():
    global bookings
    bookings = []
    path = settings.MEDIA_ROOT + '/plannings/' + 'planning.xls'
    if not os.path.exists(path):
        return bookings
    book = xlrd.open_workbook(path)
    global book_date_format
    book_date_format = book.datemode
    sh = book.sheet_by_index(0)
    for rx in range(sh.nrows):
        row = sh.row(rx)
        booking = {}
        try:
            booking["datum"] = get_date(row[0])
            booking["resno"] = get_resno(row[1])
            booking["start"] = convert_date(row[2].value)
            booking["eind"] = convert_date(row[3].value)
            booking["relatie"] = get_relatie(row[4])
            booking["aantal"] = int(row[5].value)
            booking["artikel"] = row[6].value
            booking["info"] = get_info(row[7])
            bookings.append(booking)
        except ValueError:
            pass

    return bookings


def get_date(cell):
    if cell.ctype == xlrd.XL_CELL_EMPTY:
        # global bookings
        # length = len(bookings)
        # print('Length:' + str(length))
        # index = length - 1
        # print('Index:' + str(index))
        # if index >= 0:
        #     prev_book = bookings[index]
        #     prev_date = prev_book["datum"]
        #     # print("prev date:" + str(prev_date))
        #     return prev_date
        # else:
        #     return convert_date(36525)
        return None
    else:
        return convert_date(cell.value)


def get_resno(cell):
    if cell.ctype == xlrd.XL_CELL_EMPTY:
        # global bookings
        # length = len(bookings)
        # print('Length:' + str(length))
        # index = length - 1
        # print('Index:' + str(index))
        # if index >= 0:
        #     prev_book = bookings[index]
        #     prev_resno = prev_book["resno"]
        #     # print("prev date:" + str(prev_date))
        #     return prev_resno
        # else:
        return None
    else:
        return int(cell.value)


def get_relatie(cell):
    global bookings
    length = len(bookings)
    index = length - 1
    if index >= 0:
        prev_book = bookings[index]
        prev_relatie = prev_book["relatie"]
        global last_relatie
        if prev_relatie == cell.value or last_relatie == cell.value:
            return None
        else:
            last_relatie = cell.value

    return cell.value


def get_info(cell):
    # print('info type:' + str(cell.ctype))
    if cell.ctype == xlrd.XL_CELL_NUMBER:
        return None
    else:
        return cell.value


def convert_date(date):
    return datetime.datetime(*xldate_as_tuple(float(date), book_date_format))
