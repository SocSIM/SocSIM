"""
Starts Self-organized criticality
"""

from SOC.models.avalanches.app import MainLoop

def run():
    """
    Run MainLoop
    """
    print("Hello World")
    MainLoop(100)
    print("lalala")

if __name__ == '__main__':
    print("app")
    run()