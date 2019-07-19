# coding=utf-8
import pdb
import os
import sys
sys.path.append(os.path.join(os.path.abspath(os.path.dirname(__file__)), "../"))
from calc.standup_people import StandUp

import unittest

class TestStandUp(unittest.TestCase):
    """
    StandUp
    """
    def test_stand_up_run(self):
        """
        run
        """
        self.assertEqual(0, StandUp(1, 0, 0).run())
        self.assertEqual(2, StandUp(5, 1, 3).run())
        self.assertEqual(7, StandUp(100, 1, 10).run())


if __name__ == "__main__":
    unittest.main()