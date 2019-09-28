"""
Starts Self-organized criticality some loop
"""

from SOC.models.avalanches import MainLoop
import common
import logging

common.log.info("APP")

def run():
    """
    Run MainLoop
    """
    common.log.info("STARTED")
    MainLoop(100)
    common.log.info("FINISHED")

if __name__ == '__main__':
    run()