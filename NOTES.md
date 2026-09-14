# NOTES

## 2026-09-14
- 워크스페이스 생성 (회사 업무와 분리). 과제 정의 대기.
- 과제 확정: 오사카 여행 웹앱. 폴더 devproj → osaka-trip. index.html + osaka-trip.ics + 아이콘 완성.
- 검증: jsdom 스모크(탭 4개, 완료/체크/예산 입력·환율·localStorage, 9/20 13:00 시뮬레이션 next=이시바시) 오류 0. 실기기(iPhone Safari) 확인은 사용자.
- 미확정: 신파치 쇼쿠도 지점(지도 검색어 "しんぱち食堂 天神橋筋" 으로 넣음), 이시바시/이케베/미키가키는 좌표 없이 상호 검색.
- 배포: GitHub Pages 는 사용자 결정(개인 일정이 공개 repo 에 올라감). private repo + Pages 는 GitHub Pro 필요.
- 09-14 배포: https://github.com/MAYFCHOI/osaka-trip (public) → GitHub Pages https://mayfchoi.github.io/osaka-trip/ (main, root). index/icon/ics 전부 200 확인. 아이폰 실기기 확인 대기.
- 09-14 리뷰 반영(UX 13건 + 코드 15건 중 21건): 자정/앱복귀 시 날짜 자동 전환, 지도 링크 → 도보 길찾기(지하철 카드는 transit), 매일 체크리스트 날짜별 키(d{N}-) + 오늘만 초기화, 지난 카드 접기(다음 앞 1장만), 예산 일별 소계, ink3 대비 #948a78, 다음 배지 글자색, 카드 지도 링크 44px, 탭별 스크롤 위치 기억, 키패드 닫힘 후 body 원위치, lang=ja, aria-label. ICS: 23:30 카드 DTEND 자정 넘김(T240000 버그), 공연 1/2세트 겹침 해소, LOCATION 은 검색어 있을 때만 + X-APPLE-STRUCTURED-LOCATION, METHOD 제거. 참고 탭에 .ics 링크.
- 보류(P3): 잔여 현금 계산기, 문구 복사 버튼. 실기기 확인 필요: 홈화면 앱에서 지도 링크가 구글맵 앱으로 넘어가는지, details 4개 탭 동작, 비행기 모드 첫 실행(README 오프라인 주의 참고).
- 09-14 실기기 확인: 홈 화면 앱에서 카드 장소 탭 → 구글맵 앱으로 바로 넘어감 (Safari 경유 없음). 비행기 모드 첫 실행은 사용자 테스트 예정.
- 09-14 비행기 모드 확인: 홈 화면 앱 오프라인 실행 OK (사용자). 서비스워커 불필요로 확정. 오프라인은 실제로 기내 정도만 해당.
