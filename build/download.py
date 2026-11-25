#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Download all 720yun cube faces and thumbnails for the offline tour."""
import json
import os
import sys
import time
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
import requests

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STATE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "state.json")
CDN = "https://ssl-panoimg130.720static.com"
BASE = "/resource/prod/d0737059s34/230jO5syrm7"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                  "(KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
    "Referer": "https://www.720yun.com/",
    "Accept": "image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8",
}
FACES = ["f", "b", "l", "r", "u", "d"]

lock = threading.Lock()
done = 0
failed = []
total_bytes = 0


def fetch(url, dest, min_bytes=40000):
    last = None
    for attempt in range(4):
        try:
            r = requests.get(url, headers=HEADERS, timeout=60)
            ctype = r.headers.get("content-type", "")
            if r.status_code == 200 and ctype.startswith("image/") and len(r.content) >= min_bytes:
                os.makedirs(os.path.dirname(dest), exist_ok=True)
                tmp = dest + ".part"
                with open(tmp, "wb") as f:
                    f.write(r.content)
                os.replace(tmp, dest)
                return len(r.content)
            last = f"HTTP {r.status_code} {ctype} {len(r.content)}B"
        except Exception as e:
            last = repr(e)
        time.sleep(0.8 * (attempt + 1))
    raise RuntimeError(f"{url} -> {last}")


def job(url, dest, min_bytes=40000):
    global done, total_bytes
    if os.path.exists(dest) and os.path.getsize(dest) >= min_bytes:
        size = os.path.getsize(dest)
    else:
        size = fetch(url, dest, min_bytes)
    with lock:
        done += 1
        total_bytes += size
        if done % 10 == 0 or done == TOTAL:
            print(f"[{done}/{TOTAL}] {total_bytes/1024/1024:.1f} MB  {os.path.basename(os.path.dirname(dest))}/{os.path.basename(dest)}", flush=True)
    return dest


def main():
    global TOTAL
    with open(STATE, encoding="utf-8") as f:
        st = json.load(f)
    scenes = st["data"]["product"]["config"]["scenes"]
    tasks = []
    for s in scenes:
        pano = str(s["panoId"])
        for face in FACES:
            url = f"{CDN}{BASE}/{pano}/imgs/mobile_{face}.jpg"
            dest = os.path.join(ROOT, "images", pano, face + ".jpg")
            tasks.append((url, dest, 40000))
        url = f"{CDN}{BASE}/{pano}/imgs/thumb.jpg"
        dest = os.path.join(ROOT, "thumbs", pano + ".jpg")
        tasks.append((url, dest, 5000))
    # cover preview
    tasks.append((f"{CDN}{BASE}/34496034/imgs/preview.jpg", os.path.join(ROOT, "cover.jpg"), 20000))
    TOTAL = len(tasks)
    print(f"Downloading {TOTAL} files ({len(scenes)} scenes)...", flush=True)
    with ThreadPoolExecutor(max_workers=8) as ex:
        futs = {ex.submit(job, u, d, m): (u, d) for u, d, m in tasks}
        for fut in as_completed(futs):
            try:
                fut.result()
            except Exception as e:
                with lock:
                    failed.append(str(e))
    print(f"Done. {done}/{TOTAL}, total {total_bytes/1024/1024:.1f} MB, failed {len(failed)}", flush=True)
    for e in failed:
        print("FAILED:", e, flush=True)
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
