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
import bpy
from bpy.props import StringProperty
from bpy_extras.io_utils import ImportHelper

class DSONImporter(bpy.types.Operator, ImportHelper):
    """Load a DAZ DSON file"""
    bl_idname = 'import_scene.dson'
    bl_label = 'Import DSON'

    filename_ext = '.duf'
    filter_glob = StringProperty(default='*.duf;*.dsf', options={'HIDDEN'})

    def execute(self, context):
        print('FigureTools: Importing %s' % self.filepath)

        return {'FINISHED'}
