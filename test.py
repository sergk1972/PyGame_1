import unittest
from main import create_bonus


class Test_goose(unittest.TestCase):

    def test_1(self):
        self.assertEqual(len(create_bonus()), 3)


if __name__ == "main":
    unittest.main()
