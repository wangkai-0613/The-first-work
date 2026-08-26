"""
星座查询功能测试
运行方式: python -m unittest tests.test_zodiac_service -v
"""

import unittest
import sys
import os
from datetime import date, timedelta

# 添加项目根目录到路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from app.services.zodiac_service import (
    get_zodiac_sign,
    get_all_zodiac_signs,
    get_zodiac_date_range,
)


def _shift_date(month: int, day: int, days: int) -> tuple[int, int]:
    """把 (月, 日) 平移指定天数，返回新的 (月, 日)。"""
    shifted = date(2000, month, day) + timedelta(days=days)
    return shifted.month, shifted.day


class TestZodiacService(unittest.TestCase):
    """星座服务测试类"""

    # 十二星座及日期范围（起点月、起点日、终点月、终点日）
    ZODIAC_RANGES = {
        "水瓶座": (1, 20, 2, 18),
        "双鱼座": (2, 19, 3, 20),
        "白羊座": (3, 21, 4, 19),
        "金牛座": (4, 20, 5, 20),
        "双子座": (5, 21, 6, 21),
        "巨蟹座": (6, 22, 7, 22),
        "狮子座": (7, 23, 8, 22),
        "处女座": (8, 23, 9, 22),
        "天秤座": (9, 23, 10, 23),
        "天蝎座": (10, 24, 11, 22),
        "射手座": (11, 23, 12, 21),
        "摩羯座": (12, 22, 1, 19),
    }

    def test_all_zodiac_signs(self):
        """测试获取所有星座的数量与顺序"""
        signs = get_all_zodiac_signs()
        expected_signs = list(self.ZODIAC_RANGES.keys())
        self.assertEqual(len(signs), 12, "应该有12个星座")
        self.assertEqual(signs, expected_signs, "星座名称及顺序应该正确")

    def test_zodiac_boundaries(self):
        """测试各星座边界日期"""
        # 水瓶座 1.20-2.18
        self.assertEqual(get_zodiac_sign(1, 19), "摩羯座")
        self.assertEqual(get_zodiac_sign(1, 20), "水瓶座")
        self.assertEqual(get_zodiac_sign(2, 18), "水瓶座")
        self.assertEqual(get_zodiac_sign(2, 19), "双鱼座")

        # 双鱼座 2.19-3.20
        self.assertEqual(get_zodiac_sign(2, 19), "双鱼座")
        self.assertEqual(get_zodiac_sign(3, 20), "双鱼座")
        self.assertEqual(get_zodiac_sign(3, 21), "白羊座")

        # 白羊座 3.21-4.19
        self.assertEqual(get_zodiac_sign(3, 21), "白羊座")
        self.assertEqual(get_zodiac_sign(4, 19), "白羊座")
        self.assertEqual(get_zodiac_sign(4, 20), "金牛座")

        # 金牛座 4.20-5.20
        self.assertEqual(get_zodiac_sign(4, 20), "金牛座")
        self.assertEqual(get_zodiac_sign(5, 20), "金牛座")
        self.assertEqual(get_zodiac_sign(5, 21), "双子座")

        # 双子座 5.21-6.21
        self.assertEqual(get_zodiac_sign(5, 21), "双子座")
        self.assertEqual(get_zodiac_sign(6, 21), "双子座")
        self.assertEqual(get_zodiac_sign(6, 22), "巨蟹座")

        # 巨蟹座 6.22-7.22
        self.assertEqual(get_zodiac_sign(6, 22), "巨蟹座")
        self.assertEqual(get_zodiac_sign(7, 22), "巨蟹座")
        self.assertEqual(get_zodiac_sign(7, 23), "狮子座")

        # 狮子座 7.23-8.22
        self.assertEqual(get_zodiac_sign(7, 23), "狮子座")
        self.assertEqual(get_zodiac_sign(8, 22), "狮子座")
        self.assertEqual(get_zodiac_sign(8, 23), "处女座")

        # 处女座 8.23-9.22
        self.assertEqual(get_zodiac_sign(8, 23), "处女座")
        self.assertEqual(get_zodiac_sign(9, 22), "处女座")
        self.assertEqual(get_zodiac_sign(9, 23), "天秤座")

        # 天秤座 9.23-10.23
        self.assertEqual(get_zodiac_sign(9, 23), "天秤座")
        self.assertEqual(get_zodiac_sign(10, 23), "天秤座")
        self.assertEqual(get_zodiac_sign(10, 24), "天蝎座")

        # 天蝎座 10.24-11.22
        self.assertEqual(get_zodiac_sign(10, 24), "天蝎座")
        self.assertEqual(get_zodiac_sign(11, 22), "天蝎座")
        self.assertEqual(get_zodiac_sign(11, 23), "射手座")

        # 射手座 11.23-12.21
        self.assertEqual(get_zodiac_sign(11, 23), "射手座")
        self.assertEqual(get_zodiac_sign(12, 21), "射手座")
        self.assertEqual(get_zodiac_sign(12, 22), "摩羯座")

        # 摩羯座 12.22-1.19（跨年）
        self.assertEqual(get_zodiac_sign(12, 22), "摩羯座")
        self.assertEqual(get_zodiac_sign(1, 19), "摩羯座")
        self.assertEqual(get_zodiac_sign(1, 20), "水瓶座")

    def test_all_boundaries_table_driven(self):
        """表驱动：遍历十二星座的首日、末日及相邻日期"""
        signs = list(self.ZODIAC_RANGES.keys())
        for index, sign in enumerate(signs):
            start_month, start_day, end_month, end_day = self.ZODIAC_RANGES[sign]
            prev_sign = signs[index - 1]
            next_sign = signs[(index + 1) % len(signs)]

            with self.subTest(sign=sign, case="首日"):
                self.assertEqual(get_zodiac_sign(start_month, start_day), sign)
            with self.subTest(sign=sign, case="末日"):
                self.assertEqual(get_zodiac_sign(end_month, end_day), sign)

            before_month, before_day = _shift_date(start_month, start_day, -1)
            with self.subTest(sign=sign, case="首日前一天"):
                self.assertEqual(
                    get_zodiac_sign(before_month, before_day), prev_sign)

            after_month, after_day = _shift_date(end_month, end_day, 1)
            with self.subTest(sign=sign, case="末日之后一天"):
                self.assertEqual(
                    get_zodiac_sign(after_month, after_day), next_sign)

    def test_invalid_dates(self):
        """测试无效日期"""
        # 无效月份
        with self.assertRaises(ValueError):
            get_zodiac_sign(0, 1)  # 月份太小
        with self.assertRaises(ValueError):
            get_zodiac_sign(13, 1)  # 月份太大

        # 大月无效日期（1,3,5,7,8,10,12月）
        with self.assertRaises(ValueError):
            get_zodiac_sign(1, 0)   # 日期太小
        with self.assertRaises(ValueError):
            get_zodiac_sign(1, 32)  # 日期太大
        with self.assertRaises(ValueError):
            get_zodiac_sign(3, 0)   # 日期太小
        with self.assertRaises(ValueError):
            get_zodiac_sign(3, 32)  # 日期太大

        # 小月无效日期（4,6,9,11月）
        with self.assertRaises(ValueError):
            get_zodiac_sign(4, 0)   # 日期太小
        with self.assertRaises(ValueError):
            get_zodiac_sign(4, 31)  # 日期太大
        with self.assertRaises(ValueError):
            get_zodiac_sign(6, 0)   # 日期太小
        with self.assertRaises(ValueError):
            get_zodiac_sign(6, 31)  # 日期太大
        with self.assertRaises(ValueError):
            get_zodiac_sign(9, 0)   # 日期太小
        with self.assertRaises(ValueError):
            get_zodiac_sign(9, 31)  # 日期太大
        with self.assertRaises(ValueError):
            get_zodiac_sign(11, 0)  # 日期太小
        with self.assertRaises(ValueError):
            get_zodiac_sign(11, 31)  # 日期太大

        # 2月无效日期（最多29天）
        with self.assertRaises(ValueError):
            get_zodiac_sign(2, 0)   # 日期太小
        with self.assertRaises(ValueError):
            get_zodiac_sign(2, 30)  # 日期太大（2月最多29天）
        with self.assertRaises(ValueError):
            get_zodiac_sign(2, 31)  # 日期太大

    def test_invalid_types(self):
        """测试非法输入类型"""
        with self.assertRaises(ValueError):
            get_zodiac_sign("3", 21)  # 月份为字符串
        with self.assertRaises(ValueError):
            get_zodiac_sign(3, "21")  # 日期为字符串
        with self.assertRaises(ValueError):
            get_zodiac_sign(None, 21)  # 月份为 None
        with self.assertRaises(ValueError):
            get_zodiac_sign(3, None)  # 日期为 None
        with self.assertRaises(ValueError):
            get_zodiac_sign(True, 21)  # 布尔值不是合法整数
        with self.assertRaises(ValueError):
            get_zodiac_sign(3, False)  # 布尔值不是合法整数

    def test_get_zodiac_date_range(self):
        """测试全部星座的日期范围"""
        for sign, expected in self.ZODIAC_RANGES.items():
            with self.subTest(sign=sign):
                self.assertEqual(get_zodiac_date_range(sign), expected)

        # 测试不存在的星座
        with self.assertRaises(ValueError):
            get_zodiac_date_range("不存在星座")

    def test_edge_cases(self):
        """测试边界情况"""
        # 年末年初的边界
        self.assertEqual(get_zodiac_sign(12, 31), "摩羯座")
        self.assertEqual(get_zodiac_sign(1, 1), "摩羯座")
        self.assertEqual(get_zodiac_sign(1, 19), "摩羯座")
        self.assertEqual(get_zodiac_sign(1, 20), "水瓶座")

    def test_february_dates(self):
        """测试2月日期处理"""
        # 2月有效日期
        self.assertEqual(get_zodiac_sign(2, 1), "水瓶座")   # 2月1日是水瓶座
        self.assertEqual(get_zodiac_sign(2, 18), "水瓶座")  # 2月18日是水瓶座
        self.assertEqual(get_zodiac_sign(2, 19), "双鱼座")  # 2月19日是双鱼座
        self.assertEqual(get_zodiac_sign(2, 29), "双鱼座")  # 2月29日是双鱼座

    def test_month_day_limits(self):
        """测试各月份的日期限制"""
        # 大月（31天）- 验证能正常查询到正确的星座
        valid_large_months = {
            1: "水瓶座",   # 1月31日是水瓶座
            3: "白羊座",   # 3月31日是白羊座
            5: "双子座",   # 5月31日是双子座
            7: "狮子座",   # 7月31日是狮子座
            8: "处女座",   # 8月31日是处女座
            10: "天蝎座",  # 10月31日是天蝎座
            12: "摩羯座",  # 12月31日是摩羯座
        }

        for month, expected_sign in valid_large_months.items():
            result = get_zodiac_sign(month, 31)
            self.assertEqual(result, expected_sign,
                             f"{month}月31日应该是{expected_sign}，实际是{result}")

        # 小月（30天）- 验证能正常查询到正确的星座
        valid_small_months = {
            4: "金牛座",   # 4月30日是金牛座
            6: "巨蟹座",   # 6月30日是巨蟹座
            9: "天秤座",   # 9月30日是天秤座
            11: "射手座",  # 11月30日是射手座
        }

        for month, expected_sign in valid_small_months.items():
            result = get_zodiac_sign(month, 30)
            self.assertEqual(result, expected_sign,
                             f"{month}月30日应该是{expected_sign}，实际是{result}")
            with self.assertRaises(ValueError):
                get_zodiac_sign(month, 31)  # 小月没有31日

        # 2月（29天）
        self.assertEqual(get_zodiac_sign(2, 29), "双鱼座",
                         "2月29日应该是双鱼座")
        with self.assertRaises(ValueError):
            get_zodiac_sign(2, 30)  # 2月没有30日
        with self.assertRaises(ValueError):
            get_zodiac_sign(2, 31)  # 2月没有31日


if __name__ == '__main__':
    unittest.main()