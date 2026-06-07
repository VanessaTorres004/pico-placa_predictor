from enum import Enum


class DayOfWeek(Enum):
    MONDAY    = 1
    TUESDAY   = 2
    WEDNESDAY = 3
    THURSDAY  = 4
    FRIDAY    = 5
    SATURDAY  = 6
    SUNDAY    = 7

    def is_weekend(self) -> bool:
        return self in (DayOfWeek.SATURDAY, DayOfWeek.SUNDAY)

    def label(self) -> str:
        return self.name.capitalize()