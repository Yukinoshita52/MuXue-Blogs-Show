import os
import datetime
import random
from collections import Counter

ROOT = os.path.join(os.path.dirname(__file__), "..", "_posts")
FMT_FULL = "%Y-%m-%d %H:%M:%S"
FMT_DATE = "%Y-%m-%d"


# ---------- time ----------

def parse_full(s):
    try:
        return datetime.datetime.strptime(s, FMT_FULL)
    except:
        return None


def parse_date(s):
    try:
        return datetime.datetime.strptime(s, FMT_DATE)
    except:
        return None


def fmt(dt):
    return dt.strftime(FMT_FULL)


# ---------- front matter ----------

def read_fm(lines):
    if not lines or lines[0].strip() != "---":
        return {}, 0
    fm = {}
    i = 1
    while i < len(lines):
        if lines[i].strip() == "---":
            return fm, i + 1
        if ":" in lines[i]:
            k, v = lines[i].split(":", 1)
            fm[k.strip()] = v.strip()
        i += 1
    return fm, 0


def write_fm(lines, fm, body):
    out = ["---\n"]
    for k, v in fm.items():
        out.append(f"{k}: {v}\n")
    out.append("---\n")
    out.extend(lines[body:])
    return out


# ---------- scan ----------

def scan():
    posts = []
    for b, _, fs in os.walk(ROOT):
        for f in fs:
            if not f.endswith(".md"):
                continue
            p = os.path.join(b, f)
            with open(p, encoding="utf-8") as r:
                lines = r.readlines()
            fm, body = read_fm(lines)
            st = os.stat(p)
            posts.append({
                "path": p,
                "rel": os.path.relpath(p, ROOT),
                "fm": fm,
                "lines": lines,
                "body": body,
                "atime": st.st_atime,
            })
    return posts


# ---------- hour distribution ----------

def hour_dist(posts):
    c = Counter()
    t = 0
    for p in posts:
        for k in ("date", "updated"):
            v = p["fm"].get(k)
            if not v:
                continue
            dt = parse_full(v) or parse_date(v)
            if dt:
                c[dt.hour] += 1
                t += 1
    return {h: (c[h] / t if t else 1 / 24) for h in range(24)}


def rand_time(d, prob):
    base = parse_date(d)
    h = random.choices(list(prob), list(prob.values()))[0]
    return base.replace(
        hour=h,
        minute=random.randint(0, 59),
        second=random.randint(0, 59),
    )


def build_time(v, prob):
    return parse_full(v) or (rand_time(v, prob) if parse_date(v) else None)


# ---------- view ----------

def view(posts, cmd):
    ps = []
    parts = cmd.split()

    if parts[0] == "all":
        ps = posts

    elif parts[0] == "recent":
        n = int(parts[1]) if len(parts) > 1 else 5
        ps = sorted(posts, key=lambda p: p["fm"].get("date", ""), reverse=True)[:n]

    else:
        ym = parts[0]
        n = int(parts[1]) if len(parts) > 1 else None
        for p in posts:
            d = p["fm"].get("date")
            dt = parse_full(d) or parse_date(d) if d else None
            if dt and dt.strftime("%Y-%m") == ym:
                ps.append((dt, p))
        ps.sort(reverse=True)
        ps = [p for _, p in (ps[:n] if n else ps)]

    for i, p in enumerate(ps, 1):
        d = p["fm"].get("date", "")
        print(f"[{i}] {d[:16]:16} | {p['rel']}")


# ---------- modify ----------

def modify(posts, line):
    args = line.split()
    if len(args) % 3 != 0:
        print("参数数量错误")
        return

    prob = hour_dist(posts)

    for i in range(0, len(args), 3):
        rel, date, updated = args[i:i+3]
        p = next((x for x in posts if x["rel"] == rel), None)
        if not p:
            print(f"未找到 {rel}")
            return

        fm = p["fm"]
        if date != "-":
            dt = build_time(date, prob)
            if not dt:
                print("date 格式错误")
                return
            fm["date"] = fmt(dt)

        ut = None
        if updated != "-":
            ut = build_time(updated, prob)
            if not ut:
                print("updated 格式错误")
                return
            fm["updated"] = fmt(ut)

        out = write_fm(p["lines"], fm, p["body"])
        with open(p["path"], "w", encoding="utf-8") as w:
            w.writelines(out)
        if ut:
            os.utime(p["path"], (p["atime"], ut.timestamp()))

    print("修改完成")


# ---------- main ----------

def main():
    posts = scan()

    print("1. 查看博客时间")
    print("2. 修改博客时间")
    op = input().strip()
    if not op:
        return

    if op == "1":
        cmd = input("输入 YYYY-MM [N] / recent [N] / all：").strip()
        if not cmd:
            return
        view(posts, cmd)

    elif op == "2":
        line = input("输入 [文章] [date] [updated] ... ：").strip()
        if not line:
            return
        modify(posts, line)


if __name__ == "__main__":
    main()
