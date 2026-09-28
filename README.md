# 国内可访问作品集（GitHub 公开仓库自动镜像）

把 `intp41455` 在 GitHub 上的**所有公开仓库**自动生成一个单页作品集，
部署到国内 CDN 后，HR / 国内访客可直接打开浏览（每个项目一键跳回 GitHub 源码）。
**不要求在线运行，只做"都能看"的展示页。**

## 包含的文件
- `generate.py` —— 拉取公开仓库、自动分类并生成 `index.html`（可本地直接跑）
- `index.html` —— 生成的单页作品集（已含全部 21 个仓库）
- `.github/workflows/sync.yml` —— GitHub Actions 每日自动重新生成并提交

## 怎么用（一次性，之后全自动）

### 1. 把这堆文件推到一个新仓库
```bash
# 在 GitHub 新建一个仓库，例如 showcase-cn，然后：
git init
git add .
git commit -m "init portfolio mirror"
git remote add origin https://github.com/intp41455/showcase-cn.git
git push -u origin main
```

### 2. 连接 EdgeOne Pages（免费，国内加速）
1. 打开 [EdgeOne Pages 控制台](https://console.cloud.tencent.com/edgeone/pages)（需腾讯云账号，免费版够用）。
2. 「新建项目」→ 导入上面的 Git 仓库。
3. 框架预设选 **纯静态 / 无**（Static），构建命令留空，输出目录填 `.`（根目录）。
4. 部署，获得 `*.edgeone.app` 域名 —— **国内秒开**。
5. （可选）在 EdgeOne 绑定自己的域名，如 `projects.intp41455.com`。

之后：GitHub Actions 每天拉取最新公开仓库 → 重新生成 `index.html` → 提交 →
EdgeOne 自动重新部署。**你以后新建任何公开仓库，第二天就会自动出现在作品集里。**

## 本地预览 / 手动生成
```bash
python generate.py          # 生成 index.html
python -m http.server 8000  # 本地预览
```

## 备选：不想配 EdgeOne？
WorkBuddy 环境里已加了一个**每周兜底自动化**，会用 WorkBuddy 自带的发布能力
把作品集发布成国内可访问链接，作为 EdgeOne 之外的双保险。

## 分类规则
`generate.py` 里有 `CATEGORY_MAP` 做精确分类；新仓库按关键词兜底归入
Web 应用 / 工具与库 / 方法论与文档。需要调整分组直接改 `CATEGORY_MAP` 即可。
