# -*- coding: utf-8 -*-
#
# GPL License and Copyright Notice ============================================
#  This file is part of Wrye Bash.
#
#  Wrye Bash is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  Wrye Bash is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with Wrye Bash; if not, write to the Free Software Foundation,
#  Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.
#
#  Wrye Bash copyright (C) 2005-2009 Wrye, 2010-2019 Wrye Bash Team
#  https://github.com/wrye-bash
#
# =============================================================================
from collections import OrderedDict

default_tweaks = {
    'Border Regions, Disabled.ini': OrderedDict(
    [('MAIN', OrderedDict([('bEnableBorderRegion', '0')]))]),
    'Border Regions, ~Enabled.ini': OrderedDict(
        [('MAIN', OrderedDict([('bEnableBorderRegion', '1')]))]),
    'Fonts 1, ~Default.ini': OrderedDict([('Fonts', OrderedDict(
        [('sFontFile_1', 'Textures\\Fonts\\Glow_Monofonto_Large.fnt')]))]),
    'Grass, Fade 4k-5k.ini': OrderedDict(
        [('Grass', OrderedDict(
        [('iMinGrassSize', '140'),
         ('fGrassMaxStartFadeDistance', '5000.0000')]))]),
    'Mouse Acceleration, Default.ini': OrderedDict([('CONTROLS', OrderedDict(
        [('fForegroundMouseAccelBase', ''), ('fForegroundMouseBase', ''),
         ('fForegroundMouseAccelTop', ''),
         ('fForegroundMouseMult', '')]))]),
    'Mouse Acceleration, ~Fixed.ini': OrderedDict([('CONTROLS', OrderedDict(
        [('fForegroundMouseAccelBase', '0'), ('fForegroundMouseBase', '0'),
         ('fForegroundMouseAccelTop', '0'),
         ('fForegroundMouseMult', '0')]))]),
    'Refraction Shader, Disabled.ini': OrderedDict(
        [('Display', OrderedDict([('bUseRefractionShader', '0')]))]),
    'Refraction Shader, ~Enabled.ini': OrderedDict(
        [('Display', OrderedDict([('bUseRefractionShader', '1')]))]),
    'Save Backups, 1.ini': OrderedDict(
        [('General', OrderedDict([('iSaveGameBackupCount', '1')]))]),
    'Save Backups, 2.ini': OrderedDict(
        [('General', OrderedDict([('iSaveGameBackupCount', '2')]))]),
    'Save Backups, 3.ini': OrderedDict(
        [('General', OrderedDict([('iSaveGameBackupCount', '3')]))]),
    'Save Backups, 5.ini': OrderedDict(
        [('General', OrderedDict([('iSaveGameBackupCount', '5')]))]),
    'bInvalidateOlderFiles, ~Default.ini': OrderedDict(
        [('Archive', OrderedDict([('bInvalidateOlderFiles', '0')]))]),
    'bInvalidateOlderFiles, ~Enabled.ini': OrderedDict(
        [('Archive', OrderedDict([('bInvalidateOlderFiles', '1')]))]),
    'iConsoleTextXPos, Default.ini': OrderedDict(
        [('Menu', OrderedDict([('iConsoleTextXPos', '30')]))]),
    'iConsoleTextXPos, ~Fixed.ini': OrderedDict(
        [('Menu', OrderedDict([('iConsoleTextXPos', '130')]))])
}
