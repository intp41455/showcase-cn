#!/usr/bin/env python3
"""每日把最新生成的 index.html 推送到 Gitee 仓库（供 Gitee Pages 部署）。
依赖环境变量 GITEE_TOKEN。仅更新 index.html（展示页），其余文件不常变。
"""
import os
import base64
import json
import urllib.request
import urllib.error

TOKEN = os.environ.get("GITEE_TOKEN")
OWNER = "intp41455"
REPO = "showcase-cn"
BRANCH = "master"
PATH = "index.html"
API = "https://gitee.com/api/v5"


def req(method, url, data=None):
    body = json.dumps(data).encode() if data else None
    r = urllib.request.Request(url, data=body, method=method)
    if body:
        r.add_header("Content-Type", "application/json")
    with urllib.request.urlopen(r, timeout=30) as resp:
        return resp.read().decode()


def main():
    if not TOKEN:
        print("未配置 GITEE_TOKEN，跳过 Gitee 同步")
        return
    with open("index.html", "rb") as f:
        content = base64.b64encode(f.read()).decode()

    sha = None
    try:
        r = req("GET", f"{API}/repos/{OWNER}/{REPO}/contents/{PATH}?access_token={TOKEN}")
        sha = json.loads(r)["sha"]
    except urllib.error.HTTPError:
        pass  # 文件不存在则创建

    body = {
        "access_token": TOKEN,
        "content": content,
        "message": "auto sync index.html",
        "branch": BRANCH,
    }
    if sha:
        body["sha"] = sha
    req("POST", f"{API}/repos/{OWNER}/{REPO}/contents/{PATH}?access_token={TOKEN}", body)
    print("已同步 index.html 到 Gitee")


if __name__ == "__main__":
    main()
