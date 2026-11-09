#!/usr/bin/env python3
"""按 issues.json 批量创建 GitHub Issue。

默认只预览，加 --apply 才创建；创建前会拉取现有 Issue 标题查重。

用法：
    python scripts/create_issues.py --repo OWNER/REPO
    python scripts/create_issues.py --repo OWNER/REPO --only-stage S0 --apply
"""

import argparse
import json
import subprocess
import sys
from pathlib import Path
from tempfile import NamedTemporaryFile


def run_gh(args):
    proc = subprocess.run(["gh", *args], capture_output=True, text=True, encoding="utf-8")
    if proc.returncode != 0:
        raise RuntimeError(proc.stderr.strip() or "gh 执行失败")
    return proc.stdout


def normalize(title):
    return "".join(title.split()).lower()


def existing_titles(repo):
    out = run_gh(["issue", "list", "--repo", repo, "--state", "all",
                  "--limit", "2000", "--json", "title"])
    return {normalize(i["title"]) for i in json.loads(out or "[]")}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", required=True)
    ap.add_argument("--data", default="scripts/issues.json")
    ap.add_argument("--only-stage", default=None)
    ap.add_argument("--apply", action="store_true")
    args = ap.parse_args()

    data = json.loads(Path(args.data).read_text(encoding="utf-8"))
    seen = existing_titles(args.repo) if args.apply else set()
    created = skipped = planned = 0

    print(f"仓库: {args.repo}  模式: {'创建' if args.apply else '预览'}")
    for item in data:
        stage = item.get("stage", "")
        if args.only_stage and stage != args.only_stage:
            continue
        planned += 1
        title, key = item["title"], normalize(item["title"])
        if key in seen:
            print(f"SKIP  已存在: {title}")
            skipped += 1
            continue
        if not args.apply:
            print(f"PLAN  [{stage}] {title}")
            continue

        labels = ["type:feature"]
        if item.get("priority"):
            labels.append(f"priority:{item['priority'].lower()}")
        if item.get("module"):
            labels.append(f"module:{item['module'].lower()}")

        with NamedTemporaryFile("w", suffix=".md", delete=False, encoding="utf-8") as fh:
            fh.write(item.get("body", ""))
            body_file = fh.name

        cmd = ["issue", "create", "--repo", args.repo, "--title", title,
               "--body-file", body_file]
        for label in labels:
            cmd += ["--label", label]
        try:
            print(f"CREATE {title} -> {run_gh(cmd).strip()}")
            seen.add(key)
            created += 1
        except RuntimeError as exc:
            print(f"FAIL  {title}: {exc}")

    print(f"\n匹配 {planned}，创建 {created}，跳过 {skipped}。")
    if not args.apply:
        print("预览模式，加 --apply 才会真正创建。")


if __name__ == "__main__":
    main()
