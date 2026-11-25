#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Build tour_data.json and index.html for the static panorama site."""
import json
import os
import re
import xml.etree.ElementTree as ET

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BUILD = os.path.dirname(os.path.abspath(__file__))
STATE = os.path.join(BUILD, "state.json")
TEMPLATE = os.path.join(BUILD, "template.html")
OUT_HTML = os.path.join(ROOT, "index.html")


def fnum(v, default=0.0):
    try:
        return float(v)
    except (TypeError, ValueError):
        return default


def main():
    with open(STATE, encoding="utf-8") as f:
        st = json.load(f)
    config = st["data"]["product"]["config"]
    scenes = config["scenes"]
    cats = config["category"][0]["scenes"]
    by_id = {str(s["id"]): s for s in scenes}
    pano_to_id = {str(s["panoId"]): str(s["id"]) for s in scenes}

    root = ET.fromstring(st["xml"])
    views = {}
    for p in root.findall(".//config/panos/pano"):
        v = p.find("view")
        if v is not None:
            views[p.get("name")] = v.attrib

    out = {}
    for idx, c in enumerate(cats, 1):
        sid = str(c["id"])
        s = by_id.get(sid)
        if not s:
            continue
        pano = str(s["panoId"])
        view = views.get("s_" + sid, {})
        hotspots = []
        for h in s.get("hotspot", []):
            if not isinstance(h, dict):
                continue
            # krpano's vlookat/atv are positive downwards; Pannellum pitch is positive upwards.
            pitch = -fnum(h.get("atv"))
            yaw = fnum(h.get("ath"))
            htype = h.get("type")
            title = (h.get("title") or "").strip()
            if htype == 0:
                data = h.get("data")
                target_pano = ""
                if isinstance(data, dict):
                    target_pano = str(data.get("panoId") or "")
                target = pano_to_id.get(target_pano)
                if not target:
                    continue
                hotspots.append({
                    "pitch": round(pitch, 3),
                    "yaw": round(yaw, 3),
                    "type": "scene",
                    "sceneId": target,
                    "text": title or "前往",
                    "cssClass": "nav-spot",
                })
            elif htype == 4:
                if not title:
                    continue
                hotspots.append({
                    "pitch": round(pitch, 3),
                    "yaw": round(yaw, 3),
                    "type": "custom",
                    "cssClass": "pano-label",
                    "text": title,
                })
        out[sid] = {
            "id": sid,
            "panoId": pano,
            "name": s["name"],
            "index": idx,
            "thumb": f"thumbs/{pano}.jpg",
            "faces": [f"images/{pano}/{f}.jpg" for f in ("f", "r", "b", "l", "u", "d")],
            "yaw": round(fnum(view.get("hlookat")), 3),
            "pitch": round(-fnum(view.get("vlookat")), 3),
            "mfov": round(fnum(view.get("fov"), 95), 3),
            "hotSpots": hotspots,
        }

    first = str(cats[0]["id"]) if cats and str(cats[0]["id"]) in out else next(iter(out))
    data = {
        "title": "江苏电子信息职业学院",
        "subtitle": "720° 校园全景漫游",
        "source": "https://www.720yun.com/t/43vkcl1qgdy?scene_id=59712277",
        "author": "落墨良人",
        "firstScene": first,
        "sceneCount": len(out),
        "order": list(out.keys()),
        "scenes": out,
    }
    with open(os.path.join(ROOT, "tour_data.json"), "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=1)

    # Scene cards
    cards = []
    for sid, s in out.items():
        cards.append(
            f'<button class="scene-card" data-scene="{sid}" data-name="{s["name"]}" '
            f'title="{s["name"]}">'
            f'<span class="thumb"><img src="{s["thumb"]}" alt="{s["name"]}" loading="lazy" '
            f'width="72" height="72"></span>'
            f'<span class="meta"><span class="idx">{s["index"]:02d}</span>'
            f'<span class="name">{s["name"]}</span></span>'
            f'</button>'
        )
    cards_html = "\n      ".join(cards)
    data_json = json.dumps(data, ensure_ascii=False, separators=(",", ":"))

    with open(TEMPLATE, encoding="utf-8") as f:
        tpl = f.read()
    html = tpl.replace("<!--__SCENE_CARDS__-->", cards_html)
    html = html.replace("/*__TOUR_DATA__*/", data_json)
    with open(OUT_HTML, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"wrote {OUT_HTML}: {len(html)} bytes, {len(out)} scenes, "
          f"{sum(len(s['hotSpots']) for s in out.values())} hotspots")


if __name__ == "__main__":
    main()
