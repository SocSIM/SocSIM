"""
Main Init

Here can be placed some general description  of SOCSIM program and how to use it.

Some directives to test functionality

.. figure:: images/SOC0.png
    :scale: 50 %
    :alt: map to buried treasure

    This is the caption of the figure (a simple paragraph).

    The legend consists of all elements after the caption.

.. autofunction:: socsim.run
    :noindex:

"""

from SOC.models.avalanches import MainLoop
import common
import logging

common.log.info("INIT")

def run():
    """
    Run MainLoop
    """
    common.log.info("STARTED")
    MainLoop(100)
    common.log.info("FINISHED")

if __name__ == '__main__':
    run()