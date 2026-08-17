# 架构与接口约定

## 分层

```text
Tkinter UI
    ↓ 调用
Services（日期、星座、运势、导出）
    ↓ 使用
Models / Data / Utils
```

- UI 不应直接读取 JSON，也不应实现日期或星座算法。
- Service 不应弹出窗口，错误通过异常或返回值交给 UI 处理。
- 测试主要直接调用 Service 和 Utils，不依赖图形窗口。

## 固定接口

以下函数签名已经建立，各负责人优先在函数内部实现，避免随意改名：

```python
parse_birth_date(text: str) -> UserProfile
days_until_next_birthday(month: int, day: int, today: date | None = None) -> int
days_lived(birth_date: date, today: date | None = None) -> int
get_zodiac_sign(month: int, day: int) -> str
get_daily_fortune(zodiac: str, target_date: date | None = None) -> dict
export_fortune(result: dict, file_path: str | Path) -> Path
```

## 运势返回结构

```python
{
    "date": "2026-08-17",
    "zodiac": "狮子座",
    "overall": 4,
    "love": 3,
    "study": 5,
    "health": 4,
    "lucky_color": "蓝色",
    "lucky_number": 7,
    "message": "适合整理计划并完成重要任务。",
}
```

评分建议统一使用 1～5 的整数。运势属于娱乐内容，界面和导出文件中应有提示。

## 日期规则

- 接受 `YYYY-MM-DD` 和 `MM-DD`，输入前后空格应被忽略。
- 完整日期不得晚于今天；只有月日时不计算出生总天数。
- 生日当天倒计时为 0。
- 2 月 29 日出生者在非闰年按 2 月 28 日处理。
- 所有计算使用本机当前日期，测试通过 `today` 参数注入固定日期。

## 数据结构与算法

- 星座边界使用有序列表保存，可配合 `bisect` 二分查询，复杂度 `O(log n)`。
- 运势素材使用字典和 JSON 保存，按类别查询平均复杂度 `O(1)`。
- 每日运势可使用“日期 + 星座”作为稳定随机种子，保证同日结果一致。

## 错误处理

- 无效输入统一抛出带中文说明的 `ValueError`。
- 文件写入错误不得被静默忽略，UI 应显示友好提示。
- 不在业务模块使用宽泛的 `except Exception: pass`。

