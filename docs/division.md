# 五人分工与交付清单

请组长把表中的“成员”替换为真实姓名或学号。每位成员都要保留独立提交记录，并为自己负责的逻辑编写测试。

| 成员 | 分支 | 职责 | 主要文件 | 完成标准 |
|---|---|---|---|---|
| 成员 1（组长） | `docs/project-documentation` | 需求、接口协调、集成、README、演示材料 | `README.md`、`docs/`、`main.py` | 文档完整，协调 PR，最终程序可运行 |
| 成员 2 | `feature/date-calculation` | 输入解析、生日倒计时、出生天数、闰年规则 | `birthday_service.py`、`date_parser.py` | 边界测试通过，错误信息清楚 |
| 成员 3 | `feature/zodiac-query` | 星座数据结构、查询算法及测试 | `zodiac_service.py`、相关数据文件 | 十二星座边界全部正确，说明复杂度 |
| 成员 4 | `feature/fortune-export` | 离线运势、稳定随机结果、TXT/JSON 导出 | `fortune_service.py`、`export_service.py`、`fortune_data.json` | 同日同星座结果一致，能正确导出 |
| 成员 5 | `feature/gui` | Tkinter 界面、模块集成、错误提示、交互测试 | `app/ui/` | 能完成输入、查询、展示、导出完整流程 |

## 全员共同要求

1. 开发前阅读 `README.md`、`CONTRIBUTING.md` 和 `docs/architecture.md`。
2. 不修改其他成员负责的文件；确有需要时先沟通。
3. 每个功能至少包含正常情况、边界情况、错误情况三类测试。
4. Pull Request 中写明改了什么、如何测试、是否影响其他模块。
5. 合并前解决冲突并确保全部测试通过。

## 建议里程碑

- 第 1 天：确定真实分工、规则和接口，各自创建分支。
- 第 2～3 天：完成各核心模块和单元测试。
- 第 4 天：GUI 集成、修复接口问题。
- 第 5 天：完整测试、文档、截图和答辩演练。

