"""수집기 로직 테스트.

네트워크를 타지 않는다. fetch_json / fetch_text 를 갈아끼워 응답을 흉내내고,
파싱·필터·중복제거·실패처리만 확인한다. 픽스처는 실제 응답에서 구조만 남기고
줄인 것이다.

    python3 tools/test_job_scraper.py
"""

import datetime
import json
import os
import sys
import tempfile
import unittest
import urllib.error

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import job_scraper as js
import generate_job_html as gen


GREENHOUSE_FIXTURE = {
    "jobs": [
        {"id": 111, "title": "Senior Android Engineer (Shopping)",
         "absolute_url": "https://example.test/111",
         "updated_at": "2026-09-01T04:05:06Z"},
        {"id": 222, "title": "Staff iOS Engineer",
         "absolute_url": "https://example.test/222",
         "updated_at": "2026-08-20T10:00:00-07:00"},
        {"id": 333, "title": "Flutter Developer, k.ride",
         "absolute_url": "https://example.test/333",
         "updated_at": None},
        {"id": 444, "title": "Backend Engineer (Java)",
         "absolute_url": "https://example.test/444",
         "updated_at": "2026-09-02T00:00:00Z"},
        {"id": 555, "title": "Data Scientist",
         "absolute_url": "https://example.test/555",
         "updated_at": "2026-09-02T00:00:00Z"},
    ]
}

# 실제 api.lever.co/v0/postings/neowiz 응답에서 구조만 남기고 줄인 것.
# 최상위가 dict 가 아니라 배열이고, createdAt 이 epoch 밀리초다.
LEVER_FIXTURE = [
    {"id": "c3704f2e-5921-49f2-a9c2-8857696d846f",
     "text": "Android 클라이언트 프로그래머",
     "hostedUrl": "https://jobs.lever.co/neowiz/c3704f2e",
     "createdAt": 1774511583936},
    {"id": "5ad83a87-38c2-4441-81da-5ab73e3217fc",
     "text": "3D 캐릭터 모델러",
     "hostedUrl": "https://jobs.lever.co/neowiz/5ad83a87",
     "createdAt": 1785312618130},
    {"id": "8ec875e2-4a05-461e-9a91-0660f2f3981a",
     "text": "iOS 개발자",
     "hostedUrl": "https://jobs.lever.co/neowiz/8ec875e2",
     "createdAt": None},
]


def greeting_opening(opening_id, title, open_date):
    return {"deploy": True, "fixed": False, "openingId": opening_id,
            "title": title, "openDate": open_date, "dueDate": None,
            "workspaceDivision": {"id": 7, "division": "무신사"}}


# 실제 채용 홈 HTML의 __NEXT_DATA__ 를 그대로 축소한 것.
# 전체 공고 목록이 react-query 캐시(queryKey ["openings"])로 직렬화되어 들어온다.
def greeting_html(openings, with_openings_query=True):
    queries = [
        {"queryKey": ["publicCareer", "getCareerBaseInfo", "www"],
         "state": {"data": {}}},
    ]
    if with_openings_query:
        queries.append({"queryKey": ["openings"], "state": {"data": openings}})
    payload = {"buildId": "build-TfctsWXpff2fKS",
               "props": {"pageProps": {"dehydratedState": {
                   "mutations": [], "queries": queries}}}}
    return ('<html><body><script id="__NEXT_DATA__" '
            'type="application/json">' + json.dumps(payload, ensure_ascii=False)
            + '</script></body></html>')


GREETING_FIXTURE = [
    greeting_opening(30835, "[캐시워크] Flutter개발 병역특례",
                     "2023-06-27T00:09:49Z"),
    greeting_opening(30830, "[캐시워크] iOS개발 병역특례",
                     "2022-07-15T02:56:13Z"),
    greeting_opening(222714, "Backend Engineer (Catalog)",
                     "2026-09-08T00:47:55Z"),
    greeting_opening(235739, "Data Operations Lead", None),
]


WANTED_FIXTURE = {
    "data": [
        {"id": 900001, "position": "안드로이드 개발자",
         "company": {"name": "테스트컴퍼니"}},
        {"id": 900002, "position": "플러터 앱 개발자",
         "company": {"name": "플러터랩"}},
        {"id": 900003, "position": "백엔드 서버 개발자",
         "company": {"name": "서버사"}},
    ]
}


