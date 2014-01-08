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
from distutils.core import setup
from distutils.command.build_py import build_py
import os.path
import re
from shutil import make_archive, rmtree

# Packages, data and additional files.
packages = ['figuretools', 'figuretools.dson']

class blender_dist(build_py):
    """ """

    description = \
    '"build" pure Python modules (copy to build directory) and zip it"'

    def run(self):
        build_dir = self.build_lib = 'tmp_build'
        super(blender_dist, self).run()

        archive_name = self.distribution.get_fullname().lower()
        archive_path = os.path.join('dist', archive_name)

        msg = \
        'creating \'%s.zip\' and adding \'%s\' (and everything under it) to it'
        print(msg % (archive_path, root_package))
        if (not self.dry_run):
            make_archive(
                base_name=archive_path,
                format='zip',
                root_dir=build_dir,
                base_dir=root_package)

        print('removing %s (and everything under it)' % build_dir)
        if (not self.dry_run):
            rmtree(build_dir)


# For now, assume addon has one root package and it is the first package.
root_package = packages[0]

# Reuse addon details from bl_info in the root package.
bl_info_re = re.compile('bl_info\s*?=\s*?({.*?})', re.DOTALL)
bl_info_file = os.path.join(root_package, '__init__.py')
bl_info_match = bl_info_re.search(open(bl_info_file, 'r').read())
bl_info = eval(bl_info_match.groups()[0])

setup(
    name=bl_info['name'],
    version='%s.%s.%s' % bl_info['version'],
    author=bl_info['author'],
    packages=packages,
    cmdclass={'blender_dist': blender_dist})
