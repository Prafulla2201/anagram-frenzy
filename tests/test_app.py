import os
import sys
import unittest

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SRC_DIR = os.path.join(ROOT_DIR, "src")
for p in (ROOT_DIR, SRC_DIR):
    if p not in sys.path:
        sys.path.insert(0, p)

try:
    from src.app import app
    from src import seed_data
except ImportError:
    from app import app
    import seed_data


class TestCommercialApplicationE2E(unittest.TestCase):
    def setUp(self):
        app.config["TESTING"] = True
        self.client = app.test_client()
        self.client.post("/api/reset")

    def test_01_root_serves_interactive_spa(self):
        resp = self.client.get("/")
        self.assertEqual(resp.status_code, 200)
        html = resp.data.decode("utf-8", errors="ignore").lower()
        self.assertIn("<html", html)
        self.assertIn("<script", html)
        self.assertIn("word-meaning-drawer", html)
        self.assertIn("inspectunlockedwordmeaning", html)

    def test_02_health_endpoint(self):
        resp = self.client.get("/health")
        self.assertEqual(resp.status_code, 200)
        data = resp.get_json()
        self.assertEqual(data.get("status"), "healthy")

    def test_03_catalog_and_search_filtering(self):
        resp = self.client.get("/api/catalog")
        self.assertEqual(resp.status_code, 200)
        data = resp.get_json()
        self.assertIn("items", data)
        self.assertIn("personas", data)
        self.assertGreater(len(data["items"]), 0)
        self.assertGreater(len(data["personas"]), 0)

    def test_04_end_to_end_interactive_verification_flow(self):
        cat_resp = self.client.get("/api/catalog")
        items = cat_resp.get_json().get("items", [])
        first_item = items[0]

        # Happy path: submit correct answer
        post_resp = self.client.post(
            "/api/interact",
            json={
                "item_id": first_item["id"],
                "selected_option": first_item.get("quiz_answer", ""),
            },
        )
        self.assertEqual(post_resp.status_code, 200)
        result = post_resp.get_json()
        self.assertTrue(result.get("correct"))
        self.assertGreater(result.get("score_delta", 0), 0)

        # Edge path: submit wrong option
        wrong_resp = self.client.post(
            "/api/interact",
            json={
                "item_id": first_item["id"],
                "selected_option": "__definitely_wrong_choice__",
            },
        )
        self.assertEqual(wrong_resp.status_code, 200)
        self.assertFalse(wrong_resp.get_json().get("correct"))

    def test_05_v13_rejects_invalid_english_words(self):
        # Non-English / gibberish words must be rejected during word entry
        bad_resp = self.client.post("/api/word/analyze", json={"word": "asdfgh"})
        self.assertEqual(bad_resp.status_code, 400)
        bad_data = bad_resp.get_json()
        self.assertFalse(bad_data.get("valid"))
        self.assertEqual(bad_data.get("reason"), "not_english_word")

        # Valid English word must succeed and return word_meaning
        good_resp = self.client.post("/api/word/analyze", json={"word": "earth"})
        self.assertEqual(good_resp.status_code, 200)
        good_data = good_resp.get_json()
        self.assertTrue(good_data.get("valid"))
        self.assertTrue(good_data.get("has_anagrams"))
        self.assertIn("word_meaning", good_data)
        self.assertEqual(good_data["word_meaning"].get("word"), "earth")

    def test_06_v13_guess_anagram_and_click_meaning(self):
        # Start game on 'earth'
        self.client.post("/api/word/analyze", json={"word": "earth"})

        # Non-English guess with same letters ('htraa' / 'htrae') must be rejected as non-English
        non_english_guess = self.client.post(
            "/api/word/guess",
            json={"base_word": "earth", "guess": "htrae"},
        )
        self.assertEqual(non_english_guess.status_code, 200)
        ne_data = non_english_guess.get_json()
        self.assertFalse(ne_data.get("correct"))
        self.assertEqual(ne_data.get("status"), "not_english_word")

        # Valid English anagram guess ('heart') unlocks the word and returns its meaning
        valid_guess = self.client.post(
            "/api/word/guess",
            json={"base_word": "earth", "guess": "heart"},
        )
        self.assertEqual(valid_guess.status_code, 200)
        vg_data = valid_guess.get_json()
        self.assertTrue(vg_data.get("correct"))
        self.assertIn("heart", vg_data.get("unlocked_targets", []))
        self.assertIn("heart", vg_data.get("unlocked_meanings", {}))
        self.assertTrue(len(vg_data["unlocked_meanings"]["heart"].get("definition", "")) > 10)

        # Clicking an unlocked anagram word queries /api/word/meaning
        meaning_resp = self.client.get("/api/word/meaning?word=heart")
        self.assertEqual(meaning_resp.status_code, 200)
        meaning_data = meaning_resp.get_json()
        self.assertEqual(meaning_data.get("word"), "heart")
        self.assertTrue(meaning_data.get("is_valid"))
        self.assertIn("organ", meaning_data.get("definition", "").lower())

    def test_07_daily_challenge_endpoint(self):
        resp = self.client.get("/api/daily")
        self.assertEqual(resp.status_code, 200)
        data = resp.get_json()
        self.assertIn("word", data)
        self.assertIn("puzzle_number", data)
        self.assertIn("theme", data)
        self.assertGreater(data.get("target_count", 0), 0)
        self.assertTrue(len(data.get("target_words", [])) > 0)


if __name__ == "__main__":
    unittest.main()
