# 国内可访问作品集（GitHub 公开仓库自动镜像）

把 `intp41455` 在 GitHub 上的**所有公开仓库**自动生成一个单页作品集，
部署到国内节点后，HR / 国内访客可直接打开浏览（每个项目一键跳回 GitHub 源码）。
**不要求在线运行，只做"都能看"的展示门面。**

## 线上地址（国内直连 · 免备案 · 长期有效）
- **正式地址**：`https://showcase-cn-5egoqlia.edgeone.cool/`
  （EdgeOne Pages 连接 `showcase-cn` 仓库后分配的默认域名；**国内 CDN 加速、免备案、免费、长期有效**。）
- **注意**：首次部署后控制台弹出的带 `?eo_token=...` 预览链接**仅约 3 小时有效**，用于临时查看；给 HR/面试官请用上面不带 token 的正式地址。
- 部署方式：EdgeOne Pages **连接 GitHub 仓库 `intp41455/showcase-cn`**，纯静态自动部署；push 到 `main` 自动触发重新部署。

## 包含的文件
- `generate.py` —— 拉取公开仓库、自动分类并生成 `index.html`（可本地直接跑，无需 token）
- `index.html` —— 生成的单页作品集（每次运行抓取当时所有公开仓库）
- `.github/workflows/sync.yml` —— GitHub Actions 每日自动重新生成并提交到本仓库

## 自动更新闭环（零 token 全自动）
- `sync.yml`（GitHub Actions，每日 cron）跑在 GitHub 免费 runner：拉取 `intp41455` 最新公开仓库、重新生成 `index.html` 并推回本仓库。
- 本仓库已连接 EdgeOne Pages，push 到 `main` 自动触发重新部署。**新增公开仓库次日自动出现在国内作品集，零 token、零维护。**
- 早期用 EdgeOne Makers `deploy_folder` 工具部署的预览项目（`makers-cmijuqonak0f`）已弃用，可忽略。

## 手动重新生成 / 本地预览
```bash
python generate.py          # 生成 index.html（默认用户 intp41455）
python -m http.server 8000  # 本地预览
```

## 分类规则
`generate.py` 里有 `CATEGORY_MAP` 做精确分类；新仓库按关键词兜底归入
Web 应用 / 工具与库 / 方法论与文档。需要调整分组直接改 `CATEGORY_MAP` 即可。
