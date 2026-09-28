#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GitHub 公开仓库 -> 国内可访问的单页作品集生成器。

- 通过 GitHub 公开 API 拉取指定用户的所有公开仓库（无需 token）。
- 按分类（Web 应用 / 工具与库 / 方法论与文档 / 其他）生成 index.html。
- 可直接被 GitHub Actions 定时调用，实现"新增公开仓库自动同步"。

用法:
    python generate.py            # 拉取 intp41455 的公开仓库并生成 index.html
    GITHUB_USER=intp41455 python generate.py
"""

import json
import os
import platform
import subprocess
import sys
from datetime import datetime, timezone

GITHUB_USER = os.environ.get("GITHUB_USER", "intp41455")
OUTPUT = os.environ.get("OUTPUT", "index.html")

# 已知仓库的精确分类（新仓库会走下面的兜底规则）
CATEGORY_MAP = {
    # Web 应用 / 全栈 MVP
    "codepath": "web",
    "CodeMaster": "web",
    "career-assessment-system": "web",
    "smart-hr-platform": "web",
    "hr-payroll-platform": "web",
    "cutenote-clone": "web",
    "codetutor": "web",
    "destiny-compass": "web",
    "incidentops-enterprise-agent": "web",
    "life-workbench": "web",
    "notebook": "web",
    "local-kb-server": "web",
    # 工具与库
    "docx-standardizer": "tools",
    "rag-hybrid-retrieval": "tools",
    "llm-gateway": "tools",
    "lora-attendance-finetune": "tools",
    "ai-free-api-intel": "tools",
    "tianxi-bridge": "tools",
    # 方法论与文档
    "multi-agent-architecture-playbook": "docs",
    "ai-learning-wiki": "docs",
}

# 兜底分类关键词
WEB_KW = ["平台", "系统", "学院", "工作台", "app", "application", "mvp", "pwa",
          "网站", "web", "前端", "react", "vue", "express", "clone"]
TOOLS_KW = ["工具", "库", "网关", "检索", "rag", "微调", "finetune", "网关",
            "gateway", "逆向", "研究", "intel", "bridge"]


def classify(name, desc):
    if name in CATEGORY_MAP:
        return CATEGORY_MAP[name]
    d = (desc or "").lower()
    if any(k in d for k in WEB_KW):
        return "web"
    if any(k in d for k in TOOLS_KW):
        return "tools"
    return "docs"


def fetch_repos():
    url = f"https://api.github.com/users/{GITHUB_USER}/repos?per_page=100&sort=updated"
    # 沙箱 Windows 下 schannel 证书吊销离线，需 --ssl-no-revoke；Linux 忽略该选项
    ssl_flag = ["--ssl-no-revoke"] if platform.system() == "Windows" else []
    for attempt in range(3):
        try:
            out = subprocess.check_output(
                ["curl", "-sS", "--retry", "2", *ssl_flag, "-H",
                 "Accept: application/vnd.github+json", url],
                stderr=subprocess.DEVNULL,
                timeout=30,
            )
            data = json.loads(out)
            if isinstance(data, list):
                return data
        except Exception as e:
            print(f"[warn] fetch attempt {attempt+1} failed: {e}", file=sys.stderr)
    print("[error] 无法从 GitHub 拉取仓库，请检查网络", file=sys.stderr)
    sys.exit(1)


def build_card(r):
    name = r["name"]
    lang = r.get("language") or "—"
    desc = (r.get("description") or "（暂无描述）").strip()
    url = r["html_url"]
    updated = (r.get("updated_at") or "")[:10]
    badge_color = {
        "web": "#2f6df6", "tools": "#0f9d58", "docs": "#f4b400", "other": "#888"
    }[classify(name, r.get("description"))]
    return f"""
      <article class="card">
        <div class="card-head">
          <h3><a href="{url}" target="_blank" rel="noopener">{name}</a></h3>
          <span class="badge" style="background:{badge_color}">{lang}</span>
        </div>
        <p class="desc">{desc}</p>
        <div class="card-foot">
          <a class="gh-link" href="{url}" target="_blank" rel="noopener">在 GitHub 查看 →</a>
          <span class="date">更新 {updated}</span>
        </div>
      </article>"""


def build_section(title, repos):
    if not repos:
        return ""
    cards = "\n".join(build_card(r) for r in repos)
    return f"""
    <section>
      <h2 class="sec-title">{title}<span class="count">{len(repos)}</span></h2>
      <div class="grid">{cards}
      </div>
    </section>"""


def main():
    repos = fetch_repos()
    repos.sort(key=lambda r: r.get("updated_at", ""), reverse=True)

    groups = {"web": [], "tools": [], "docs": [], "other": []}
    for r in repos:
        cat = classify(r["name"], r.get("description"))
        groups[cat].append(r)

    sections = (
        build_section("🚀 可交互 Web 应用 / 全栈 MVP", groups["web"])
        + build_section("🧰 工具与库", groups["tools"])
        + build_section("📚 方法论与文档", groups["docs"])
        + build_section("📦 其他项目", groups["other"])
    )

    generated = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    total = len(repos)

    html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{GITHUB_USER} · 项目作品集（国内镜像）</title>
<style>
  :root {{
    --bg:#f6f8fb; --card:#ffffff; --ink:#1f2937; --muted:#6b7280;
    --accent:#2f6df6; --line:#e5e7eb;
  }}
  * {{ box-sizing:border-box; }}
  body {{ margin:0; font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",
    "PingFang SC","Microsoft YaHei",Roboto,Helvetica,Arial,sans-serif;
    background:var(--bg); color:var(--ink); line-height:1.6; }}
  header {{ background:linear-gradient(135deg,#2f6df6,#5b8def);
    color:#fff; padding:48px 24px 40px; text-align:center; }}
  header h1 {{ margin:0 0 8px; font-size:30px; letter-spacing:.5px; }}
  header p {{ margin:4px 0; opacity:.92; font-size:15px; }}
  header a {{ color:#fff; text-decoration:underline; }}
  .wrap {{ max-width:1080px; margin:0 auto; padding:32px 20px 64px; }}
  .sec-title {{ font-size:20px; margin:36px 0 16px; display:flex;
    align-items:center; gap:10px; border-left:4px solid var(--accent);
    padding-left:12px; }}
  .count {{ font-size:13px; background:var(--line); color:var(--muted);
    border-radius:999px; padding:1px 10px; }}
  .grid {{ display:grid; grid-template-columns:repeat(auto-fill,minmax(320px,1fr));
    gap:16px; }}
  .card {{ background:var(--card); border:1px solid var(--line);
    border-radius:14px; padding:18px; display:flex; flex-direction:column;
    transition:transform .12s ease, box-shadow .12s ease; }}
  .card:hover {{ transform:translateY(-3px);
    box-shadow:0 8px 24px rgba(31,41,55,.10); }}
  .card-head {{ display:flex; justify-content:space-between;
    align-items:flex-start; gap:10px; }}
  .card-head h3 {{ margin:0; font-size:17px; word-break:break-word; }}
  .card-head a {{ color:var(--ink); text-decoration:none; }}
  .card-head a:hover {{ color:var(--accent); }}
  .badge {{ flex:none; font-size:12px; color:#fff; border-radius:6px;
    padding:2px 8px; white-space:nowrap; }}
  .desc {{ color:var(--muted); font-size:14px; margin:10px 0 14px;
    flex:1; }}
  .card-foot {{ display:flex; justify-content:space-between;
    align-items:center; font-size:13px; }}
  .gh-link {{ color:var(--accent); text-decoration:none; font-weight:600; }}
  .gh-link:hover {{ text-decoration:underline; }}
  .date {{ color:#9ca3af; }}
  footer {{ text-align:center; color:var(--muted); font-size:13px;
    padding:24px; }}
  footer code {{ background:var(--line); padding:1px 6px; border-radius:4px; }}
</style>
</head>
<body>
<header>
  <h1>{GITHUB_USER} 的项目作品集</h1>
  <p>国内可访问镜像 · 共 {total} 个公开仓库</p>
  <p>源码仍在 <a href="https://github.com/{GITHUB_USER}" target="_blank" rel="noopener">github.com/{GITHUB_USER}</a>，本页自动同步</p>
</header>
<div class="wrap">
{sections}
</div>
<footer>
  本页由 <code>generate.py</code> 自动生成 · 最后同步：{generated}<br>
  自动同步：GitHub Actions 每日刷新 / WorkBuddy 每周兜底
</footer>
</body>
</html>"""

    with open(OUTPUT, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"[ok] 已生成 {OUTPUT}：{total} 个仓库（web={len(groups['web'])} "
          f"tools={len(groups['tools'])} docs={len(groups['docs'])} other={len(groups['other'])}）")


if __name__ == "__main__":
    main()
