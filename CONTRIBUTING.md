# Git 协作规范

## 首次准备

```bash
git clone https://github.com/wangkai-0613/The-first-work.git
cd The-first-work
git switch main
git pull
```

## 开发流程

每次开发前从最新的 `main` 创建自己的功能分支：

```bash
git switch main
git pull
git switch -c feature/功能名称
```

推荐分支：

- `feature/date-calculation`
- `feature/zodiac-query`
- `feature/fortune-export`
- `feature/gui`
- `docs/project-documentation`

提交和推送：

```bash
git status
git add 你负责的文件
git commit -m "feat: 简要描述改动"
git push -u origin 当前分支名
```

随后在 GitHub 创建 Pull Request，请至少一位队员检查后再合并。

## 提交信息

- `feat:` 新功能
- `fix:` 修复错误
- `test:` 测试
- `docs:` 文档
- `ui:` 界面
- `refactor:` 重构但不改变功能

示例：`feat: add birthday countdown calculation`

## 避免冲突

- 不要多人同时修改同一个模块；先查看 `docs/division.md`。
- 不要提交 `.venv`、缓存、IDE 配置或 `exports/` 中的个人文件。
- 不要使用 `git push --force` 修改公共分支。
- 不要把访问令牌、密码、真实用户隐私或 API 密钥提交到仓库。
- 合并前必须执行 `python -m unittest discover -s tests -v`。
- 接口需要调整时，先在群里说明，同时更新架构文档和相关测试。

