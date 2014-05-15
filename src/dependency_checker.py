#!/usr/bin/env python

import subprocess
import sys

def check_dependencies():
    # check primer3_core
    if primer3_core_is_installed():
        print("...Yarr! primer3_core be installed.")
    else:
        print("Yarr! Why ye not install primer3_core, scurvy dog.")
        sys.exit()

    # check makeblastdb
    if makeblastdb_is_installed():
        print("...Yarr! makeblastdb be installed.")
    else:
        print("Yarr! Why ye not install makeblastdb, scurvy dog.")
        sys.exit()

    # check blastall
    if blastall_is_installed():
        print("...Yarr! blastall be installed.\n")
    else:
        print("Yarr! Why ye not install blastall, scurvy dog.")
        sys.exit()


def command_is_available(command):
    # Not smart enough to redirect stderr and stdout to /dev/null
    # so using a file instead.
    junkfile = open("junk", "wb")
    args = command.split()
    try:
        output = subprocess.call(args, stderr=junkfile, stdout=junkfile)
        junkfile.close()
        subprocess.call(["rm", "junk"])
        return True
    except OSError:
        junkfile.close()
        subprocess.call(["rm", "junk"])
        return False

def primer3_core_is_installed():
    return command_is_available("primer3_core --help")

def blastall_is_installed():
    return command_is_available("blastall --help")

def makeblastdb_is_installed():
    return command_is_available("makeblastdb -h")
