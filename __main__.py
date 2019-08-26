"""
Main Class [SocSim]. 
This program will run avalanche simulation
"""

import app
import common #initialize logging
import logging


common.log.info("MAIN")

def main():
    """
    Avalanche simulation
    """
    app.run()

if __name__ == '__main__':
    main()