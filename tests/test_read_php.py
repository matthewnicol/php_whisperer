import unittest
from read_php import read_php

class TestReadPHP(unittest.TestCase):
    def test_extraction(self):
        self.assertEqual(read_php(
           "test_load_array_1.php"
        ),
            {
                "array_key": "array_value",
                "another_key": 6,
                "third_key": ["k", "v", "g"],
            }
        )

    def test_extraction_2(self):
        self.assertEqual(
            read_php("test_load_array_2.php", variable="second_array"),
            [{"array_key": "array_value"}]
        )