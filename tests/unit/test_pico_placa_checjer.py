import unittest
from datetime import datetime

from pico_placa.services.pico_placa_checker import PicoPlacaChecker
from pico_placa.services.pico_placa_schedule import PicoPlacaSchedule
from pico_placa.value_objects.license_plate import LicensePlate


def dt(date_str: str, time_str: str) -> datetime:
    return datetime.strptime(f"{date_str} {time_str}", "%Y-%m-%d %H:%M")


# 2024-03-18 = Monday | 2024-03-19 = Tuesday  | 2024-03-20 = Wednesday
# 2024-03-21 = Thursday | 2024-03-22 = Friday
# 2024-03-23 = Saturday | 2024-03-24 = Sunday


class TestRestrictedCases(unittest.TestCase):
    def setUp(self):
        self.checker = PicoPlacaChecker(PicoPlacaSchedule())

    def _assert_restricted(self, plate, date, time_str):
        result = self.checker.is_restricted(LicensePlate(plate), dt(date, time_str))
        self.assertTrue(result, f"{plate} on {date} {time_str} should be RESTRICTED")

    def _assert_free(self, plate, date, time_str):
        result = self.checker.is_restricted(LicensePlate(plate), dt(date, time_str))
        self.assertFalse(result, f"{plate} on {date} {time_str} should be FREE")

    def test_digit_1_monday_morning(self):      self._assert_restricted("ABC-1001", "2024-03-18", "08:00")
    def test_digit_2_monday_morning(self):      self._assert_restricted("ABC-1002", "2024-03-18", "07:00")
    def test_digit_3_tuesday_morning(self):     self._assert_restricted("ABC-1003", "2024-03-19", "09:00")
    def test_digit_4_tuesday_morning(self):     self._assert_restricted("ABC-1004", "2024-03-19", "07:30")
    def test_digit_5_wednesday_boundary(self):  self._assert_restricted("ABC-1005", "2024-03-20", "09:30")
    def test_digit_6_wednesday_afternoon(self): self._assert_restricted("ABC-1006", "2024-03-20", "16:00")
    def test_digit_7_thursday_afternoon(self):  self._assert_restricted("ABC-1007", "2024-03-21", "18:00")
    def test_digit_8_thursday_boundary(self):   self._assert_restricted("ABC-1008", "2024-03-21", "19:30")
    def test_digit_9_friday_afternoon(self):    self._assert_restricted("ABC-1009", "2024-03-22", "17:00")
    def test_digit_0_friday_afternoon(self):    self._assert_restricted("ABC-1230", "2024-03-22", "16:30")

    def test_correct_day_outside_window(self):  self._assert_free("ABC-1001", "2024-03-18", "10:00")
    def test_correct_day_before_morning(self):  self._assert_free("ABC-1002", "2024-03-18", "06:59")
    def test_correct_day_before_afternoon(self):self._assert_free("ABC-1005", "2024-03-20", "15:59")
    def test_correct_day_after_afternoon(self): self._assert_free("ABC-1009", "2024-03-22", "19:31")
    def test_wrong_day(self):                   self._assert_free("ABC-1001", "2024-03-19", "08:00")
    def test_another_wrong_day(self):           self._assert_free("ABC-1003", "2024-03-18", "08:00")
    def test_saturday_is_free(self):            self._assert_free("ABC-1001", "2024-03-23", "08:00")
    def test_sunday_is_free(self):              self._assert_free("ABC-1005", "2024-03-24", "17:00")


class TestCheckResult(unittest.TestCase):
    def setUp(self):
        self.checker = PicoPlacaChecker(PicoPlacaSchedule())

    def test_restricted_result_has_cannot_message(self):
        result = self.checker.check(LicensePlate("PBX-1234"), dt("2024-03-19", "08:00"))
        self.assertTrue(result.restricted)
        self.assertIn("CANNOT", result.message)
        self.assertEqual(result.plate, "PBX-1234")

    def test_unrestricted_result_has_can_message(self):
        result = self.checker.check(LicensePlate("PBX-1234"), dt("2024-03-19", "12:00"))
        self.assertFalse(result.restricted)
        self.assertIn("CAN", result.message)
        self.assertNotIn("CANNOT", result.message)


if __name__ == "__main__":
    unittest.main()
