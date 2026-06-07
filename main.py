#!/usr/bin/env python3
"""
Pico y Placa Predictor — CLI
Usage:
    python main.py
    python main.py --plate PBX-1234 --date 2024-03-19 --time 08:00
"""
import argparse
import sys
from datetime import datetime

from pico_placa.services.pico_placa_checker import PicoPlacaChecker
from pico_placa.services.pico_placa_schedule import PicoPlacaSchedule
from pico_placa.value_objects.license_plate import LicensePlate

DATE_FORMAT = "%Y-%m-%d"
TIME_FORMAT = "%H:%M"
DATETIME_FORMAT = f"{DATE_FORMAT} {TIME_FORMAT}"

GREEN  = "\033[92m"
RED    = "\033[91m"
YELLOW = "\033[93m"
BOLD   = "\033[1m"
RESET  = "\033[0m"


def build_checker() -> PicoPlacaChecker:
    return PicoPlacaChecker(PicoPlacaSchedule())


def parse_datetime(date_str: str, time_str: str) -> datetime:
    try:
        return datetime.strptime(f"{date_str} {time_str}", DATETIME_FORMAT)
    except ValueError:
        print(f"{RED}Invalid date or time format.{RESET}")
        print(f"  Date must be YYYY-MM-DD  (e.g. 2024-03-19)")
        print(f"  Time must be HH:MM 24h   (e.g. 08:00)")
        sys.exit(1)


def parse_plate(plate_str: str) -> LicensePlate:
    try:
        return LicensePlate(plate_str)
    except ValueError as e:
        print(f"{RED}Invalid plate: {e}{RESET}")
        sys.exit(1)


def display_result(result) -> None:
    color  = RED if result.restricted else GREEN
    status = "Restringido" if result.restricted else "Permitido"

    print()
    print(f"{BOLD}{'─' * 48}{RESET}")
    print(f"  Plate : {BOLD}{result.plate}{RESET}")
    print(f"  Date  : {result.date}")
    print(f"  Time  : {result.time}")
    print(f"  Result: {color}{BOLD}{status}{RESET}")
    print(f"  {result.message}")
    print(f"{BOLD}{'─' * 48}{RESET}")
    print()


def interactive_mode(checker: PicoPlacaChecker) -> None:
    print(f"\n{BOLD}{'═' * 48}")
    print("   Pico y Placa Predictor — Quito")
    print(f"{'═' * 48}{RESET}\n")

    plate_str = input(f"  {YELLOW}License plate{RESET} (e.g. PBX-1234) : ").strip()
    date_str  = input(f"  {YELLOW}Date{RESET}          (YYYY-MM-DD)    : ").strip()
    time_str  = input(f"  {YELLOW}Time{RESET}          (HH:MM 24h)     : ").strip()

    plate  = parse_plate(plate_str)
    moment = parse_datetime(date_str, time_str)
    result = checker.check(plate, moment)

    display_result(result)


def cli_mode(checker: PicoPlacaChecker, args: argparse.Namespace) -> None:
    plate  = parse_plate(args.plate)
    moment = parse_datetime(args.date, args.time)
    result = checker.check(plate, moment)
    display_result(result)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Pico y Placa Predictor for Quito, Ecuador."
    )
    parser.add_argument("--plate", help="License plate, e.g. PBX-1234")
    parser.add_argument("--date",  help="Date in YYYY-MM-DD format")
    parser.add_argument("--time",  help="Time in HH:MM 24h format")

    args = parser.parse_args()

    checker = build_checker()

    if args.plate and args.date and args.time:
        cli_mode(checker, args)
    else:
        interactive_mode(checker)


if __name__ == "__main__":
    main()
