# 国内可访问作品集（GitHub 公开仓库自动镜像）

把 `intp41455` 在 GitHub 上的**所有公开仓库**自动生成一个单页作品集，
部署到国内节点后，HR / 国内访客可直接打开浏览（每个项目一键跳回 GitHub 源码）。
**不要求在线运行，只做"都能看"的展示门面。**

## 线上地址（重要：选对部署通道）
> ⚠️ **`https://showcase-cn-5egoqlia.edgeone.cool/` 不可靠，别写进简历。**
> 这是 **EdgeOne Makers 的「预览」域名**，公开访问按网络节点（PoP）抽风：服务器/部分网络能 200 直开，**但手机、部分运营商节点会强制要 token 而返回 401**（已实测手机 401）。HR 的手机也可能 401，所以**不能当正式链接**。

### ✅ 真正稳定可用的线上地址（二选一）
**A. 标准 EdgeOne Pages（控制台）连接 Git 仓库（推荐，零 token 自动部署）**
1. 打开 https://console.cloud.tencent.com/edgeone/pages （腾讯云账号，免费版够用）。
2. 「新建项目」→ 导入 Git 仓库 `intp41455/showcase-cn`（先在 EdgeOne 授权 GitHub）。
3. 框架选「纯静态 / 无」，**构建命令留空**，**输出目录填 `.`**。
4. 部署后控制台分配的 **`*.edgeone.app` 默认域名才是真正公开、免备案、长期有效的地址**（手机/电脑都能开）。
5. 之后本仓库 push 到 `main` 自动触发重新部署，新增仓库次日自动上线。

**B. Gitee Pages（纯国内、公开、免费）** —— 若不想用腾讯云，把仓库镜像到 Gitee 并开启 Gitee Pages（ `*用户名.gitee.io` ），国内公开稳定；缺点：免费版不支持 push 自动重新部署，需手动点「更新」。

### ❌ 不可靠的通道（仅临时查看用）
- Makers `deploy_folder` 工具部署的 `*.edgeone.cool` 预览域名：带 `?eo_token=...` 的链接仅约 **3 小时**有效；**不带 token 的裸域名也会在手机/部分网络 401**，不可作正式链接。

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
