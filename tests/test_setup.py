import os
import sys
import unittest

# append to path to import from chat_doc
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class TestSetup(unittest.TestCase):
    def test_config(self):
        from chat_doc.config import config

        required_keys = ["logging", "app", "credentials"]
        for key in required_keys:
            self.assertIn(key, config.keys())


if __name__ == "__main__":
    unittest.main()
