"""
test_avalanches.

"""

import sys
import unittest
from SOC.models.avalanches import GetMatrixBase

class BaseMatrixTest(unittest.TestCase):
    """BaseMatrixTest"""

    def setUp(self):
        """setUp"""
        self.matrix = GetMatrixBase(10, 1)

    def test_matrix(self):
        """test_matrix"""
        value = self.matrix
        self.assertEqual(value[0, 0], 1)



if __name__ == '__main__':
    import xmlrunner

    unittest.main(
        testRunner = xmlrunner.XMLTestRunner(output = 'test-reports'),
        failfast = False,
        buffer = False,
        catchbreak = False)