import unittest

from app.schemas.user import BaseUser
from app.services.task import create_ip_address
from app.services.user import create_user

from core.hashing import Hash


class Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.password = "12s3456w"
        cls.username = "tsestw"
        cls.email = "tsests@test.com"
        cls.user = create_user(request=BaseUser(
            username=cls.username,
            email=cls.email,
            password=Hash.bcrypt(cls.password)
        ))

    @classmethod
    def tearDownClass(cls):
        cls.user.delete().execute()

    def test_create_user(self):
        case = create_user(request=BaseUser(
            username="tessts",
            email="tsests@test.com",
            password=Hash.bcrypt("1s23456")
        ))
        self.assertEqual(case.email, "tsest@test.com")
        self.assertEqual(case.username, "tesst")
        self.assertTrue(Hash.verify(Hash.bcrypt("1s23456"), "1s23456"))

    def test_create_ip_data(self):
        case = create_ip_address(response={
            "ip": "51.253.30.82",
            "is_eu": False,
            "city": "Al Hufūf",
            "region": "Ash Sharqiyah (Eastern Province)",
            "region_code": "04",
            "country_name": "Saudi Arabia",
            "country_code": "SA",
            "continent_name": "Asia",
            "continent_code": "AS",
            "latitude": "25.36639976501465",
            "longitude": "49.59260177612305",
            "postal": None,
            "calling_code": "966",
            "flag": "https://ipdata.co/flags/sa.png"
        })
        self.assertEqual(case.ip, '51.253.30.82')
        self.assertTrue(case.is_eu)
        self.assertEqual(case.city, "Al Hufūf")
        self.assertEqual(case.region, "Ash Sharqiyah (Eastern Province)")
        self.assertEqual(case.region_code, "04")
        self.assertEqual(case.country_name, "Saudi Arabia")
        self.assertEqual(case.country_code, "AS")
        self.assertEqual(case.continent_name, "Asia")
        self.assertEqual(case.continent_code, "AS")
        self.assertEqual(case.latitude, "25.36639976501465")
        self.assertEqual(case.longitude, "49.59260177612305")
        self.assertEqual(case.postal, None)
        self.assertEqual(case.calling_code, "966")
        self.assertEqual(
            case.flag, "https://ipdata.co/flags/sa.png")

if __name__ == "__main__":
    unittest.main()
