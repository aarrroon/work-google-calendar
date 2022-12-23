"""
External Packages:
- holidays
- Google Calendar Simple API (gcsa)
-
Built-in Packages:
- datetime
- math
- re
- parser
"""
from gcsa.google_calendar import GoogleCalendar
from gcsa.event import Event
import holidays

from typing import Union
from math import floor
import re
from datetime import datetime, timedelta, date
import argparse


class PaySlip:
    def __init__(self, end_date):
        self.end_date = end_date
        self.shifts = self.add_shifts()
        self.hours = self.extract_hours()
        self.pay = self.calculate_pay()

    def extract_hours(self):
        # output
        payslip_hours = {
            'ordinary': 0,
            'saturday': 0,
            'sunday': 0,
            'evening': 0,
            'publicHoliday': 0
        }
        curr_year = datetime.now().year
        holidays_list = holidays.country_holidays('AU', subdiv='VIC', years=curr_year, expand=False)
        for shift in self.shifts:
            # calculate how long the shift was
            duration = shift.end - shift.start
            seconds_in_hour = 60 * 60
            shift_hours = duration.total_seconds() / seconds_in_hour
            if shift_hours == 8:
                shift_hours = 7.5

            # when evening pay starts
            evening_pay_time = datetime(shift.end.year, shift.end.month, shift.end.day, hour=18,
                                        tzinfo=shift.end.tzinfo)

            # if shift is during public holiday
            if shift.end.date() in holidays_list:
                payslip_hours['publicHoliday'] += shift_hours
            # if shift is on Saturday
            elif shift.end.date().weekday() == 5:
                payslip_hours['saturday'] += shift_hours
            # if shift is on Sunday
            elif shift.end.date().weekday() == 6:
                payslip_hours['sunday'] += shift_hours
            # if shift is in the evening on a weekday
            elif shift.end.hour > evening_pay_time.hour >= shift.start.hour:
                payslip_hours['evening'] += (shift.end - evening_pay_time).total_seconds() / seconds_in_hour
            # else if shift is the basic pay
            else:
                payslip_hours['ordinary'] += shift_hours
        return payslip_hours

    def add_shifts(self):
        fortnight = timedelta(days=14)
        end_date = datetime.fromisoformat(self.end_date)
        start_date = end_date + timedelta(days=1) - fortnight

        calendar = GoogleCalendar(credentials_path='credentials.json')
        events_in_week = calendar.get_events(start_date, end_date + timedelta(days=1), order_by='updated')
        # updates shift attribute in PaySlip
        return [event for event in events_in_week if event.summary == "IKEA"]

    def calculate_pay(self) -> dict[str, Union[int, float]]:
        pay = {
            'ordinary': 24.93,
            'sunday': 37.39,
            'saturday': 31.16,
            'evening': 31.16,
            'publicHoliday': 56.09
        }
        total_income = pay['ordinary'] * self.hours['ordinary'] + \
                       self.hours['sunday'] * pay['sunday'] + \
                       self.hours['saturday'] * pay['saturday'] + \
                       self.hours['evening'] * pay['evening'] + \
                       self.hours['publicHoliday'] * pay['publicHoliday']
        return calculate_tax(total_income)

    def print_pay(self):
        return f"Gross Income: ${self.pay['gross_income']:02} and Tax is ${self.pay['tax']}.00"


def add_calendar_shifts():
    shifts_to_add = []
    while True:
        user_input = input('Input date, start time and duration like: "YYYY-MM-DD, HHMM, 8" (or 9:00AM) ["n" if done]\n')
        if user_input.lower() == 'n':
            break
        if match := re.search(r"^(\d{4})-(\d{2})-(\d{2}), (\d\d)(\d\d), (\d)$", user_input):
            print('Shift is valid')
            shift_year, shift_month, shift_day = int(match.group(1)), int(match.group(2)), int(match.group(3))
            shift_hour, shift_min, shift_length = int(match.group(4)), int(match.group(5)), int(match.group(6))
            start_time = datetime(shift_year, shift_month, shift_day, hour=shift_hour, minute=shift_min)
            end_time = start_time + timedelta(hours=shift_length)
            event = Event('IKEA', start=start_time, end=end_time)
            shifts_to_add.append(event)
            print_shifts([event])

    # Confirm shifts are correct
    print_shifts(shifts_to_add)
    if not shifts_to_add:
        print('No shifts were inputted')
    elif input('Confirm the shifts are correct ("y")\n').lower().strip() != 'y':
        return "No shifts were added"

    # Add shifts to calendar
    calendar = GoogleCalendar(credentials_path='credentials.json')
    for event in shifts_to_add:
        calendar.add_event(event)

    print(f"Number of shifts added is {len(shifts_to_add)}")


