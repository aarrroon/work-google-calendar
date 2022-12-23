
from project import *


class TestPayslip:
    payslip_dates = list_payslip_dates()
    p1 = PaySlip(list_payslip_dates()[0])
    p2 = PaySlip(list_payslip_dates()[1])

    def test_extract_hours(self):
        assert self.p1.extract_hours() == {'ordinary': 20.0, 'saturday': 7.5, 'sunday': 5.0, 'evening': 4.0, 'publicHoliday': 0}
        assert self.p2.extract_hours() == {'ordinary': 15.0, 'saturday': 15.0, 'sunday': 7.5, 'evening': 8.0, 'publicHoliday': 0}


    def test_add_shifts(self):
        assert self.p1.add_shifts()[0] == self.p1.add_shifts()[0]

    def test_calculate_pay(self):
        assert self.p1.calculate_pay() == {'tax': 78, 'gross_income': 965.89}
        assert self.p2.calculate_pay() == {'tax': 151, 'gross_income': 1220.06}

    def test_print_pay(self):
        assert self.p1.print_pay() == 'Gross Income: $965.89 and Tax is $78.00'
        assert self.p2.print_pay() == 'Gross Income: $1220.06 and Tax is $151.00'


def test_print_shifts(capsys):
    assert True


def test_list_payslip_dates():
    assert list_payslip_dates() == ['2022-05-15', '2022-05-29', '2022-06-12', '2022-06-26', '2022-07-10', '2022-07-24', '2022-08-07', '2022-08-21', '2022-09-04', '2022-09-18']


def test_calculate_tax():
    assert calculate_tax(300) == {'tax': 0, 'gross_income': 300}
    assert calculate_tax(1000) == {'tax': 65, 'gross_income': 935}
