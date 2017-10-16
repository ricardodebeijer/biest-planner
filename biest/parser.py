from datetime import datetime
import os
import xlrd
from xlrd import xldate_as_tuple
from biestplanner import settings

# configurable:
only_show_present = True
show_double_resno = True
show_double_relatie = True
show_double_datum = True

# global variables
book_date_format = None
bookings = None
instructors = None
last_relatie = None
last_datum = None
current_date = None


def get_bookings():
    global current_date, bookings, instructors
    current_date = datetime.today().date()
    bookings = []
    instructors = []
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
            booking["start"] = get_date(row[2])
            booking["eind"] = get_date(row[3])
            booking["relatie"] = get_relatie(row[4])
            booking["aantal"] = get_aantal(row[5])
            booking["artikel"] = get_artikel(row[6])
            booking["info"] = get_info(row[7])
            check_only_add_present_booking(booking)
        except ValueError:
            pass

    return bookings


def get_instructors():
    global instructors
    return instructors


def check_only_add_present_booking(booking):
    global bookings, last_datum, current_date
    if only_show_present:
        datum = booking["datum"]
        if datum is None:
            datum = last_datum

        if last_datum != datum:
            last_datum = datum

        date = datum.date()
        if date >= current_date:
            # print(str(date) + ' valt na vandaag ' + str(current_date))
            bookings.append(booking)
    else:
        bookings.append(booking)


def get_date(cell):
    global last_datum
    if cell.ctype == xlrd.XL_CELL_EMPTY:
        if show_double_datum:
            return last_datum
        else:
            return None
    else:
        return convert_date(cell.value)


def get_resno(cell):
    if cell.ctype == xlrd.XL_CELL_EMPTY:
        global bookings
        length = len(bookings)
        index = length - 1
        if index >= 0 and show_double_resno:
            prev_book = bookings[index]
            prev_resno = prev_book["resno"]
            return prev_resno
        else:
            return None
    else:
        return int(cell.value)


def get_relatie(cell):
    global bookings, last_relatie
    length = len(bookings)
    index = length - 1
    if index >= 0:
        prev_book = bookings[index]
        prev_relatie = prev_book["relatie"]
        if (prev_relatie == cell.value or last_relatie == cell.value) and not show_double_relatie:
            return None
        else:
            last_relatie = cell.value

    return cell.value


def get_aantal(cell):
    return int(cell.value)


def get_artikel(cell):
    global instructors
    artikel = cell.value
    if artikel.startswith('*Instructeur'):
        if artikel not in instructors:
            instructors.append(artikel)
            # print(artikel + ' is toegevoegd')
    return artikel


def get_info(cell):
    if cell.ctype == xlrd.XL_CELL_NUMBER:
        return None
    else:
        return cell.value


def convert_date(date):
    return datetime(*xldate_as_tuple(float(date), book_date_format))
