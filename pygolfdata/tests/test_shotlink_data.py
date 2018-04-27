import unittest

from data import shotlink

class ShotsTests(unittest.TestCase):
   def test_get_shots_exists(self):
       shotlink.get_shots()
