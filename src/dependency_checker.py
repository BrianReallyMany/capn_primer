#!/usr/bin/env python

import subprocess
import sys

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
