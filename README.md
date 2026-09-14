# osaka-trip

2026.9.20–22 오사카 2박 3일, 폰으로 보는 단일 페이지 웹앱. 서버·빌드·외부 API 없음, 오프라인 동작.

| 파일 | 용도 |
|---|---|
| `index.html` | 앱 본체. CSS/JS/아이콘(data URI) 전부 인라인. 이것 하나만 있으면 동작 |
| `osaka-trip.ics` | 일정 44건, Asia/Tokyo, 각 30분 전 알림. 아이폰 캘린더에 임포트 |
| `icon-180.png` / `icon-512.png` / `icon.svg` | 홈 화면 아이콘 (GitHub Pages 배포 시 파일로도 제공) |
| `make_ics.py` | `index.html` 의 DATA 블록에서 `.ics` 재생성. 일정을 고치면 `python3 make_ics.py` |

## 폰에 올리기

1. **GitHub Pages** (홈 화면 추가·아이콘까지 되는 유일한 경로). 이 폴더를 repo 로 push → Settings → Pages → main / root. `https://<user>.github.io/osaka-trip/` 를 Safari 로 열고 공유 → 홈 화면에 추가.
2. **파일만**: `index.html` 을 AirDrop/iCloud 로 보내 Safari 에서 열기. 동작은 전부 되지만 홈 화면 추가는 안 됨 (file:// 제한).

`.ics` 는 AirDrop 이나 메일 첨부로 보내서 탭 → "모두 추가". 알림은 캘린더 앱이 담당하므로 앱 자체 푸시는 없음.

## 데이터 수정

`index.html` 안 `/*DATA-START*/ … /*DATA-END*/` JSON 만 고친다. 카드 필드: `t`(시각) `name` `memo`(`**굵게**` 가능) `cost`(엔) `lat/lng` 또는 `q`(지도 검색어). 한 카드가 여러 알림이면 `ics:[["20:00","제목"],…]`.

저장 키는 `localStorage` 의 `osaka2026:*` (done / ck / act / rate / day). 전부 지우려면 Safari 설정 → 웹사이트 데이터 삭제.
