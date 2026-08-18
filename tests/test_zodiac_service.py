"""
星座查询功能测试
运行方式: python -m unittest tests.test_zodiac_service -v
"""

import unittest
import sys
import os

# 添加项目根目录到路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from app.services.zodiac_service import get_zodiac_sign, get_all_zodiac_signs, get_zodiac_date_range


class TestZodiacService(unittest.TestCase):
    """星座服务测试类"""
    
    def test_all_zodiac_signs(self):
        """测试获取所有星座"""
        signs = get_all_zodiac_signs()
        expected_signs = [
            "水瓶座", "双鱼座", "白羊座", "金牛座", "双子座", "巨蟹座",
            "狮子座", "处女座", "天秤座", "天蝎座", "射手座", "摩羯座"
        ]
        self.assertEqual(len(signs), 12, "应该有12个星座")
        self.assertEqual(set(signs), set(expected_signs), "星座名称应该正确")
    
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
    
    def test_get_zodiac_date_range(self):
        """测试获取星座日期范围"""
        # 测试几个星座
        self.assertEqual(get_zodiac_date_range("水瓶座"), (1, 20, 2, 18))
        self.assertEqual(get_zodiac_date_range("白羊座"), (3, 21, 4, 19))
        self.assertEqual(get_zodiac_date_range("摩羯座"), (12, 22, 1, 19))
        
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
        
        # 各星座的第一天和最后一天
        test_cases = [
            (1, 20, "水瓶座"),   # 水瓶座第一天
            (2, 18, "水瓶座"),   # 水瓶座最后一天
            (3, 21, "白羊座"),   # 白羊座第一天
            (4, 19, "白羊座"),   # 白羊座最后一天
            (12, 22, "摩羯座"),  # 摩羯座第一天
            (1, 19, "摩羯座"),   # 摩羯座最后一天
        ]
        
        for month, day, expected_sign in test_cases:
            with self.subTest(month=month, day=day):
                self.assertEqual(get_zodiac_sign(month, day), expected_sign,
                               f"{month}月{day}日应该是{expected_sign}")
    
    def test_february_dates(self):
        """测试2月日期处理"""
        # 2月有效日期
        self.assertEqual(get_zodiac_sign(2, 1), "水瓶座")   # 2月1日是水瓶座
        self.assertEqual(get_zodiac_sign(2, 18), "水瓶座")  # 2月18日是水瓶座
        self.assertEqual(get_zodiac_sign(2, 19), "双鱼座")  # 2月19日是双鱼座
        self.assertEqual(get_zodiac_sign(2, 29), "双鱼座")  # 2月29日是双鱼座
        
        # 2月无效日期已经在test_invalid_dates中测试
        
    def test_month_day_limits(self):
        """测试各月份的日期限制"""
        # 大月（31天）
        valid_large_months = [1, 3, 5, 7, 8, 10, 12]
        for month in valid_large_months:
            self.assertEqual(get_zodiac_sign(month, 31), "星座查询应该成功")
        
        # 小月（30天）
        valid_small_months = [4, 6, 9, 11]
        for month in valid_small_months:
            self.assertEqual(get_zodiac_sign(month, 30), "星座查询应该成功")
            with self.assertRaises(ValueError):
                get_zodiac_sign(month, 31)  # 小月没有31日
        
        # 2月（29天）
        self.assertEqual(get_zodiac_sign(2, 29), "星座查询应该成功")
        with self.assertRaises(ValueError):
            get_zodiac_sign(2, 30)  # 2月没有30日
        with self.assertRaises(ValueError):
            get_zodiac_sign(2, 31)  # 2月没有31日


if __name__ == '__main__':
    unittest.main()