import sys
import unittest

from socsim.avalanches.app import GetMatrixBase

class BaseMAtrixTest(unittest.TestCase):
    def setUp(self):
        self.matrix = GetMatrixBase(10, 1);
    def test_matrix(self):
        value = self.calc
        self.assertEqual(calc[0, 0], 1, FAILURE)



if __name__ == '__main__':
    import xmlrunner

    unittest.main(
        testRunner = xmlrunner.XMLTestRunner(output = 'test-reports'),
        failfast = False,
        buffer = False,
        catchbreak = False)