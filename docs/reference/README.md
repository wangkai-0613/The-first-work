# 说明文档（自动生成）

本目录是第三次作业要求的“说明文档”：用 [pdoc](https://pdoc.dev/) 从
`app/` 下每个模块、类、函数的 docstring 自动生成，覆盖全部五人分工的
代码（`app/models`、`app/services`、`app/ui`、`app/utils`）。不要手工
编辑本目录下的 HTML 文件——它们都是生成产物，源头是各模块文件里的
注释。

## 浏览

打开 `docs/reference/index.html`（或直接看 `docs/reference/app.html`）。

## 重新生成

代码里的 docstring 改动后，在仓库根目录重新执行：

```bash
python -m pip install pdoc
python -m pdoc app -o docs/reference
```

## 与 `docs/architecture.md`、`docs/division.md` 的关系

- `docs/architecture.md` / `docs/division.md`：人工维护的设计和分工说明。
- `docs/reference/`（本目录）：从代码注释自动生成，随代码同步更新，
  不需要也不应该手工同步内容。
