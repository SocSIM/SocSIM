"""
test_avalanches.
"""

from SOC.models import avalanches
import numpy

def test_mainloop():
    """
    Tests that the `avalanches` model runs without exceptions.
    """

    avalanches.MainLoop(100)