class TestClassify(unittest.TestCase):
    def test_track(self):
        cases = {
            "Flutter Developer": "Flutter",
            "플러터 앱 개발자": "Flutter",
            "React Native Engineer": "React Native",
            "Senior Android Engineer": "Android",
            "안드로이드 개발자": "Android",
            "iOS 앱 개발자": "iOS",
            "모바일 엔지니어": "기타 모바일",
        }
        for title, expected in cases.items():
            self.assertEqual(js.classify_track(title), expected, title)

    def test_flutter_beats_native(self):
        # Flutter 공고가 네이티브 이해를 요구해도 Flutter 트랙이어야 한다.
        self.assertEqual(
            js.classify_track("Flutter 개발자 (Android/iOS 경험 우대)"), "Flutter")

    def test_looks_mobile(self):
        self.assertTrue(js.looks_mobile("Android Engineer"))
        self.assertTrue(js.looks_mobile("Flutter 개발자"))
        self.assertTrue(js.looks_mobile("모바일 앱 개발자"))
        self.assertFalse(js.looks_mobile("Backend Engineer (Java)"))
        self.assertFalse(js.looks_mobile("Data Scientist"))
        self.assertFalse(js.looks_mobile("디자이너"))

    def test_mobile_first_wins(self):
        # 모바일 키워드가 앞에 있으면 뒤의 제외어에 걸리지 않는다.
        self.assertTrue(js.looks_mobile("Android 개발자 (서버 연동 경험 우대)"))
        # 반대로 웹 프론트 공고가 RN을 우대로 적은 경우는 제외한다.
        self.assertFalse(js.looks_mobile("프론트엔드 개발자 (React Native 우대)"))

    def test_ascii_keyword_needs_word_boundary(self):
        # 'app'이 Application/Applied 에 걸려 모바일 공고로 잡히던 오탐.
        # 실제로 수집돼 있던 제목들이다.
        self.assertFalse(js.looks_mobile("Application Security Engineer(자동화/취약점)"))
        self.assertFalse(js.looks_mobile("Applied Scientist II - Moloco Commerce Media"))
        self.assertFalse(js.looks_mobile("Application Architect, Professional Services"))
        self.assertFalse(js.looks_mobile("Deep Learning Applications Engineer"))
        # 'ios'가 Studios 에, 'mobile'이 automobile 에 걸리는 것도 같은 문제다.
        self.assertFalse(js.looks_mobile("Onetake Studios 3D 배경 모델러"))
        self.assertFalse(js.looks_mobile("Automobile Test Engineer"))
        # 'ml'이 HTML 에 걸려 제외어로 작동하던 것도 사라져야 한다.
        self.assertTrue(js.looks_mobile("Android 개발자 (HTML 렌더링)"))

    def test_word_boundary_keeps_real_matches(self):
        # 경계를 넣어도 진짜 모바일 공고는 그대로 걸려야 한다.
        self.assertTrue(js.looks_mobile("App Lead"))
        self.assertTrue(js.looks_mobile("Mobile Apps Engineer"))
        self.assertTrue(js.looks_mobile("Sr. Mobile App Developer"))
        # 한글이 바로 붙는 제목. \b 를 썼다면 여기서 죽는다.
        self.assertTrue(js.looks_mobile("[캐시워크] iOS개발 채용전환형 인턴"))
        self.assertTrue(js.looks_mobile("[캐시워크] Flutter개발 병역특례"))
        self.assertTrue(js.looks_mobile("Android/iOS 클라이언트 개발자"))

    def test_track_uses_same_boundary(self):
        # classify_track 도 같은 부분 문자열 문제를 갖고 있었다.
        self.assertEqual(js.classify_track("[캐시워크] iOS개발 병역특례"), "iOS")
        self.assertEqual(js.classify_track("Mobile Studios Engineer"), "기타 모바일")

    def test_non_dev_roles_dropped_wherever_they_are(self):
        # 모바일 키워드가 앞에 와도 개발 직군이 아니면 뺀다.
        for title in ("[UA팀] 모바일 게임 퍼포먼스 마케터 (주니어)",
                      "앱/웹 서비스 기획 (PM) (경력)",
                      "모바일 앱 디자이너"):
            self.assertFalse(js.looks_mobile(title), title)

    def test_marketing_team_name_is_not_a_role(self):
        # 팀 이름의 Marketing 때문에 진짜 모바일 엔지니어가 빠지면 안 된다.
        self.assertTrue(js.looks_mobile(
            "Staff Mobile Engineer [Marketing Product Engineering]"))

    def test_mobile_game_is_not_a_mobile_app_signal(self):
        self.assertFalse(js.looks_mobile(
            "MMORPG 온라인/모바일 게임 클라이언트 프로그래머 (C++, C#)"))
        # 플랫폼 이름이 따로 있으면 그쪽으로 잡힌다.
        self.assertTrue(js.looks_mobile("Android 게임 클라이언트 개발자"))


