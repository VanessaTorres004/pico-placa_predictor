from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class CheckResult:
    plate:      str
    date:       str
    time:       str
    restricted: bool
    message:    str

    @classmethod
    def build(cls, plate: str, dt: datetime, restricted: bool) -> "CheckResult":
        status = "CANNOT be on the road" if restricted else "CAN be on the road"
        return cls(
            plate=plate,
            date=dt.strftime("%Y-%m-%d"),
            time=dt.strftime("%H:%M"),
            restricted=restricted,
            message=f"The vehicle with plate {plate} {status} at {dt.strftime('%H:%M')} on {dt.strftime('%A, %B %-d %Y')}.",
        )
