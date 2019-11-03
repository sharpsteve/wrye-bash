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
    'Archery, ArrowTilt 0.0 [Enderal].ini': OrderedDict(
        [('Combat', OrderedDict(
            [('f1PArrowTiltUpAngle', '0.0'),
             ('f3PArrowTiltUpAngle', '0.0')]))]),
    'Archery, ArrowTilt 0.7 [Enderal].ini': OrderedDict(
        [('Combat', OrderedDict(
            [('f1PArrowTiltUpAngle', '0.7'),
             ('f3PArrowTiltUpAngle', '0.7')]))]),
    'Archery, NavMeshMove 12288 [Enderal].ini': OrderedDict(
        [('Actor', OrderedDict(
            [('fVisibleNavmeshMoveDist', '12288.0000')]))]),
    'Archery, NavMeshMove 4096 [Enderal].ini': OrderedDict(
        [('Actor', OrderedDict(
            [('fVisibleNavmeshMoveDist', '4096.0000')]))]),
    'Archery, NavMeshMove 8192 [Enderal].ini': OrderedDict(
        [('Actor', OrderedDict(
            [('fVisibleNavmeshMoveDist', '8192.0000')]))]),
    'Enderal Intro sequence, Disabled [Enderal].ini': OrderedDict(
        [('General', OrderedDict([('sIntroSequence', '0')]))]),
    'Enderal Intro sequence, Enabled ~Default [Enderal].ini': OrderedDict(
        [('General', OrderedDict([('sIntroSequence', '1')]))]),
    'Border Regions, Disabled [Enderal].ini': OrderedDict(
        [('General', OrderedDict([('bBorderRegionsEnabled', '0')]))]),
    'Border Regions, Enabled [Enderal].ini': OrderedDict(
        [('General', OrderedDict([('bBorderRegionsEnabled', '1')]))]),
    'Debug Log, Disabled [Enderal].ini': OrderedDict(
        [('Papyrus', OrderedDict(
            [('bEnableLogging', '0'), ('bLoadDebugInformation', '0'),
             ('bEnableTrace', '0')]))]),
    'Debug Log, Enabled ~Default [Enderal].ini': OrderedDict(
        [('Papyrus', OrderedDict(
        [('bEnableLogging', '1'), ('bLoadDebugInformation', '1'),
         ('bEnableTrace', '1')]))]),
    'Grass, Spacing 20 [Enderal].ini': OrderedDict(
        [('Grass', OrderedDict([('iMinGrassSize', '20')]))]),
    'Grass, Spacing 40 [Enderal].ini': OrderedDict(
        [('Grass', OrderedDict([('iMinGrassSize', '40')]))]),
    'Grass, Spacing 60 [Enderal].ini': OrderedDict(
        [('Grass', OrderedDict([('iMinGrassSize', '60')]))]),
    'Grass, Spacing 80 [Enderal].ini': OrderedDict(
        [('Grass', OrderedDict([('iMinGrassSize', '80')]))]),
    'Large Interiors Static Limit Fix [Enderal].ini': OrderedDict(
        [('General', OrderedDict([('iLargeIntRefCount', '999999')]))]),
    'Large Interiors Static Limit [Enderal].ini': OrderedDict(
        [('General', OrderedDict([('iLargeIntRefCount', '1000')]))]),
    'Particles, 100 [EnderalPrefs.ini].ini': OrderedDict(
        [('Particles', OrderedDict([('iMaxDesired', '100')]))]),
    'Particles, 150 [EnderalPrefs.ini].ini': OrderedDict(
        [('Particles', OrderedDict([('iMaxDesired', '150')]))]),
    'Particles, 250 [EnderalPrefs.ini].ini': OrderedDict(
        [('Particles', OrderedDict([('iMaxDesired', '250')]))]),
    'Particles, 350 [EnderalPrefs.ini].ini': OrderedDict(
        [('Particles', OrderedDict([('iMaxDesired', '350')]))]),
    'Particles, 450 [EnderalPrefs.ini].ini': OrderedDict(
        [('Particles', OrderedDict([('iMaxDesired', '450')]))]),
    'Particles, 550 [EnderalPrefs.ini].ini': OrderedDict(
        [('Particles', OrderedDict([('iMaxDesired', '550')]))]),
    'Particles, 650 [EnderalPrefs.ini].ini': OrderedDict(
        [('Particles', OrderedDict([('iMaxDesired', '650')]))]),
    'Particles, 750 ~Default [EnderalPrefs.ini].ini': OrderedDict(
        [('Particles', OrderedDict([('iMaxDesired', '750')]))]),
    'Screenshot, Disabled [Enderal].ini': OrderedDict(
        [('Display', OrderedDict([('bAllowScreenShot', '0')]))]),
    'Screenshot, Enabled ~Default [Enderal].ini': OrderedDict(
        [('Display', OrderedDict([('bAllowScreenShot', '1')]))]),
    'Shadows, Res512 [EnderalPrefs.ini].ini': OrderedDict(
        [('Display', OrderedDict([('iShadowMapResolution', '512')]))]),
    'Shadows, Res1024 [EnderalPrefs.ini].ini': OrderedDict(
        [('Display', OrderedDict([('iShadowMapResolution', '1024')]))]),
    'Shadows, Res2048 [EnderalPrefs.ini].ini': OrderedDict(
        [('Display', OrderedDict([('iShadowMapResolution', '2048')]))]),
    'Shadows, Res4096 ~Default [EnderalPrefs.ini].ini': OrderedDict(
        [('Display', OrderedDict([('iShadowMapResolution', '4096')]))]),
    'Vanity Camera, 120 [Enderal].ini': OrderedDict(
        [('Camera', OrderedDict([('fAutoVanityModeDelay', '120.0000')]))]),
    'Vanity Camera, 600 [Enderal].ini': OrderedDict(
        [('Camera', OrderedDict([('fAutoVanityModeDelay', '600.0000')]))]),
    'Vanity Camera, Disable [Enderal].ini': OrderedDict(
        [('Camera', OrderedDict([('fAutoVanityModeDelay', '0')]))]),
    'Window Mode Top left, 20-225 [Enderal].ini': OrderedDict(
        [('Display', OrderedDict(
            [('iLocation Y', '20'), ('iLocation X', '225')]))]),
    'Window Mode Top left, 5-5 [Enderal].ini': OrderedDict(
        [('Display', OrderedDict(
            [('iLocation Y', '5'), ('iLocation X', '5')]))]),
    'Window Mode Top left, 5-60 [Enderal].ini': OrderedDict(
        [('Display', OrderedDict(
            [('iLocation Y', '5'), ('iLocation X', '60')]))]),
    'Invalidate, Allow loose files ~Default [Enderal].ini': OrderedDict(
        [('Archive', OrderedDict([('bInvalidateOlderFiles', '1')]))]),
    'Invalidate, Disallow loose files [Enderal].ini': OrderedDict(
        [('Archive', OrderedDict([('bInvalidateOlderFiles', '0')]))]),
    'Depth Of Field, Off [EnderalPrefs.ini].ini': OrderedDict(
        [('Imagespace', OrderedDict([('bDoDepthOfField', '0')]))]),
    'Depth Of Field, On ~Default [EnderalPrefs.ini].ini': OrderedDict(
        [('Imagespace', OrderedDict([('bDoDepthOfField', '1')]))]),
    'In Game Compass, Off [EnderalPrefs.ini].ini': OrderedDict(
        [('Interface', OrderedDict([('bShowCompass', '0')]))]),
    'In Game Compass, On ~Default [EnderalPrefs.ini].ini': OrderedDict(
        [('Interface', OrderedDict([('bShowCompass', '1')]))]),
    'In Game Crosshair, Off [EnderalPrefs.ini].ini': OrderedDict(
        [('Main', OrderedDict([('bCrosshairEnabled', '0')]))]),
    'In Game Crosshair, On ~Default [EnderalPrefs.ini].ini': OrderedDict(
        [('Main', OrderedDict([('bCrosshairEnabled', '1')]))]),
    'In Game Quest Markers, Off [EnderalPrefs.ini].ini': OrderedDict(
        [('GamePlay', OrderedDict([('bShowFloatingQuestMarkers', '0')]))]),
    'In Game Quest Markers, On ~Default [EnderalPrefs.ini].ini': OrderedDict(
        [('GamePlay', OrderedDict([('bShowFloatingQuestMarkers', '1')]))]),
    'Map Quest Markers, Off [EnderalPrefs.ini].ini': OrderedDict(
        [('GamePlay', OrderedDict([('bShowQuestMarkers', '0')]))]),
    'Map Quest Markers, On ~Default [EnderalPrefs.ini].ini': OrderedDict(
        [('GamePlay', OrderedDict([('bShowQuestMarkers', '1')]))]),
    'Tutorials, Off [Enderal].ini': OrderedDict(
        [('Interface', OrderedDict([('bShowTutorials', '0')]))]),
    'Tutorials, On [Enderal].ini': OrderedDict(
        [('Interface', OrderedDict([('bShowTutorials', '1')]))]),
}