class TestStamp(unittest.TestCase):
    def test_utc_z(self):
        self.assertEqual(js.iso_to_stamp("2026-09-01T04:05:06Z"),
                         "2026-09-01 04:05:06")

    def test_offset_converted_to_utc(self):
        self.assertEqual(js.iso_to_stamp("2026-08-20T10:00:00-07:00"),
                         "2026-08-20 17:00:00")

    def test_bad_values(self):
        self.assertIsNone(js.iso_to_stamp(None))
        self.assertIsNone(js.iso_to_stamp(""))
        self.assertIsNone(js.iso_to_stamp("어제"))

    def test_epoch_ms(self):
        # Lever 는 ISO8601이 아니라 epoch 밀리초를 준다.
        self.assertEqual(js.epoch_ms_to_stamp(1774511583936),
                         "2026-03-26 07:53:03")

    def test_epoch_ms_bad_values(self):
        self.assertIsNone(js.epoch_ms_to_stamp(None))
        self.assertIsNone(js.epoch_ms_to_stamp(0))
        self.assertIsNone(js.epoch_ms_to_stamp("2026-03-26"))


class FakeResponse:
    def __init__(self, body):
        self.body = body

    def read(self):
        return self.body.encode('utf-8')

    def __enter__(self):
        return self

    def __exit__(self, *exc):
        return False


def http_error(code):
    return urllib.error.HTTPError('https://x.test', code, 'nope', {}, None)


class TestFetch(unittest.TestCase):
    """fetch_text 의 헤더 병합과 재시도. 실제 소켓도, 실제 대기도 없다."""

    def setUp(self):
        self._orig_urlopen = js.urllib.request.urlopen
        self._orig_sleep = js.time.sleep
        self.requests = []
        self.waits = []
        js.time.sleep = self.waits.append

    def tearDown(self):
        js.urllib.request.urlopen = self._orig_urlopen
        js.time.sleep = self._orig_sleep

    def respond_with(self, *outcomes):
        """호출 순서대로 하나씩 돌려준다. 예외 클래스면 올린다."""
        remaining = list(outcomes)

        def urlopen(req, timeout=None):
            self.requests.append(req)
            outcome = remaining.pop(0)
            if isinstance(outcome, Exception):
                raise outcome
            return FakeResponse(outcome)

        js.urllib.request.urlopen = urlopen

    def test_default_user_agent_is_sent(self):
        self.respond_with('ok')
        self.assertEqual(js.fetch_text('https://x.test'), 'ok')
        self.assertEqual(self.requests[0].get_header('User-agent'),
                         js.USER_AGENT)

    def test_headers_override_default(self):
        self.respond_with('ok')
        js.fetch_text('https://x.test', {'User-Agent': 'Chrome/140',
                                         'Referer': 'https://x.test/list'})
        sent = self.requests[0]
        self.assertEqual(sent.get_header('User-agent'), 'Chrome/140')
        self.assertEqual(sent.get_header('Referer'), 'https://x.test/list')

    def test_403_is_retried_then_succeeds(self):
        self.respond_with(http_error(403), 'ok')
        self.assertEqual(js.fetch_text('https://x.test'), 'ok')
        self.assertEqual(len(self.requests), 2)
        self.assertEqual(self.waits, [js.RETRY_WAITS[0]])

    def test_403_gives_up_and_reports_the_status(self):
        self.respond_with(*[http_error(403)] * (len(js.RETRY_WAITS) + 1))
        with self.assertRaises(js.SourceError) as caught:
            js.fetch_text('https://x.test')
        self.assertIn('HTTP 403', str(caught.exception))
        self.assertEqual(len(self.requests), len(js.RETRY_WAITS) + 1)
        self.assertEqual(self.waits, list(js.RETRY_WAITS))

    def test_404_is_not_retried(self):
        self.respond_with(http_error(404))
        with self.assertRaises(js.SourceError):
            js.fetch_text('https://x.test')
        self.assertEqual(len(self.requests), 1)
        self.assertEqual(self.waits, [])

    def test_network_error_is_retried(self):
        self.respond_with(urllib.error.URLError('끊김'), 'ok')
        self.assertEqual(js.fetch_text('https://x.test'), 'ok')
        self.assertEqual(len(self.requests), 2)


