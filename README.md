# 生日助手（题目 4）

这是一个由 5 人使用 Git 协作完成的 Python/Tkinter 桌面小程序。程序计划支持生日倒计时、出生天数、星座查询、每日运势和结果导出。

> 当前分支提供项目框架和协作约定，核心功能由各成员在独立功能分支中完成。

## 快速开始

项目只依赖 Python 标准库，建议使用 Python 3.10 或更高版本。

```bash
python main.py
```

运行测试：

```bash
python -m unittest discover -s tests -v
```

## 目录结构

```text
.
├── main.py                       # 程序入口
├── app/
│   ├── models/user_profile.py    # 用户数据模型
│   ├── services/                 # 日期、星座、运势、导出业务逻辑
│   ├── data/fortune_data.json    # 离线运势素材
│   ├── ui/main_window.py         # Tkinter 主界面
│   └── utils/                    # 输入解析和校验工具
├── tests/                        # 单元测试与集成测试
├── docs/
│   ├── architecture.md           # 架构、接口和关键规则
│   └── division.md               # 5 人分工与交付要求
├── CONTRIBUTING.md               # Git 协作规范
└── exports/                      # 本地导出目录，导出文件不提交
```

## 功能目标

- 输入 `YYYY-MM-DD` 或 `MM-DD` 格式的出生日期。
- 查询距离下一次生日的天数。
- 输入年份时查询已出生天数和年龄。
- 根据月、日查询十二星座。
- 查询当日娱乐运势，并导出为 TXT；可扩展 JSON/CSV。
- 提供清晰的图形界面、输入校验和错误提示。

## 重要约定

1. 界面层只负责收集输入和展示结果，不在按钮回调中编写日期算法。
2. 业务逻辑统一放在 `app/services/`，以便测试和多人协作。
3. `2 月 29 日`生日在非闰年暂按 `2 月 28 日`庆祝；如需修改，必须先更新文档和测试。
4. 生日当天距离下一次生日为 `0` 天。
5. 每日运势是离线生成的娱乐结果，同一星座在同一天应保持一致。
6. 所有人从功能分支提交 Pull Request，不直接向 `main` 推送。

详细接口见 [docs/architecture.md](docs/architecture.md)，分工见 [docs/division.md](docs/division.md)，协作步骤见 [CONTRIBUTING.md](CONTRIBUTING.md)。

