# 国内可访问作品集（GitHub 公开仓库自动镜像）

把 `intp41455` 在 GitHub 上的**所有公开仓库**自动生成一个单页作品集，
部署到国内节点后，HR / 国内访客可直接打开浏览（每个项目一键跳回 GitHub 源码）。
**不要求在线运行，只做"都能看"的展示门面。**

## 线上地址（国内直连）
- 正式域名：`https://github-portfolio-cn-mirror-fo0hfnld.edgeone.cool`
- 带授权预览链接（有时效，见 WorkBuddy 部署返回）：`*.edgeone.cool?eo_token=...&eo_time=...`
- 部署方式：EdgeOne Pages（Makers）`deploy_folder` 工具，国内 CDN 加速，免费。

## 包含的文件
- `generate.py` —— 拉取公开仓库、自动分类并生成 `index.html`（可本地直接跑，无需 token）
- `index.html` —— 生成的单页作品集（每次运行抓取当时所有公开仓库）
- `.github/workflows/sync.yml` —— GitHub Actions 每日自动重新生成并提交到本仓库

## 自动更新闭环（已配好）
- **每日（GitHub Actions，零 token）**：`sync.yml` 跑在 GitHub 免费 runner，拉取最新公开仓库、重新生成 `index.html` 并推回本仓库。
- **每周日 9:00（WorkBuddy 自动化，极小 token）**：调用 EdgeOne Pages `deploy_folder` 工具把最新目录重新部署到国内节点。
- 你以后在 GitHub 新建任何公开仓库，**最迟次周周日**自动出现在国内作品集里，零维护。

## 手动重新部署（如需）
EdgeOne Pages（Makers）只能通过其 `deploy_folder` 工具部署（不支持连接 Git 自动触发）：
- `workspacePath` = `builtFolderPath` = 含 `index.html` 的项目根目录
- `projectType` = `static`
- `projectName` = `github-portfolio-cn-mirror`
- 首次会弹浏览器登录（选中国站），返回带 `eo_token` 的 `*.edgeone.cool` 链接，国内直连可达。

## 本地预览 / 手动生成
```bash
python generate.py          # 生成 index.html（默认用户 intp41455）
python -m http.server 8000  # 本地预览
```

## 分类规则
`generate.py` 里有 `CATEGORY_MAP` 做精确分类；新仓库按关键词兜底归入
Web 应用 / 工具与库 / 方法论与文档。需要调整分组直接改 `CATEGORY_MAP` 即可。
