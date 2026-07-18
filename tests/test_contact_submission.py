import json
import tempfile
import unittest
from pathlib import Path

import serve


class ContactSubmissionTests(unittest.TestCase):
    def test_save_contact_message_writes_payload_to_jsonl(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            output_path = Path(tmpdir) / "messages.jsonl"
            payload = {
                "name": "Ada Lovelace",
                "email": "ada@example.com",
                "subject": "Hello",
                "message": "Testing the contact flow"
            }

            result = serve.save_contact_message(payload, output_path=output_path)

            self.assertTrue(result["saved"])
            self.assertTrue(output_path.exists())
            line = output_path.read_text(encoding="utf-8").strip()
            data = json.loads(line)
            self.assertEqual(data["name"], "Ada Lovelace")
            self.assertEqual(data["email"], "ada@example.com")
            self.assertEqual(data["subject"], "Hello")
            self.assertEqual(data["message"], "Testing the contact flow")


if __name__ == "__main__":
    unittest.main()
