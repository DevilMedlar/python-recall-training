from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from senpai_bot.context import CHAT_BEHAVIOR_ANCHOR, build_startup_context
from senpai_bot.ollama_client import OllamaClient
from senpai_bot.state import prepare_messages


class _FakeResponse:
    def __init__(self, body: dict) -> None:
        self.body = json.dumps(body).encode("utf-8")

    def __enter__(self):
        return self

    def __exit__(self, *_args):
        return False

    def read(self) -> bytes:
        return self.body


class ContextTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.root = Path(self.temp_dir.name)
        for name in ("README.md", "rules.md", "SECURITY.md"):
            (self.root / name).write_text(f"full contents of {name}", encoding="utf-8")

    def tearDown(self) -> None:
        self.temp_dir.cleanup()

    def test_compact_context_keeps_persona_and_omits_contract_bodies(self) -> None:
        prompt = build_startup_context(self.root, "PERSONA_MARKER", "compact")

        self.assertIn("PERSONA_MARKER", prompt)
        self.assertIn(CHAT_BEHAVIOR_ANCHOR, prompt)
        self.assertNotIn("full contents of rules.md", prompt)
        self.assertLess(len(prompt), 5000)
        self.assertLess(prompt.index("PERSONA_MARKER"), prompt.index(CHAT_BEHAVIOR_ANCHOR))

    def test_full_context_places_persona_after_contract(self) -> None:
        prompt = build_startup_context(self.root, "PERSONA_MARKER", "full")

        self.assertIn("full contents of rules.md", prompt)
        self.assertGreater(prompt.index("PERSONA_MARKER"), prompt.index("full contents of rules.md"))
        self.assertTrue(prompt.endswith(CHAT_BEHAVIOR_ANCHOR))


class StateTests(unittest.TestCase):
    def test_changed_system_prompt_discards_poisoned_history(self) -> None:
        old = [
            {"role": "system", "content": "old prompt"},
            {"role": "user", "content": "hey"},
            {"role": "assistant", "content": "generic broken reply"},
        ]

        prepared, reset = prepare_messages(old, "new prompt", 24)

        self.assertTrue(reset)
        self.assertEqual(prepared, [{"role": "system", "content": "new prompt"}])

    def test_history_limit_starts_at_a_user_message(self) -> None:
        messages = [{"role": "system", "content": "prompt"}]
        for number in range(10):
            messages.extend(
                [
                    {"role": "user", "content": f"question {number}"},
                    {"role": "assistant", "content": f"answer {number}"},
                ]
            )

        prepared, reset = prepare_messages(messages, "prompt", 5)

        self.assertTrue(reset)
        self.assertEqual(prepared[0]["role"], "system")
        self.assertEqual(prepared[1]["role"], "user")
        self.assertLessEqual(len(prepared) - 1, 5)


class OllamaClientTests(unittest.TestCase):
    @patch("senpai_bot.ollama_client.urllib.request.urlopen")
    def test_num_ctx_is_sent_as_an_ollama_option(self, urlopen) -> None:
        urlopen.return_value = _FakeResponse(
            {"message": {"role": "assistant", "content": "hello"}}
        )
        client = OllamaClient("http://localhost:11434", "test-model", num_ctx=8192)

        reply = client.chat([{"role": "user", "content": "hi"}])

        request = urlopen.call_args.args[0]
        payload = json.loads(request.data.decode("utf-8"))
        self.assertEqual(payload["options"], {"num_ctx": 8192})
        self.assertEqual(reply["content"], "hello")


if __name__ == "__main__":
    unittest.main()
