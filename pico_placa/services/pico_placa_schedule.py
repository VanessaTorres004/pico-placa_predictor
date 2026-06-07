from datetime import time

from pico_placa.enums.day_of_week import DayOfWeek


class PicoPlacaSchedule:
    

    _DIGIT_TO_DAY: dict[int, DayOfWeek] = {
        1: DayOfWeek.MONDAY,
        2: DayOfWeek.MONDAY,
        3: DayOfWeek.TUESDAY,
        4: DayOfWeek.TUESDAY,
        5: DayOfWeek.WEDNESDAY,
        6: DayOfWeek.WEDNESDAY,
        7: DayOfWeek.THURSDAY,
        8: DayOfWeek.THURSDAY,
        9: DayOfWeek.FRIDAY,
        0: DayOfWeek.FRIDAY,
    }

    _RESTRICTED_WINDOWS: list[tuple[time, time]] = [
        (time(7, 0),  time(9, 30)),   # 07:00 – 09:30
        (time(16, 0), time(19, 30)),  # 16:00 – 19:30
    ]

    def restricted_day_for(self, last_digit: int) -> DayOfWeek:
        return self._DIGIT_TO_DAY[last_digit]

    def is_restricted_day(self, last_digit: int, day: DayOfWeek) -> bool:
        return self.restricted_day_for(last_digit) == day

    def is_within_restricted_window(self, t: time) -> bool:
        return any(start <= t <= end for start, end in self._RESTRICTED_WINDOWS)
