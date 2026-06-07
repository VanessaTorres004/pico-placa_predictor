from datetime import datetime

from pico_placa.enums.day_of_week import DayOfWeek
from pico_placa.services.check_result import CheckResult
from pico_placa.services.pico_placa_schedule import PicoPlacaSchedule
from pico_placa.value_objects.license_plate import LicensePlate


class PicoPlacaChecker:
    def __init__(self, schedule: PicoPlacaSchedule) -> None:
        self._schedule = schedule

    def is_exempt_vehicle(self, plate: LicensePlate) -> bool:
        """

Future implementations of exemption rules for certain types of vehicles.

Examples:

- Electric or hybrid vehicles

- Emergency vehicles (ambulances, fire trucks, police cars)

- Official vehicles (government, diplomatic vehicles)

- Vehicles for people with disabilities
"""
        return False

    def is_restricted(self, plate: LicensePlate, dt: datetime) -> bool:

        # futras implementaciones de reglas de exención para ciertos tipos de vehículos.
        if self.is_exempt_vehicle(plate):
            return False

        day = DayOfWeek(dt.isoweekday())

        # No hay pico y placa los fines de semana
        if day.is_weekend():
            return False

        
        if not self._schedule.is_restricted_day(
            plate.last_digit,
            day
        ):
            return False

        
        return self._schedule.is_within_restricted_window(
            dt.time()
        )

    def check(
        self,
        plate: LicensePlate,
        dt: datetime
    ) -> CheckResult:

        restricted = self.is_restricted(plate, dt)

        return CheckResult.build(
            str(plate),
            dt,
            restricted
        )