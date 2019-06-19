import unittest
import Level_Design_Utilities
from collections import defaultdict


class TestLDU(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        pass

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_special_dict(self):
        result = Level_Design_Utilities.special_dict()
        self.assertIsInstance(result, defaultdict)
        self.assertIsInstance(result["test"], defaultdict)
        self.assertIsInstance(result["test"]["test"], list)


if __name__ == "__main__":
    unittest.main()
