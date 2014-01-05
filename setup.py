#!/usr/bin/env python
# -*- coding: utf8 -*-
#
# ***** BEGIN GPL LICENSE BLOCK *****
#
# --------------------------------------------------------------------------
# Blender 2.6 FigureTools Addon
# --------------------------------------------------------------------------
#
# Authors:
# Tony Edwards
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, see <http://www.gnu.org/licenses/>.
#
# ***** END GPL LICENCE BLOCK *****
#
from argparse import ArgumentParser, RawDescriptionHelpFormatter
import glob
import os
import shutil
import sys

# -----------------------------------------------------------------------------
# Settings
# You can changes stuffs here.
# -----------------------------------------------------------------------------
dist_directory = 'dist'
package_directories = []


# -----------------------------------------------------------------------------
# Guts
# You shouldn't change stuffs here. Unless its broken or something.
# -----------------------------------------------------------------------------
description = """
Create a Blender friendly Python distribution.

Example:
  setup.py sdist   wil bundle raw files in a zip suitable for Blender.

Commands:
  sdist            create a source distribution (zip file)
"""

# Convention is that each command in 'available_commands' has a companion
# module function prefixed with 'do_'. So if there is a command 'sdist', there
# should be a function named 'do_sdist'.
#
# Right now only a source distribution is supported. Perhaps in the future a
# compiled (.pyc) distribution could be supported.
available_commands = ['sdist']

def do_sdist():
    """Make source distribution of package"""
    if not os.path.exists(dist_directory):
        os.makedirs(dist_directory)

    # Create a clean temporary build directory.
    temp_build_directory = 'build_tmp'
    if os.path.exists(temp_build_directory):
        shutil.rmtree(temp_build_directory)
    os.mkdir(temp_build_directory)

    # Running list of files to package. Starting with modules in current dir.
    distributable_files = glob.glob('*.py')

    for pd in package_directories:
        # Add all package modules.
        py_pathname = os.path.join(pd, '*.py')
        distributable_files.extend(glob.glob(py_pathname))

        # Create a package directory in our build directory.
        build_pd = os.path.join(temp_build_directory, pd)
        if not os.path.exists(build_pd):
            os.makedirs(build_pd)

    # Move distributable files to our build directory.
    for df in distributable_files:
        df_destination = os.path.join(temp_build_directory, df)
        shutil.copyfile(df, df_destination)

    # Remember to clean up the build directory.
    #shutil.rmtree(temp_build_directory)


def main(args):
    parser = ArgumentParser(
        formatter_class=RawDescriptionHelpFormatter,
        description=description)

    parser.add_argument('cmd', help='See available commands above')

    args = parser.parse_args(args)

    # Perform command.
    cmd = args.cmd
    if cmd in available_commands:
        # Using globals feels like the wrong way to do this, but it works.
        globals()['do_' + cmd]()
    else:
        print("error: invalid command '%s'" % cmd)


if __name__ == '__main__':
    main(sys.argv[1:])