class TestScrapers(unittest.TestCase):
    def setUp(self):
        self._orig = js.fetch_json
        self._orig_text = js.fetch_text

    def tearDown(self):
        js.fetch_json = self._orig
        js.fetch_text = self._orig_text

    def test_greenhouse_filters_and_maps(self):
        js.fetch_json = lambda url, headers=None: GREENHOUSE_FIXTURE
        jobs = js.scrape_greenhouse("coupang", "쿠팡")

        self.assertEqual(len(jobs), 3)  # backend/data 제외
        self.assertEqual([j['track'] for j in jobs],
                         ['Android', 'iOS', 'Flutter'])
        self.assertEqual(jobs[0]['id'], 'greenhouse_coupang_111')
        self.assertEqual(jobs[0]['company'], '쿠팡')
        self.assertEqual(jobs[0]['posted_at'], '2026-09-01 04:05:06')
        self.assertIsNone(jobs[2]['posted_at'])

    def test_greenhouse_bad_shape_raises(self):
        js.fetch_json = lambda url, headers=None: {"unexpected": []}
        with self.assertRaises(js.SourceError):
            js.scrape_greenhouse("nope", "없는회사")

    def test_lever_filters_and_maps(self):
        js.fetch_json = lambda url, headers=None: LEVER_FIXTURE
        jobs = js.scrape_lever("neowiz", "네오위즈")

        self.assertEqual(len(jobs), 2)  # 3D 모델러 제외
        self.assertEqual([j['track'] for j in jobs], ['Android', 'iOS'])
        self.assertEqual(jobs[0]['id'],
                         'lever_neowiz_c3704f2e-5921-49f2-a9c2-8857696d846f')
        self.assertEqual(jobs[0]['platform'], 'Lever')
        self.assertEqual(jobs[0]['job_url'],
                         'https://jobs.lever.co/neowiz/c3704f2e')
        self.assertEqual(jobs[0]['posted_at'], '2026-03-26 07:53:03')
        self.assertIsNone(jobs[1]['posted_at'])

    def test_lever_location_filter_goes_into_url(self):
        # 글로벌 보드는 서울 공고만 받아야 한다. 필터가 URL 에 실려야 한다.
        seen = []
        js.fetch_json = lambda url, headers=None: seen.append(url) or []
        js.scrape_lever("matchgroup", "매치그룹", "Seoul, South Korea")
        js.scrape_lever("neowiz", "네오위즈")
        self.assertIn("&location=Seoul%2C%20South%20Korea", seen[0])
        self.assertNotIn("location=", seen[1])

    def test_lever_bad_shape_raises(self):
        # 계정이 사라지면 배열이 아니라 {"ok": false} 가 온다.
        js.fetch_json = lambda url, headers=None: {"ok": False, "error": "Document not found"}
        with self.assertRaises(js.SourceError):
            js.scrape_lever("nope", "없는회사")

    def test_lever_bad_posting_shape_raises(self):
        js.fetch_json = lambda url, headers=None: [{"id": "1", "title": "제목 키가 바뀐 경우"}]
        with self.assertRaises(js.SourceError):
            js.scrape_lever("neowiz", "네오위즈")

    def test_greetinghr_filters_and_maps(self):
        js.fetch_text = lambda url, headers=None: greeting_html(GREETING_FIXTURE)
        jobs = js.scrape_greetinghr("cashwalk12", "넛지헬스케어(캐시워크)")

        self.assertEqual(len(jobs), 2)  # backend/data 제외
        self.assertEqual([j['track'] for j in jobs], ['Flutter', 'iOS'])
        self.assertEqual(jobs[0]['id'], 'greeting_cashwalk12_30835')
        self.assertEqual(jobs[0]['platform'], '그리팅')
        self.assertEqual(
            jobs[0]['job_url'],
            'https://cashwalk12.career.greetinghr.com/o/30835')
        self.assertEqual(jobs[0]['posted_at'], '2023-06-27 00:09:49')

    def test_greetinghr_empty_openings_is_not_an_error(self):
        # 공고가 0건인 회사는 정상이다. 실패로 집계하면 매주 헛경고가 뜬다.
        js.fetch_text = lambda url, headers=None: greeting_html([])
        self.assertEqual(js.scrape_greetinghr("xyz", "엑스와이지"), [])

    def test_greetinghr_missing_next_data_raises(self):
        # SSR 구조가 바뀌면 조용히 0건이 아니라 실패로 끝나야 한다.
        js.fetch_text = lambda url, headers=None: '<html><body>공고 목록</body></html>'
        with self.assertRaises(js.SourceError):
            js.scrape_greetinghr("musinsa", "무신사")

    def test_greetinghr_missing_openings_query_raises(self):
        js.fetch_text = lambda url, headers=None: greeting_html([], with_openings_query=False)
        with self.assertRaises(js.SourceError):
            js.scrape_greetinghr("musinsa", "무신사")

    def test_greetinghr_bad_openings_shape_raises(self):
        js.fetch_text = lambda url, headers=None: greeting_html({"data": []})
        with self.assertRaises(js.SourceError):
            js.scrape_greetinghr("musinsa", "무신사")

    def test_greetinghr_broken_next_data_json_raises(self):
        js.fetch_text = lambda url, headers=None: (
            '<script id="__NEXT_DATA__" type="application/json">'
            '{not json</script>')
        with self.assertRaises(js.SourceError):
            js.scrape_greetinghr("musinsa", "무신사")

    def test_greetinghr_missing_opening_id_raises(self):
        js.fetch_text = lambda url, headers=None: greeting_html(
            [{"title": "안드로이드 개발자", "openDate": "2026-09-01T00:00:00Z"}])
        with self.assertRaises(js.SourceError):
            js.scrape_greetinghr("musinsa", "무신사")

    def test_wanted_filters(self):
        js.fetch_json = lambda url, headers=None: WANTED_FIXTURE
        jobs = js.scrape_wanted()
        self.assertEqual(len(jobs), 2)
        self.assertEqual(jobs[0]['id'], 'wanted_900001')
        self.assertEqual(jobs[1]['track'], 'Flutter')

    def test_wanted_bad_shape_raises(self):
        js.fetch_json = lambda url, headers=None: {"nope": 1}
        with self.assertRaises(js.SourceError):
            js.scrape_wanted()


