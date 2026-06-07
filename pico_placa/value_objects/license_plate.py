import re


class LicensePlate:
    PATTERN = re.compile(r'^[A-Z]{3}-\d{4}$')

    def __init__(self, plate: str) -> None:
        self._plate = plate.strip().upper()
        self._validate()

    def _validate(self) -> None:
        if not self.PATTERN.match(self._plate):
            raise ValueError(
                f"Invalid license plate format. Expected ABC-1234, got: '{self._plate}'"
            )

    @property
    def plate(self) -> str:
        return self._plate

    @property
    def last_digit(self) -> int:
        return int(self._plate[-1])

    def __str__(self) -> str:
        return self._plate

    def __repr__(self) -> str:
        return f"LicensePlate('{self._plate}')"
