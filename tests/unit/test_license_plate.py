import unittest

from pico_placa.value_objects.license_plate import LicensePlate


class TestLicensePlate(unittest.TestCase):

    def test_valid_plate_is_accepted(self):
        plate = LicensePlate("PBX-1234")
        self.assertEqual(plate.plate, "PBX-1234")

    def test_lowercase_is_normalized(self):
        plate = LicensePlate("pbx-1234")
        self.assertEqual(plate.plate, "PBX-1234")

    def test_last_digit_is_extracted(self):
        self.assertEqual(LicensePlate("ABC-1234").last_digit, 4)

    def test_last_digit_zero(self):
        self.assertEqual(LicensePlate("ABC-1230").last_digit, 0)

    def test_str_returns_plate(self):
        self.assertEqual(str(LicensePlate("ABC-1234")), "ABC-1234")

    def test_invalid_reversed_format(self):
        with self.assertRaises(ValueError):
            LicensePlate("1234-PBX")

    def test_invalid_no_dash(self):
        with self.assertRaises(ValueError):
            LicensePlate("PBX1234")

    def test_invalid_two_letters(self):
        with self.assertRaises(ValueError):
            LicensePlate("PB-1234")

    def test_invalid_three_digits(self):
        with self.assertRaises(ValueError):
            LicensePlate("PBX-123")

    def test_invalid_five_digits(self):
        with self.assertRaises(ValueError):
            LicensePlate("PBX-12345")

    def test_invalid_empty_string(self):
        with self.assertRaises(ValueError):
            LicensePlate("")

    def test_invalid_wrong_separator(self):
        with self.assertRaises(ValueError):
            LicensePlate("PBX_1234")


if __name__ == "__main__":
    unittest.main()
