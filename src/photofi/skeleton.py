# -*- coding: utf-8 -*-
"""
This is a skeleton file that can serve as a starting point for a Python
console script. To run this script uncomment the following lines in the
[options.entry_points] section in setup.cfg:

    console_scripts =
         fibonacci = photofi.skeleton:run

Then run `python setup.py install` which will install the command `fibonacci`
inside your current environment.
Besides console scripts, the header (i.e. until _logger...) of this file can
also be used as template for Python modules.

Note: This skeleton file can be safely removed if not needed!
"""

import argparse
import logging
import sys
from pathlib import Path as Path

from photofi import __version__
from photofi import core

__author__ = "Julien Hoffmann"
__copyright__ = "Julien Hoffmann"
__license__ = "mit"

_logger = logging.getLogger(__name__)


def fib(n):
    """Fibonacci example function

    Args:
      n (int): integer

    Returns:
      int: n-th Fibonacci number
    """
    assert n > 0
    a, b = 1, 1
    for i in range(n - 1):
        a, b = b, a + b
    return a


def parse_args(args):
    """Parse command line parameters

    Args:
      args ([str]): command line parameters as list of strings

    Returns:
      :obj:`argparse.Namespace`: command line parameters namespace
    """
    parser = argparse.ArgumentParser(
      prog="Pho(to)fo(folder)fi(x)",
      description="Photo folder fixer and then some more - Fixes folder structure, created date and exif data if needed.",
      usage="phofofix -i [INPUT FOLDER] -o [OUTPUT FOLDER]"
    )
    parser.add_argument(
        "--version",
        action="version",
        version="photofi {ver}".format(ver=__version__),
    )
    parser.add_argument(
        "-i",
        "--input-folder",
        required=True,
        default="data/input",
        help="set input folder",
        type=str
    )
    parser.add_argument(
        "-R",
        "--recursivly",
        action='store_true',
        help="search through input folder recursivly"
    )
    parser.add_argument(
        "-fm",
        "--fix-meta-data",
        action='store_true',
        help="tries to fix broken metadata such as wrongly set creation date"
    )
    parser.add_argument(
        "-o",
        "--output-folder",
        required=True,
        default="data/output",
        help="set output folder",
        type=str
    )
    parser.add_argument(
        "-v",
        "--verbose",
        dest="loglevel",
        help="set loglevel to INFO",
        action="store_const",
        const=logging.INFO,
    )
    parser.add_argument(
        "-vv",
        "--very-verbose",
        dest="loglevel",
        help="set loglevel to DEBUG",
        action="store_const",
        const=logging.DEBUG,
    )
    return parser.parse_args(args)


def setup_logging(loglevel):
    """Setup basic logging

    Args:
      loglevel (int): minimum loglevel for emitting messages
    """
    logformat = "[%(asctime)s] %(levelname)s:%(name)s:%(message)s"
    logging.basicConfig(
        level=loglevel, stream=sys.stdout, format=logformat, datefmt="%Y-%m-%d %H:%M:%S"
    )


def runFib():
    """Entry point for console_scripts"""
    main(sys.argv[1:])

def run():
    """Entry point for console_scripts"""
    
    """Main entry point allowing external calls

    Args:
      args ([str]): command line parameter list
    """
    
    args = parse_args(sys.argv[1:])
    setup_logging(args.loglevel)
    main(args)
    
    _logger.info("Script ends here")

def main(args):
    core.main(args)
    

if __name__ == "__main__":
    run()