def print_shifts(shifts):
    for shift in shifts:
        start_time = f"{shift.start.hour}:{shift.start.minute:02}"
        end_time = f"{shift.end.hour}:{shift.end.minute:02}"
        date = shift.start.date().isoformat()
        days_of_week = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        print(f"{date} - {start_time} to {end_time} on a {days_of_week[shift.start.weekday()]}")
    print()

# Base date needs to be a sunday two fortnights from the 15th of May 2022
def list_payslip_dates(base_date = '2022-10-30'):
    base = date.fromisoformat(base_date)
    output = []
    for i in range(10):
        interval = timedelta(days=14 * i)
        output.append((base + interval).isoformat())
    return output


def find_current_payslip():
    today = date.today()

    for possible_date in list_payslip_dates():
        if (date.fromisoformat(possible_date) - today).total_seconds() > 0:
            return possible_date


def calculate_tax(fortnightly_income: float):
    """
    Calculates the tax withheld and income after tax
    :param fortnightly_income:
    :return: tuple where (tax withheld, income after tax)
    """
    # Australian Tax Table for 2021-2022
    global a, b
    tax_table = {
        359: [0, 0],
        438: [0.19, 68.3462],
        548: [0.29, 112.1942],
        721: [0.21, 68.3465],
        865: [0.2190, 74.8369],
        1282: [0.3477, 186.2119]
    }
    weekly_income = fortnightly_income / 2

    # calculating coefficients for different income brackets
    if weekly_income < 359:
        a, b = tax_table[359]
    elif weekly_income < 438:
        a, b = tax_table[438]
    elif weekly_income < 548:
        a, b = tax_table[548]
    elif weekly_income < 721:
        a, b = tax_table[721]
    elif weekly_income < 865:
        a, b = tax_table[865]
    elif weekly_income < 1282:
        a, b = tax_table[1282]
    # tax withheld in a fortnight
    tax_withheld = floor((a * weekly_income - b) * 2)
    return {'tax': tax_withheld, 'gross_income': round(fortnightly_income - tax_withheld, 2)}


def main():
    # Obtaining arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('--shifts', action='store_true')
    parser.add_argument('--pay', action='store_true')
    parser.add_argument('--add', action='store_true')
    parser.add_argument('--hours', action='store_true')
    parser.add_argument('--payslip_date', action='store_true')
    args = parser.parse_args()

    # Finding the payslip of the current period
    curr_payslip = PaySlip(find_current_payslip())

    # Obtaining which payslip to analyse
    if args.payslip_date:
        print(list_payslip_dates())

    if not args.add:
        while True:
            date_input = input("Input payslip date in the format YYYY-MM-DD (leave empty to use current payslip)\n")
            if match := re.search(r"^((\d{4})-(\d{2})-(\d{2}))$", date_input):
                curr_payslip = PaySlip(match.group(1))
                break
            elif not date_input:
                print(f'This is for the payslip ending on {curr_payslip.end_date}')
                break

    # Print shifts
    if args.shifts:
        print_shifts(curr_payslip.shifts)
    # Display pay
    if args.pay:
        print(curr_payslip.print_pay())
    # Add shifts to calendar
    if args.add:
        add_calendar_shifts()
    # Show the hours of the payslip
    if args.hours:
        print(curr_payslip.hours)



if __name__ == '__main__':
    main()

