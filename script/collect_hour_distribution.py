import os
import datetime
from collections import Counter

ROOT = os.path.join(os.path.dirname(__file__), "..", "_posts")
TIME_FMT_FULL = "%Y-%m-%d %H:%M:%S"
TIME_FMT_DATE = "%Y-%m-%d"

def parse_time_loose(s):
    s = s.strip()
    try:
        return datetime.datetime.strptime(s, TIME_FMT_FULL)
    except ValueError:
        try:
            return datetime.datetime.strptime(s, TIME_FMT_DATE)
        except ValueError:
            return None


def read_front_matter(lines):
    if not lines or lines[0].strip() != "---":
        return {}

    fm = {}
    for line in lines[1:]:
        if line.strip() == "---":
            break
        if ":" in line:
            k, v = line.split(":", 1)
            fm[k.strip()] = v.strip()
    return fm


counter = Counter()
total = 0

for base, _, files in os.walk(ROOT):
    for f in files:
        if not f.endswith(".md"):
            continue

        path = os.path.join(base, f)
        with open(path, "r", encoding="utf-8") as r:
            lines = r.readlines()

        fm = read_front_matter(lines)

        for key in ("date", "updated"):
            if key not in fm:
                continue

            dt = parse_time_loose(fm[key])
            if not dt:
                continue

            counter[dt.hour] += 1
            total += 1


print("hour  count  probability")
for h in range(24):
    c = counter.get(h, 0)
    p = c / total if total else 0
    print(f"{h:02d}    {c:<6d} {p:.4f}")
