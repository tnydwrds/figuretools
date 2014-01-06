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
import re

# -----------------------------------------------------------------------------
# Settings
# You can changes stuffs here.
# -----------------------------------------------------------------------------
dist_directory = 'dist'
package_directories = []
exclude_files = [__file__]
exclude_patterns = []
include_files = []


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
    package_name = os.path.basename(os.path.split(os.path.realpath(__file__))[0])
    build_directory = 'build_tmp'
    working_directory = os.path.join(build_directory, package_name)
    if os.path.exists(build_directory):
        shutil.rmtree(build_directory)
    os.makedirs(working_directory)

    # Running list of distributable files. Starting with modules in current dir.
    distributable_files = glob.glob('*.py')

    for pd in package_directories:
        # Add all package modules.
        py_pathname = os.path.join(pd, '*.py')
        distributable_files.extend(glob.glob(py_pathname))

        # Create a package directory in our working directory.
        build_pd = os.path.join(working_directory, pd)
        if not os.path.exists(build_pd):
            os.makedirs(build_pd)

    # Remove excluded files from distributable_files.
    if exclude_patterns:
        for ep in exclude_patterns:
            exclude_files.extend(glob.glob(ep))
    for ef in exclude_files:
        distributable_files.remove(ef)

    # Add explicitly included files to distributable_files.
    # TODO: Mabye add include_pattern as well?
    distributable_files.extend(include_files)

    # Move distributable files to our working directory.
    for df in distributable_files:
        df_destination = os.path.join(working_directory, df)
        shutil.copyfile(df, df_destination)

    # Get addon version number.
    version_re = '["\']version["\']\s*?:\s*?\(\s*?(\d+?)\s*?,\s*?(\d+?)\s*?,\s*?(\d+?)\s*?\)'
    version = re.search(version_re, open('__init__.py', 'r').read())
    version = '.'.join(version.groups()) if version else '0.0.0'

    # Make the zip file.
    zip_file_name = '%s-%s' % (package_name, version)
    shutil.make_archive(
        base_name=os.path.join(dist_directory, zip_file_name),
        format='zip',
        root_dir=build_directory,
        base_dir=package_name)

    # Remember to clean up the build directory.
    shutil.rmtree(build_directory)


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