#!/usr/bin/env python3
"""index.html 의 DATA 블록을 읽어 osaka-trip.ics 를 만든다. 데이터 원본은 index.html 하나.
사용: python3 make_ics.py  (같은 폴더에서)"""
import json, re, uuid, datetime, urllib.parse, pathlib

here = pathlib.Path(__file__).parent
html = (here / "index.html").read_text(encoding="utf-8")
data = json.loads(re.search(r"/\*DATA-START\*/(.*?)/\*DATA-END\*/", html, re.S).group(1))

def esc(s):  # RFC 5545 TEXT escaping
    return s.replace("\\", "\\\\").replace(";", "\\;").replace(",", "\\,").replace("\n", "\\n")

def fold(line):  # 75 octets per line, CRLF + space continuation
    out, b = [], line.encode("utf-8")
    while len(b) > 75:
        cut = 75
        while cut > 0 and (b[cut] & 0xC0) == 0x80:  # don't split a UTF-8 sequence
            cut -= 1
        out.append(b[:cut].decode("utf-8")); b = b" " + b[cut:]
    out.append(b.decode("utf-8"))
    return "\r\n".join(out)

def map_url(it):
    if it.get("lat") is not None:
        return f"https://www.google.com/maps/search/?api=1&query={it['lat']},{it['lng']}"
    if it.get("q"):
        return "https://www.google.com/maps/search/?api=1&query=" + urllib.parse.quote(it["q"])
    return None

lines = [
    "BEGIN:VCALENDAR", "VERSION:2.0", "PRODID:-//osaka-trip//2026//KO", "CALSCALE:GREGORIAN",
    "X-WR-CALNAME:大阪 二泊三日", "X-WR-TIMEZONE:Asia/Tokyo",
    "BEGIN:VTIMEZONE", "TZID:Asia/Tokyo", "BEGIN:STANDARD", "DTSTART:19700101T000000",
    "TZOFFSETFROM:+0900", "TZOFFSETTO:+0900", "TZNAME:JST", "END:STANDARD", "END:VTIMEZONE",
]
stamp = datetime.datetime.now(datetime.timezone.utc).strftime("%Y%m%dT%H%M%SZ")
n = 0
for day in data["days"]:
    d = day["date"].replace("-", "")
    items = day["items"]
    # 한 카드가 여러 이벤트(공연 2세트)면 ics 필드로 펼친다
    events = []
    for i, it in enumerate(items):
        nxt_card = items[i + 1]["t"] if i + 1 < len(items) else None
        group = it.get("ics") or [[it["t"], it["name"]]]
        for gi, (t, title) in enumerate(group):
            nxt = group[gi + 1][0] if gi + 1 < len(group) else nxt_card  # 같은 카드 안에서는 다음 세트 시각
            events.append((t, title, it, nxt))
    for t, title, it, nxt in events:
        # 종료 = 다음 일정 시작(최대 3시간), 없으면 +30분. 자정을 넘기면 날짜도 넘긴다
        sh, sm = int(t[:2]), int(t[3:])
        if nxt:
            eh, em = int(nxt[:2]), int(nxt[3:])
            dur = (eh * 60 + em) - (sh * 60 + sm)
            if dur <= 0 or dur > 180: dur = 30
        else:
            dur = 30
        start_dt = datetime.datetime.strptime(d + t.replace(":", ""), "%Y%m%d%H%M")
        end_dt = start_dt + datetime.timedelta(minutes=dur)
        dtstart = start_dt.strftime("%Y%m%dT%H%M00")
        dtend = end_dt.strftime("%Y%m%dT%H%M00")
        memo = it.get("memo", "").replace("**", "")
        desc = memo
        if it.get("cost"): desc += (" · " if desc else "") + f"예상 ¥{it['cost']:,}"
        n += 1
        ev = [
            "BEGIN:VEVENT",
            f"UID:osaka2026-{it['id']}-{n}@mayfchoi",
            f"DTSTAMP:{stamp}",
            f"DTSTART;TZID=Asia/Tokyo:{dtstart}",
            f"DTEND;TZID=Asia/Tokyo:{dtend}",
            f"SUMMARY:{esc(title)}",
        ]
        if desc: ev.append(f"DESCRIPTION:{esc(desc)}")
        url = map_url(it)
        if url: ev.append(f"URL:{url}")
        if it.get("q"): ev.append(f"LOCATION:{esc(it['q'])}")
        if it.get("lat") is not None:
            ev.append(f"GEO:{it['lat']};{it['lng']}")
            # 아이폰 캘린더는 GEO 대신 이 확장으로 지도를 띄운다
            ev.append(f"X-APPLE-STRUCTURED-LOCATION;VALUE=URI;X-APPLE-RADIUS=50;X-TITLE={esc(it['name'])}:geo:{it['lat']},{it['lng']}")
        ev += ["BEGIN:VALARM", "ACTION:DISPLAY", f"DESCRIPTION:{esc(title)}", "TRIGGER:-PT30M", "END:VALARM", "END:VEVENT"]
        lines += ev
lines.append("END:VCALENDAR")
out = "\r\n".join(fold(l) for l in lines) + "\r\n"
(here / "osaka-trip.ics").write_text(out, encoding="utf-8", newline="")
print(f"osaka-trip.ics: {n} events, {len(out)} bytes")
