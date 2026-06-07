import unittest
from datetime import time

from pico_placa.enums.day_of_week import DayOfWeek
from pico_placa.services.pico_placa_schedule import PicoPlacaSchedule


class TestDigitToDay(unittest.TestCase):
    def setUp(self):
        self.schedule = PicoPlacaSchedule()

    def _assert_digit_maps_to(self, digit, expected_day):
        self.assertEqual(self.schedule.restricted_day_for(digit), expected_day)

    def test_digit_1_maps_to_monday(self):    self._assert_digit_maps_to(1, DayOfWeek.MONDAY)
    def test_digit_2_maps_to_monday(self):    self._assert_digit_maps_to(2, DayOfWeek.MONDAY)
    def test_digit_3_maps_to_tuesday(self):   self._assert_digit_maps_to(3, DayOfWeek.TUESDAY)
    def test_digit_4_maps_to_tuesday(self):   self._assert_digit_maps_to(4, DayOfWeek.TUESDAY)
    def test_digit_5_maps_to_wednesday(self): self._assert_digit_maps_to(5, DayOfWeek.WEDNESDAY)
    def test_digit_6_maps_to_wednesday(self): self._assert_digit_maps_to(6, DayOfWeek.WEDNESDAY)
    def test_digit_7_maps_to_thursday(self):  self._assert_digit_maps_to(7, DayOfWeek.THURSDAY)
    def test_digit_8_maps_to_thursday(self):  self._assert_digit_maps_to(8, DayOfWeek.THURSDAY)
    def test_digit_9_maps_to_friday(self):    self._assert_digit_maps_to(9, DayOfWeek.FRIDAY)
    def test_digit_0_maps_to_friday(self):    self._assert_digit_maps_to(0, DayOfWeek.FRIDAY)


class TestRestrictedWindows(unittest.TestCase):
    def setUp(self):
        self.schedule = PicoPlacaSchedule()

    def _assert_restricted(self, h, m):
        self.assertTrue(self.schedule.is_within_restricted_window(time(h, m)))

    def _assert_free(self, h, m):
        self.assertFalse(self.schedule.is_within_restricted_window(time(h, m)))

    # Morning window 07:00 – 09:30
    def test_morning_window_start(self):       self._assert_restricted(7, 0)
    def test_morning_window_middle(self):      self._assert_restricted(8, 0)
    def test_morning_window_end(self):         self._assert_restricted(9, 30)
    def test_before_morning_window(self):      self._assert_free(6, 59)
    def test_after_morning_window(self):       self._assert_free(9, 31)

    # Afternoon window 16:00 – 19:30
    def test_afternoon_window_start(self):     self._assert_restricted(16, 0)
    def test_afternoon_window_middle(self):    self._assert_restricted(18, 0)
    def test_afternoon_window_end(self):       self._assert_restricted(19, 30)
    def test_before_afternoon_window(self):    self._assert_free(15, 59)
    def test_after_afternoon_window(self):     self._assert_free(19, 31)

    # Outside both
    def test_midday_is_free(self):             self._assert_free(12, 0)
    def test_midnight_is_free(self):           self._assert_free(0, 0)


if __name__ == "__main__":
    unittest.main()
