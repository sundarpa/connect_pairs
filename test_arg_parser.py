import unittest
from arg_parser import parse_argv
from tquery import fetch_data_from_csv

class TestParseArgv(unittest.TestCase):

    def test_with_key_value(self):
        argv = ["--name", "Kushi", "--age", "25"]
        opts = parse_argv(argv)
        self.assertEqual(opts, {"name": "Kushi", "age": "25"})

    def test_without_value(self):
        argv = ["--h","--help"]
        opts = parse_argv(argv)
        self.assertEqual(opts, {"h": None, "help":None })

    def test_multiple_key_values(self):
        argv = ["--h", "help", "--help", "h"]
        opts = parse_argv(argv)
        self.assertEqual(opts, {"h": "help", "help": "h"})

    def test_invalid_argument(self):
        argv = ["help"]
        opts = parse_argv(argv)
        self.assertEqual(opts, {"Error: Invalid argument help {}"})

    def test_empty_keys(self):
        argv = ["--"]
        opts = parse_argv(argv)
        self.assertEqual(opts, {"": None})

    def test_empty_input(self):
        argv = []
        opts = parse_argv(argv)
        self.assertEqual(opts, {})


if __name__ == "__main__":
    unittest.main()
