import os
import re
import time
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
from collections import defaultdict

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
POSTS_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, "../_posts"))

IMG_PATTERN = re.compile(
    r"https://blogs\.muxueavid\.top/blogs/(\d{4})/(\d{2})/([^/\s)\"']+\.(png|jpg))"
)

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

HEAD_TIMEOUT = 2
GET_TIMEOUT = 3
MAX_WORKERS = 4
SLEEP = 0.05
BAR_WIDTH = 40


def render_progress(done, total):
    ratio = done / total if total else 1
    filled = int(BAR_WIDTH * ratio)
    bar = "█" * filled + "░" * (BAR_WIDTH - filled)
    percent = ratio * 100
    print(
        f"\r检测进度: [{bar}] {done}/{total} ({percent:.1f}%)",
        end="",
        flush=True
    )


def check_url(url):
    try:
        r = requests.head(url, headers=HEADERS, timeout=HEAD_TIMEOUT)
        if r.status_code < 400:
            return url, True
    except Exception:
        pass

    try:
        r = requests.get(url, headers=HEADERS, timeout=GET_TIMEOUT, stream=True)
        if r.status_code < 400:
            return url, True
    except Exception:
        pass

    return url, False


def collect_structured_urls():
    data = defaultdict(lambda: defaultdict(list))

    for root, _, files in os.walk(POSTS_ROOT):
        for f in files:
            if not f.endswith(".md"):
                continue
            path = os.path.join(root, f)
            with open(path, "r", encoding="utf-8", errors="ignore") as md:
                content = md.read()
                for m in IMG_PATTERN.finditer(content):
                    year = int(m.group(1))
                    month = int(m.group(2))
                    url = m.group(0)
                    data[year][month].append(url)

    return data


def flatten_urls(data, start_year=None, start_month=None):
    urls = []
    for year in sorted(data):
        for month in sorted(data[year]):
            if start_year is not None:
                if (year, month) < (start_year, start_month):
                    continue
            urls.extend(data[year][month])
    return urls


def parse_year_month(s):
    y, m = s.split("-")
    return int(y), int(m)


if __name__ == "__main__":
    structured = collect_structured_urls()

    print("检测模式:")
    print("1 - 全部图片")
    print("2 - 指定时间之后的图片")
    mode = input("请选择模式 (1/2): ").strip()

    start_year = start_month = None
    if mode == "2":
        ym = input("请输入起始年月 (YYYY-MM): ").strip()
        start_year, start_month = parse_year_month(ym)

    urls = flatten_urls(structured, start_year, start_month)
    total = len(urls)

    print(f"检测图片总数: {total}")

    success = 0
    failed = []
    done = 0

    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as pool:
        futures = [pool.submit(check_url, u) for u in urls]

        for fut in as_completed(futures):
            url, ok = fut.result()
            done += 1

            if ok:
                success += 1
            else:
                # 提取 年-月-文件名
                m = IMG_PATTERN.search(url)
                if m:
                    y, mth, name = m.group(1), m.group(2), m.group(3)
                    failed.append(f"{y}-{mth}-{name}")
                    print(f"\n[失效] {y}-{mth}-{name}")
                else:
                    failed.append(url)
                    print(f"\n[失效] {url}")

            render_progress(done, total)
            time.sleep(SLEEP)

    print("\n----")
    print(f"成功数量: {success}")
    print(f"失效数量: {len(failed)}")
