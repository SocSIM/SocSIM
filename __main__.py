"""
main main
"""

import app
import common #initialize logging
import logging


common.log.info("MAIN")

def main():
    """
    This function does something.

    :param name: The name to use.
    :type name: str.
    :param state: Current state to be in.
    :type state: bool.
    :returns:  int -- the return code.
    :raises: AttributeError, KeyError

    """
    app.run()

if __name__ == '__main__':
    main()