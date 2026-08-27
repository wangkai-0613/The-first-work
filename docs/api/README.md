# 自动生成的 API 文档

本目录由 [pdoc](https://pdoc.dev/) 根据 `app/` 各模块源码中的 docstring
自动生成，覆盖数据模型、工具、全部业务服务与第五部分的界面模块，
不要手工编辑 `docs/api/` 下的 HTML 文件。

## 重新生成

```bash
python -m pip install pdoc
python -m pdoc app -o docs/api
```

生成后打开 `docs/api/index.html` 即可浏览（会自动跳转到 `app.html`）。
