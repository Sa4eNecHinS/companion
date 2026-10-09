"""Component checks that need no ROS, microphone, model, or API connection."""

import unittest
from unittest.mock import patch

import numpy as np

from lwitch.audio.buffer import AudioBuffer
from lwitch.audio.chunker import AudioChunker
from lwitch.audio.resampler import AudioResampler
from lwitch.waf.security.rate_limiter import RateLimiter
from lwitch.waf.security.sanitizer import sanitize_input
from lwitch.waf.security.sql_detector import detect_sql_injection


class AudioTests(unittest.TestCase):
    def test_buffer_drops_oldest_chunk(self):
        buffer = AudioBuffer()
        for value in range(31):
            buffer.push(value)
        self.assertEqual(len(buffer), 30)
        self.assertEqual(buffer.dropped_chunks, 1)
        self.assertEqual(buffer.pop(), 1)

    def test_resampler_keeps_incomplete_group(self):
        resampler = AudioResampler()
        # Microphone blocks have shape (samples, 1).
        first = np.arange(4, dtype=np.float32).reshape(-1, 1)
        second = np.arange(4, 9, dtype=np.float32).reshape(-1, 1)
        np.testing.assert_allclose(resampler.convert_to_16k(first), [1])
        np.testing.assert_allclose(resampler.convert_to_16k(second), [4, 7])
        self.assertEqual(resampler.buffer, [])

    def test_chunker_preserves_tail_between_calls(self):
        chunker = AudioChunker()
        chunks = chunker.get_chunks(np.arange(500, dtype=np.float32))
        self.assertEqual(chunks.shape, (1, 480))
        np.testing.assert_array_equal(chunks[0], np.arange(480))
        chunks = chunker.get_chunks(np.arange(500, 960, dtype=np.float32))
        np.testing.assert_array_equal(chunks[0], np.arange(480, 960))
        self.assertEqual(chunker.buffer, [])

    def test_chunker_waits_for_full_frame(self):
        chunker = AudioChunker()
        self.assertEqual(chunker.get_chunks(np.ones(100)), [])
        self.assertEqual(chunker.get_chunks(np.ones(100)), [])
        self.assertEqual(chunker.get_chunks(np.ones(280)).shape, (1, 480))


class FilterTests(unittest.TestCase):
    def test_sanitizer_normalizes_control_bytes_and_whitespace(self):
        text, changes = sanitize_input("  hello\x00\n world  ")
        self.assertEqual(text, "hello world")
        self.assertIn("removed null bytes", changes)
        self.assertIn("collapsed whitespace", changes)

    def test_sanitizer_enforces_length(self):
        text, changes = sanitize_input("abcdef", max_length=3)
        self.assertEqual(text, "abc")
        self.assertIn("truncated to 3 chars", changes)

    def test_detector_checks_original_and_normalized_input(self):
        self.assertEqual(detect_sql_injection("DROP TABLE users"), "DROP TABLE")
        text, _ = sanitize_input("UNION\\x00 SELECT")
        self.assertEqual(detect_sql_injection(text), "UNION SELECT")
        self.assertIsNone(detect_sql_injection("Привет!"))

    def test_rate_limit_is_per_user(self):
        limiter = RateLimiter(max_requests=1)
        self.assertTrue(limiter.allow("alice"))
        self.assertFalse(limiter.allow("alice"))
        self.assertTrue(limiter.allow("bob"))

    def test_rate_limit_expires(self):
        with patch("lwitch.waf.security.rate_limiter.monotonic") as clock:
            clock.return_value = 100
            limiter = RateLimiter(max_requests=1, window_seconds=60)
            self.assertTrue(limiter.allow())
            clock.return_value = 159
            self.assertFalse(limiter.allow())
            clock.return_value = 161
            self.assertTrue(limiter.allow())


if __name__ == "__main__":
    unittest.main()
