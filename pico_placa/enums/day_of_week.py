from enum import Enum


class DayOfWeek(Enum):
    MONDAY = 1
    TUESDAY = 2
    WEDNESDAY = 3
    THURSDAY = 4
    FRIDAY = 5
    SATURDAY = 6
    SUNDAY = 7

    def is_weekend(self) -> bool:
        return self in (DayOfWeek.SATURDAY, DayOfWeek.SUNDAY)

    def restricted_digits(self) -> tuple[int, ...]:
        restrictions = {
            DayOfWeek.MONDAY: (1, 2),
            DayOfWeek.TUESDAY: (3, 4),
            DayOfWeek.WEDNESDAY: (5, 6),
            DayOfWeek.THURSDAY: (7, 8),
            DayOfWeek.FRIDAY: (9, 0),
        }

        return restrictions.get(self, ())

    def has_restriction(self, plate_last_digit: int) -> bool:
        return plate_last_digit in self.restricted_digits()