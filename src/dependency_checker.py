#!/usr/bin/env python

import subprocess

def command_is_available(command):
    args = command.split()
    try:
        output = subprocess.call(args)
        return True
    except OSError:
        return False
