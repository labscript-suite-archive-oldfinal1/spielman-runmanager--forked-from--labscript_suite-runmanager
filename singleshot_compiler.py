#####################################################################
#                                                                   #
# /singleshot_compiler.py                                           #
#                                                                   #
# Copyright 2017, Joint Quantum Institute                           #
#                                                                   #
# This file is part of the program runmanager, in the labscript     #
# suite (see http://labscriptsuite.org), and is licensed under the  #
# Simplified BSD License. See the license.txt file in the root of   #
# the project for the full license.                                 #
#                                                                   #
#####################################################################

"""A simple program to be called with a labscript file and a
shot h5 file (containing globals) as  command line arguments. Calls
labscript_init() and then executes the user's labscript file."""

import sys
labscript_file, h5_file = sys.argv[1:]
import labscript
labscript.labscript_init(h5_file)
sandbox = {'__name__': '__main__'}
execfile(labscript_file, sandbox, sandbox)
