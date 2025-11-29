import os
import datetime

ROOT = os.path.join(os.path.dirname(__file__), "..", "_posts")
ROOT_PARENT = os.path.basename(os.path.dirname(ROOT))  # 上一级目录名

def fmt(t):
    return t.strftime("%Y-%m-%d %H:%M:%S")

def parse_updated(s):
    try:
        return datetime.datetime.strptime(s.strip(), "%Y-%m-%d %H:%M:%S")
    except ValueError:
        return None

updated_files = []

for base, dirs, files in os.walk(ROOT):
    for f in files:
        if not f.endswith(".md"):
            continue

        path = os.path.join(base, f)
        stat = os.stat(path)
        mtime_dt = datetime.datetime.fromtimestamp(stat.st_mtime)
        mtime_ts = stat.st_mtime

        with open(path, "r", encoding="utf-8") as r:
            lines = r.readlines()

        changed = False
        out = []

        for line in lines:
            if line.startswith("updated:"):
                current_str = line.strip().split("updated:", 1)[1].strip()
                current_dt = parse_updated(current_str)

                if current_dt is None or abs((current_dt - mtime_dt).total_seconds()) >= 60:
                    out.append(f"updated: {fmt(mtime_dt)}\n")
                    changed = True
                else:
                    out.append(line)
            else:
                out.append(line)

        if changed:
            with open(path, "w", encoding="utf-8") as w:
                w.writelines(out)
            os.utime(path, (stat.st_atime, mtime_ts))
            updated_files.append(os.path.relpath(path, start=ROOT))

def print_tree(paths):
    tree = {}
    for p in paths:
        parts = p.split(os.sep)
        d = tree
        for part in parts[:-1]:
            d = d.setdefault(part, {})
        d[parts[-1]] = None

    def _print(d, prefix=""):
        items = list(d.items())
        for i, (k, v) in enumerate(items):
            connector = "└── " if i == len(items)-1 else "├── "
            if v is None:
                print(prefix + connector + k)
            else:
                print(prefix + connector + k + "/")
                new_prefix = prefix + ("    " if i == len(items)-1 else "│   ")
                _print(v, new_prefix)

    _print(tree)

if updated_files:
    print(f"\n更新{len(updated_files)}个文件时间成功喵~o( =∩ω∩= )m：")
    print(f"{ROOT_PARENT}/_posts/")
    print_tree(updated_files)
else:
    print("\n全部文件已是最新状态喵~o( =∩ω∩= )m")
