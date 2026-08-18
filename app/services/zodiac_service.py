"""星座查询接口，由星座查询负责人实现。"""

# 星座日期边界数据结构（按月份顺序）
ZODIAC_BOUNDARIES = [
    # 水瓶座 1.20-2.18
    {"name": "水瓶座", "start_month": 1, "start_day": 20, "end_month": 2, "end_day": 18},
    # 双鱼座 2.19-3.20
    {"name": "双鱼座", "start_month": 2, "start_day": 19, "end_month": 3, "end_day": 20},
    # 白羊座 3.21-4.19
    {"name": "白羊座", "start_month": 3, "start_day": 21, "end_month": 4, "end_day": 19},
    # 金牛座 4.20-5.20
    {"name": "金牛座", "start_month": 4, "start_day": 20, "end_month": 5, "end_day": 20},
    # 双子座 5.21-6.21
    {"name": "双子座", "start_month": 5, "start_day": 21, "end_month": 6, "end_day": 21},
    # 巨蟹座 6.22-7.22
    {"name": "巨蟹座", "start_month": 6, "start_day": 22, "end_month": 7, "end_day": 22},
    # 狮子座 7.23-8.22
    {"name": "狮子座", "start_month": 7, "start_day": 23, "end_month": 8, "end_day": 22},
    # 处女座 8.23-9.22
    {"name": "处女座", "start_month": 8, "start_day": 23, "end_month": 9, "end_day": 22},
    # 天秤座 9.23-10.23
    {"name": "天秤座", "start_month": 9, "start_day": 23, "end_month": 10, "end_day": 23},
    # 天蝎座 10.24-11.22
    {"name": "天蝎座", "start_month": 10, "start_day": 24, "end_month": 11, "end_day": 22},
    # 射手座 11.23-12.21
    {"name": "射手座", "start_month": 11, "start_day": 23, "end_month": 12, "end_day": 21},
    # 摩羯座 12.22-1.19
    {"name": "摩羯座", "start_month": 12, "start_day": 22, "end_month": 1, "end_day": 19},
]


def get_zodiac_sign(month: int, day: int) -> str:
    """根据月和日返回中文星座名称。"""
    # 参数校验 - 考虑每个月的实际天数
    if not (1 <= month <= 12):
        raise ValueError(f"月份必须在1-12之间，当前输入：{month}")
    
    # 根据月份进行严格的日期校验
    if month == 2:  # 2月最多29天
        if not (1 <= day <= 29):
            raise ValueError(f"2月日期必须在1-29之间，当前输入：{day}")
    elif month in [4, 6, 9, 11]:  # 小月（4,6,9,11月）最多30天
        if not (1 <= day <= 30):
            raise ValueError(f"{month}月日期必须在1-30之间，当前输入：{day}")
    else:  # 大月（1,3,5,7,8,10,12月）最多31天
        if not (1 <= day <= 31):
            raise ValueError(f"{month}月日期必须在1-31之间，当前输入：{day}")
    
    # 遍历星座边界，判断属于哪个星座
    for zodiac in ZODIAC_BOUNDARIES:
        # 处理跨年星座（摩羯座）
        if zodiac["start_month"] == 12:  # 摩羯座跨年
            if (month == 12 and day >= 22) or (month == 1 and day <= 19):
                return zodiac["name"]
        else:
            # 普通星座（不跨年）
            if (month == zodiac["start_month"] and day >= zodiac["start_day"]) or \
               (month == zodiac["end_month"] and day <= zodiac["end_day"]):
                return zodiac["name"]
    
    # 理论上不会执行到这里，但为了完整性
    raise ValueError(f"无法确定星座：{month}月{day}日")


def get_all_zodiac_signs() -> list:
    """获取所有星座名称列表。"""
    return [zodiac["name"] for zodiac in ZODIAC_BOUNDARIES]


def get_zodiac_date_range(zodiac_name: str) -> tuple:
    """获取星座的日期范围。返回：(开始月份, 开始日期, 结束月份, 结束日期)"""
    for zodiac in ZODIAC_BOUNDARIES:
        if zodiac["name"] == zodiac_name:
            return (zodiac["start_month"], zodiac["start_day"], 
                   zodiac["end_month"], zodiac["end_day"])
    raise ValueError(f"未找到星座：{zodiac_name}")

