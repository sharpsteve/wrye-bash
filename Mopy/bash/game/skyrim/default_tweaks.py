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
    'Archery, ArrowTilt 0.0 ~Default [Skyrim].ini': OrderedDict(
        [('Combat', OrderedDict(
            [('f1PArrowTiltUpAngle', '0.0'),
             ('f3PArrowTiltUpAngle', '0.0')]))]),
    'Archery, ArrowTilt 0.7 [Skyrim].ini': OrderedDict(
        [('Combat', OrderedDict(
            [('f1PArrowTiltUpAngle', '0.7'),
             ('f3PArrowTiltUpAngle', '0.7')]))]),
    'Archery, NavMeshMove 12288 [Skyrim].ini': OrderedDict(
        [('Actor', OrderedDict(
            [('fVisibleNavmeshMoveDist', '12288.0000')]))]),
    'Archery, NavMeshMove 4096 ~Default [Skyrim].ini': OrderedDict(
        [('Actor', OrderedDict(
            [('fVisibleNavmeshMoveDist', '4096.0000')]))]),
    'Archery, NavMeshMove 8192 [Skyrim].ini': OrderedDict(
        [('Actor', OrderedDict(
            [('fVisibleNavmeshMoveDist', '8192.0000')]))]),
    'BGS Intro sequence, Disabled [Skyrim].ini': OrderedDict(
        [('General', OrderedDict([('sIntroSequence', '')]))]),
    'BGS Intro sequence, Enabled ~Default [Skyrim].ini': OrderedDict(
        [('General', OrderedDict([('sIntroSequence', 'BGS_LOGO.BIK')]))]),
    'Border Regions, Disabled [Skyrim].ini': OrderedDict(
        [('General', OrderedDict([('bBorderRegionsEnabled', '0')]))]),
    'Border Regions, Enabled ~Default [Skyrim].ini': OrderedDict(
        [('General', OrderedDict([('bBorderRegionsEnabled', '1')]))]),
    'Debug Log, Disabled [Skyrim].ini': OrderedDict(
        [('Papyrus', OrderedDict(
            [('bEnableLogging', '0'), ('bLoadDebugInformation', '0'),
             ('bEnableTrace', '0')]))]),
    'Debug Log, Enabled [Skyrim].ini': OrderedDict(
        [('Papyrus', OrderedDict(
        [('bEnableLogging', '1'), ('bLoadDebugInformation', '1'),
         ('bEnableTrace', '1')]))]),
    'Grass, Spacing 20 ~Default [Skyrim].ini': OrderedDict(
        [('Grass', OrderedDict([('iMinGrassSize', '20')]))]),
    'Grass, Spacing 40 [Skyrim].ini': OrderedDict(
        [('Grass', OrderedDict([('iMinGrassSize', '40')]))]),
    'Grass, Spacing 60 [Skyrim].ini': OrderedDict(
        [('Grass', OrderedDict([('iMinGrassSize', '60')]))]),
    'Grass, Spacing 80 [Skyrim].ini': OrderedDict(
        [('Grass', OrderedDict([('iMinGrassSize', '80')]))]),
    'Large Interiors Static Limit Fix [Skyrim].ini': OrderedDict(
        [('General', OrderedDict([('iLargeIntRefCount', '999999')]))]),
    'Large Interiors Static Limit ~Default [Skyrim].ini': OrderedDict(
        [('General', OrderedDict([('iLargeIntRefCount', '1000')]))]),
    'Particles, 100 [SkyrimPrefs].ini': OrderedDict(
        [('Particles', OrderedDict([('iMaxDesired', '100')]))]),
    'Particles, 150 [SkyrimPrefs].ini': OrderedDict(
        [('Particles', OrderedDict([('iMaxDesired', '150')]))]),
    'Particles, 250 [SkyrimPrefs].ini': OrderedDict(
        [('Particles', OrderedDict([('iMaxDesired', '250')]))]),
    'Particles, 350 [SkyrimPrefs].ini': OrderedDict(
        [('Particles', OrderedDict([('iMaxDesired', '350')]))]),
    'Particles, 450 [SkyrimPrefs].ini': OrderedDict(
        [('Particles', OrderedDict([('iMaxDesired', '450')]))]),
    'Particles, 550 [SkyrimPrefs].ini': OrderedDict(
        [('Particles', OrderedDict([('iMaxDesired', '550')]))]),
    'Particles, 650 [SkyrimPrefs].ini': OrderedDict(
        [('Particles', OrderedDict([('iMaxDesired', '650')]))]),
    'Particles, 750 ~Default [SkyrimPrefs].ini': OrderedDict(
        [('Particles', OrderedDict([('iMaxDesired', '750')]))]),
    'Screenshot, Disabled ~Default [Skyrim].ini': OrderedDict(
        [('Display', OrderedDict([('bAllowScreenShot', '0')]))]),
    'Screenshot, Enabled [Skyrim].ini': OrderedDict(
        [('Display', OrderedDict([('bAllowScreenShot', '1')]))]),
    'Shadows, Res512 Dist 1 [SkyrimPrefs].ini': OrderedDict(
        [('Display', OrderedDict(
            [('fShadowDistance', '1.0000'), ('fShadowBiasScale', '0.6000'),
             ('iShadowMapResolutionPrimary', '1024'),
             ('iShadowMapResolutionSecondary', '512'),
             ('fInteriorShadowDistance', '2000.0000'),
             ('iShadowMapResolution', '512')]))]),
    'Shadows, Res512 [SkyrimPrefs].ini': OrderedDict(
        [('Display', OrderedDict(
            [('fShadowDistance', '2000.0000'),
             ('fShadowBiasScale', '0.6000'),
             ('iShadowMapResolutionPrimary', '1024'),
             ('iShadowMapResolutionSecondary', '512'),
             ('fInteriorShadowDistance', '2000.0000'),
             ('iShadowMapResolution', '512')]))]),
    'SunShadow, Update 0.0000 [Skyrim].ini': OrderedDict(
        [('Display', OrderedDict(
            [('fSunUpdateThreshold', '0.0000'),
             ('fSunShadowUpdateTime', '0.0000')]))]),
    'SunShadow, Update 0.0500 [Skyrim].ini': OrderedDict(
        [('Display', OrderedDict(
            [('fSunUpdateThreshold', '0.0500'),
             ('fSunShadowUpdateTime', '0.0000')]))]),
    'SunShadow, Update 0.1000 [Skyrim].ini': OrderedDict(
        [('Display', OrderedDict(
            [('fSunUpdateThreshold', '0.1000'),
             ('fSunShadowUpdateTime', '0.0000')]))]),
    'SunShadow, Update 0.2000 [Skyrim].ini': OrderedDict(
        [('Display', OrderedDict(
            [('fSunUpdateThreshold', '0.2000'),
             ('fSunShadowUpdateTime', '0.0000')]))]),
    'Texture Detail, High [SkyrimPrefs].ini': OrderedDict(
        [('Display', OrderedDict([('iTexMipMapSkip', '0')]))]),
    'Texture Detail, Low [SkyrimPrefs].ini': OrderedDict(
        [('Display', OrderedDict([('iTexMipMapSkip', '2')]))]),
    'Texture Detail, Medium [SkyrimPrefs].ini': OrderedDict(
        [('Display', OrderedDict([('iTexMipMapSkip', '1')]))]),
    'Vanity Camera, 120 ~Default [Skyrim].ini': OrderedDict(
        [('Camera', OrderedDict([('fAutoVanityModeDelay', '120.0000')]))]),
    'Vanity Camera, 600 [Skyrim].ini': OrderedDict(
        [('Camera', OrderedDict([('fAutoVanityModeDelay', '600.0000')]))]),
    'Vanity Camera, Disable [Skyrim].ini': OrderedDict(
        [('Camera', OrderedDict([('fAutoVanityModeDelay', '0')]))]),
    'WaterReflect, Res1024 [SkyrimPrefs].ini': OrderedDict(
        [('Water', OrderedDict(
            [('iWaterReflectWidth', '1024'),
             ('iWaterReflectHeight', '1024')]))]),
    'WaterReflect, Res256 [SkyrimPrefs].ini': OrderedDict(
        [('Water', OrderedDict(
            [('iWaterReflectWidth', '256'),
             ('iWaterReflectHeight', '256')]))]),
    'WaterReflect, Res512 ~Default[SkyrimPrefs].ini': OrderedDict(
        [('Water', OrderedDict(
            [('iWaterReflectWidth', '512'),
             ('iWaterReflectHeight', '512')]))]),
    'Window Mode Top left, 20-225 [Skyrim].ini': OrderedDict(
        [('Display', OrderedDict(
            [('iLocation Y', '20'), ('iLocation X', '225')]))]),
    'Window Mode Top left, 5-5 ~Default [Skyrim].ini': OrderedDict(
        [('Display', OrderedDict(
            [('iLocation Y', '5'), ('iLocation X', '5')]))]),
    'Window Mode Top left, 5-60 [Skyrim].ini': OrderedDict(
        [('Display', OrderedDict(
            [('iLocation Y', '5'), ('iLocation X', '60')]))])
}
