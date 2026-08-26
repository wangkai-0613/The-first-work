# 自动生成的 API 文档（成员 4：运势与导出模块）

本目录由 [pdoc](https://pdoc.dev/) 根据 `app/services/fortune_service.py` 和
`app/services/export_service.py` 中的 docstring 自动生成，不要手工编辑
`docs/api/app/` 下的 HTML 文件。

## 重新生成

```bash
python -m pip install pdoc
python -m pdoc app.services.fortune_service app.services.export_service -o docs/api
```

生成后打开 `docs/api/index.html` 即可浏览。
