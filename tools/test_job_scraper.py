"""수집기 로직 테스트.

네트워크를 타지 않는다. fetch_json 을 갈아끼워 응답을 흉내내고,
파싱·필터·중복제거·실패처리만 확인한다.

    python3 tools/test_job_scraper.py
"""

import datetime
import json
import os
import sys
import tempfile
import unittest

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


class TestScrapers(unittest.TestCase):
    def setUp(self):
        self._orig = js.fetch_json

    def tearDown(self):
        js.fetch_json = self._orig

    def test_greenhouse_filters_and_maps(self):
        js.fetch_json = lambda url: GREENHOUSE_FIXTURE
        jobs = js.scrape_greenhouse("coupang", "쿠팡")

        self.assertEqual(len(jobs), 3)  # backend/data 제외
        self.assertEqual([j['track'] for j in jobs],
                         ['Android', 'iOS', 'Flutter'])
        self.assertEqual(jobs[0]['id'], 'greenhouse_coupang_111')
        self.assertEqual(jobs[0]['company'], '쿠팡')
        self.assertEqual(jobs[0]['posted_at'], '2026-09-01 04:05:06')
        self.assertIsNone(jobs[2]['posted_at'])

    def test_greenhouse_bad_shape_raises(self):
        js.fetch_json = lambda url: {"unexpected": []}
        with self.assertRaises(js.SourceError):
            js.scrape_greenhouse("nope", "없는회사")

    def test_wanted_filters(self):
        js.fetch_json = lambda url: WANTED_FIXTURE
        jobs = js.scrape_wanted()
        self.assertEqual(len(jobs), 2)
        self.assertEqual(jobs[0]['id'], 'wanted_900001')
        self.assertEqual(jobs[1]['track'], 'Flutter')

    def test_wanted_bad_shape_raises(self):
        js.fetch_json = lambda url: {"nope": 1}
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