class TestCollect(unittest.TestCase):
    def test_partial_failure_keeps_going(self):
        def ok():
            return [{'id': 'x', 'title': 'Android', 'company': 'A'}]

        def boom():
            raise js.SourceError("죽음")

        jobs, per_source, failures = js.collect(
            [("good", ok), ("bad", boom)])

        self.assertEqual(len(jobs), 1)
        self.assertEqual(per_source, {"good": 1})
        self.assertEqual(len(failures), 1)
        self.assertEqual(failures[0][0], "bad")

    def test_all_failing_yields_nothing(self):
        def boom():
            raise js.SourceError("죽음")

        jobs, per_source, failures = js.collect([("a", boom), ("b", boom)])
        self.assertEqual(jobs, [])
        self.assertEqual(len(failures), 2)


class TestSave(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.NamedTemporaryFile(
            suffix='.json', delete=False, mode='w', encoding='utf-8')
        self.tmp.write('[]')
        self.tmp.close()
        self._orig_path = js.DB_PATH
        js.DB_PATH = self.tmp.name

    def tearDown(self):
        js.DB_PATH = self._orig_path
        os.unlink(self.tmp.name)

    def read(self):
        with open(self.tmp.name, encoding='utf-8') as f:
            return json.load(f)

    def test_insert_then_update(self):
        job = {'id': 'greenhouse_coupang_1', 'platform': 'Greenhouse',
               'title': 'Android Engineer', 'company': '쿠팡',
               'job_url': 'u', 'track': 'Android', 'posted_at': None}

        new, updated = js.save_jobs([dict(job)])
        self.assertEqual((new, updated), (1, 0))

        new, updated = js.save_jobs([dict(job)])
        self.assertEqual((new, updated), (0, 1))
        self.assertEqual(len(self.read()), 1)

    def test_cross_platform_dedup_merges_platform(self):
        js.save_jobs([{
            'id': 'wanted_1', 'platform': 'Wanted',
            'title': 'Senior Android Engineer', 'company': '쿠팡',
            'job_url': 'u', 'track': 'Android', 'posted_at': None}])

        # 같은 회사·같은 제목이 다른 플랫폼으로 들어오면 합쳐진다.
        new, updated = js.save_jobs([{
            'id': 'greenhouse_coupang_9', 'platform': 'Greenhouse',
            'title': 'Senior Android Engineer', 'company': '쿠팡',
            'job_url': 'u2', 'track': 'Android', 'posted_at': None}])

        rows = self.read()
        self.assertEqual((new, updated), (0, 1))
        self.assertEqual(len(rows), 1)
        self.assertIn('Wanted', rows[0]['platform'])
        self.assertIn('Greenhouse', rows[0]['platform'])

    def test_posted_at_backfilled(self):
        js.save_jobs([{
            'id': 'g_1', 'platform': 'Greenhouse', 'title': 'Android 개발자',
            'company': 'A', 'job_url': 'u', 'track': 'Android',
            'posted_at': None}])

        js.save_jobs([{
            'id': 'g_1', 'platform': 'Greenhouse', 'title': 'Android 개발자',
            'company': 'A', 'job_url': 'u', 'track': 'Android',
            'posted_at': '2026-09-01 00:00:00'}])

        self.assertEqual(self.read()[0]['posted_at'], '2026-09-01 00:00:00')

    def test_different_companies_not_merged(self):
        js.save_jobs([{'id': 'a', 'platform': 'Wanted', 'title': 'Android 개발자',
                       'company': '회사A', 'job_url': 'u', 'track': 'Android'}])
        new, _ = js.save_jobs([{'id': 'b', 'platform': 'Wanted',
                                'title': 'Android 개발자', 'company': '회사B',
                                'job_url': 'u', 'track': 'Android'}])
        self.assertEqual(new, 1)
        self.assertEqual(len(self.read()), 2)


class TestGenerate(unittest.TestCase):
    def setUp(self):
        self.now = datetime.datetime(2026, 9, 8, 0, 0, 0)

    def stamp(self, days_ago):
        return (self.now - datetime.timedelta(days=days_ago)
                ).strftime('%Y-%m-%d %H:%M:%S')

    def test_active_window(self):
        jobs = [
            {'id': '1', 'last_seen_at': self.stamp(0)},
            {'id': '2', 'last_seen_at': self.stamp(7)},
            {'id': '3', 'last_seen_at': self.stamp(30)},   # 창 밖
            {'id': '4'},                                    # 값 없음
        ]
        active = gen.select_active(jobs, self.now)
        self.assertEqual({j['id'] for j in active}, {'1', '2'})

    def test_grouping_uses_track_then_falls_back(self):
        jobs = [
            {'id': '1', 'title': '아무 제목', 'track': 'Flutter',
             'last_seen_at': self.stamp(0), 'created_at': self.stamp(0)},
            # track 없는 과거 데이터는 제목으로 분류한다.
            {'id': '2', 'title': 'iOS 개발자',
             'last_seen_at': self.stamp(0), 'created_at': self.stamp(5)},
        ]
        grouped = gen.group_by_track(gen.select_active(jobs, self.now), self.now)
        self.assertEqual(len(grouped['Flutter']), 1)
        self.assertEqual(len(grouped['iOS']), 1)

    def test_new_badge_only_for_fresh(self):
        jobs = [
            # 이번 실행에서 처음 본 공고
            {'id': '1', 'title': '갓 발견한 Android', 'track': 'Android',
             'last_seen_at': self.stamp(0), 'created_at': self.stamp(0)},
            # 지난주부터 있던 공고 — 이번에도 보였을 뿐 신규가 아니다
            {'id': '2', 'title': '지난주부터 있던 Android', 'track': 'Android',
             'last_seen_at': self.stamp(0), 'created_at': self.stamp(5)},
        ]
        grouped = gen.group_by_track(gen.select_active(jobs, self.now), self.now)
        flags = {j['title']: j['is_new'] for j in grouped['Android']}
        self.assertTrue(flags['갓 발견한 Android'])
        self.assertFalse(flags['지난주부터 있던 Android'])

    def test_card_escapes_html(self):
        card = gen.render_card({
            'title': '<script>alert(1)</script>', 'company': 'A & B',
            'platform': 'Wanted', 'url': 'https://x.test/?a=1&b=2',
            'is_new': False, 'posted': None})
        self.assertNotIn('<script>', card)
        self.assertIn('&lt;script&gt;', card)
        self.assertIn('&amp;', card)


if __name__ == '__main__':
    unittest.main(verbosity=2)
