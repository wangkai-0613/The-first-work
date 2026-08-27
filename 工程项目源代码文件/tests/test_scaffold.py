"""项目框架的基础测试。"""

import unittest

from app.models.user_profile import UserProfile


class ScaffoldTests(unittest.TestCase):
    def test_profile_without_year_has_no_full_date(self) -> None:
        profile = UserProfile(birth_month=8, birth_day=17)
        self.assertIsNone(profile.full_birth_date())

    def test_profile_with_year_builds_date(self) -> None:
        profile = UserProfile(birth_year=2005, birth_month=8, birth_day=17)
        self.assertEqual(profile.full_birth_date().isoformat(), "2005-08-17")


if __name__ == "__main__":
    unittest.main()

