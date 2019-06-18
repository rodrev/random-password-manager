#!/usr/bin/env python3
from RPM.Data import Data
from RPM.Options import Options
from RPM.MainMenu import MainMenu
import os
import shelve
import sys

# Relative path of directory containing this file
RELATIVE = os.path.dirname(sys.argv[0])
# Absolute path of directory containing this file
ABSOLUTE = os.path.abspath(RELATIVE)
# File paths to create in this directory:
OPTIONS = ABSOLUTE + "/opt"  # save options here (bytes)
DATA = ABSOLUTE + "/dat"  # save data here (bytes)
SAVE = ABSOLUTE + "/txt"  # save data here with "Save all" feature (text)


class NoUI:
    def __init__(self, name):
        """ NON-INTERACTIVE MODE """
        if name[0] in ("-q", "--quiet"):
            Data().get_entry_no_ui(name=" ".join(name[1:]), quiet=True)
        else:
            Data().get_entry_no_ui(name=" ".join(name), quiet=False)


class Main:
    # Shelve.open:
    # Opens a shelf, a persistent dictionary-like object
    # 'c' flag: opens database file for reading and writing,
    #   creating it if it doesn't exist
    # writeback parameter: all entries accessed are also cached in memory,
    #   and written back to disk on sync() and close();
    oshelf = shelve.open(filename=OPTIONS, flag="c", writeback=True)  # options
    dshelf = shelve.open(filename=DATA, flag="c", writeback=True)  # data
    options = Options(oshelf)

    def __init__(self):
        arguments = sys.argv[1:]
        if arguments:  # Command line argument given ==> Non-Interactive Mode
            NoUI(arguments)  # No user interface
        else:  # No command line argument ==> Interactive Mode
            print("\nWelcome to Random Password Manager\n")
            MainMenu(self.options)  # User interface
        self.oshelf.close()
        self.dshelf.close()


if __name__ == "__main__":
    GRAPH = False  # call graph

    if GRAPH:
        from pycallgraph import PyCallGraph
        from pycallgraph.output import GraphvizOutput
        with PyCallGraph(output=GraphvizOutput()):
            Main()
    else:
        Main()
