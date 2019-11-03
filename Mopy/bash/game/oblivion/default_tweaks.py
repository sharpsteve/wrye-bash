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
    'Autosave, Never [Oblivion].ini': OrderedDict(
        [('GamePlay', OrderedDict(
            [('bSaveOnWait', '0'), ('bSaveOnTravel', '0'),
             ('bSaveOnRest', '0')]))]),
    'Autosave, ~Always [Oblivion].ini':
        OrderedDict([('GamePlay', OrderedDict(
            [('bSaveOnWait', '1'), ('bSaveOnTravel', '1'),
                ('bSaveOnRest', '1')]))]),
    'Border Regions, Disabled [Oblivion].ini': OrderedDict(
        [('General', OrderedDict(
            [('bBorderRegionsEnabled', '0')]))]),
    'Border Regions, ~Enabled [Oblivion].ini': OrderedDict(
        [('General', OrderedDict(
            [('bBorderRegionsEnabled', '1')]))]),
    'Fonts 1, ~Default [Oblivion].ini': OrderedDict(
        [('Fonts', OrderedDict(
            [('SFontFile_1', 'Data\\Fonts\\Kingthings_Regular.fnt')]))]),
    'Fonts, ~Default [Oblivion].ini': OrderedDict(
        [('Fonts', OrderedDict(
            [('SFontFile_4', 'Data\\Fonts\\Daedric_Font.fnt'),
             ('SFontFile_5', 'Data\\Fonts\\Handwritten.fnt'),
             ('SFontFile_1', 'Data\\Fonts\\Kingthings_Regular.fnt'),
             ('SFontFile_2', 'Data\\Fonts\\Kingthings_Shadowed.fnt'),
             ('SFontFile_3', 'Data\\Fonts\\Tahoma_Bold_Small.fnt')]))]),
    'Grass, Fade 4k-5k [Oblivion].ini': OrderedDict(
        [('Grass', OrderedDict(
            [('iMinGrassSize', '120'),
             ('fGrassStartFadeDistance', '4000.0000'),
             ('fGrassEndDistance', '5000.0000')]))]),
    'Grass, ~Fade 2k-3k [Oblivion].ini': OrderedDict(
        [('Grass', OrderedDict(
        [('iMinGrassSize', '80'), ('fGrassStartFadeDistance', '2000.0000'),
         ('fGrassEndDistance', '3000.0000')]))]),
    'Intro Movies, Disabled [Oblivion].ini': OrderedDict(
        [('General', OrderedDict(
            [('SCreditsMenuMovie', ''), ('SMainMenuMovieIntro', ''),
             ('SMainMenuMovie', ''), ('SIntroSequence', '')]))]),
    'Intro Movies, ~Normal [Oblivion].ini': OrderedDict(
        [('General', OrderedDict(
            [('SCreditsMenuMovie', 'CreditsMenu.bik'),
             ('SMainMenuMovieIntro', 'Oblivion iv logo.bik'),
             ('SMainMenuMovie', 'Map loop.bik'),
             ('SIntroSequence',
              'bethesda softworks HD720p.bik,2k games.bik,game studios.bik,'
              'Oblivion Legal.bik')]))]),
    'Joystick, Disabled [Oblivion].ini': OrderedDict(
        [('Controls', OrderedDict([('bUse Joystick', '0')]))]),
    'Joystick, ~Enabled [Oblivion].ini': OrderedDict(
        [('Controls', OrderedDict([('bUse Joystick', '1')]))]),
    'Local Map Shader, Disabled [Oblivion].ini': OrderedDict(
        [('Display', OrderedDict([('blocalmapshader', '0')]))]),
    'Local Map Shader, ~Enabled [Oblivion].ini': OrderedDict(
        [('Display', OrderedDict([('blocalmapshader', '1')]))]),
    'Music, Disabled [Oblivion].ini': OrderedDict(
        [('Audio', OrderedDict([('bMusicEnabled', '0')]))]),
    'Music, ~Enabled [Oblivion].ini': OrderedDict(
        [('Audio', OrderedDict([('bMusicEnabled', '1')]))]),
    'Refraction Shader, Disabled [Oblivion].ini': OrderedDict(
        [('Display', OrderedDict([('bUseRefractionShader', '0')]))]),
    'Refraction Shader, ~Enabled [Oblivion].ini': OrderedDict(
        [('Display', OrderedDict([('bUseRefractionShader', '1')]))]),
    'Save Backups, 1 [Oblivion].ini': OrderedDict(
        [('General', OrderedDict([('iSaveGameBackupCount', '1')]))]),
    'Save Backups, 2 [Oblivion].ini': OrderedDict(
        [('General', OrderedDict([('iSaveGameBackupCount', '2')]))]),
    'Save Backups, 3 [Oblivion].ini': OrderedDict(
        [('General', OrderedDict([('iSaveGameBackupCount', '3')]))]),
    'Save Backups, 5 [Oblivion].ini': OrderedDict(
        [('General', OrderedDict([('iSaveGameBackupCount', '5')]))]),
    'Screenshot, Enabled [Oblivion].ini': OrderedDict(
        [('Display', OrderedDict([('bAllowScreenShot', '1')]))]),
    'Screenshot, ~Disabled [Oblivion].ini': OrderedDict(
        [('Display', OrderedDict([('bAllowScreenShot', '0')]))]),
    'ShadowMapResolution, 1024 [Oblivion].ini': OrderedDict(
        [('Display', OrderedDict([('iShadowMapResolution', '1024')]))]),
    'ShadowMapResolution, ~256 [Oblivion].ini': OrderedDict(
        [('Display', OrderedDict([('iShadowMapResolution', '256')]))]),
    'Sound Card Channels, 128 [Oblivion].ini': OrderedDict(
        [('Audio', OrderedDict([('iMaxImpactSoundCount', '128')]))]),
    'Sound Card Channels, 16 [Oblivion].ini': OrderedDict(
        [('Audio', OrderedDict([('iMaxImpactSoundCount', '16')]))]),
    'Sound Card Channels, 192 [Oblivion].ini': OrderedDict(
        [('Audio', OrderedDict([('iMaxImpactSoundCount', '192')]))]),
    'Sound Card Channels, 24 [Oblivion].ini': OrderedDict(
        [('Audio', OrderedDict([('iMaxImpactSoundCount', '24')]))]),
    'Sound Card Channels, 48 [Oblivion].ini': OrderedDict(
        [('Audio', OrderedDict([('iMaxImpactSoundCount', '48')]))]),
    'Sound Card Channels, 64 [Oblivion].ini': OrderedDict(
        [('Audio', OrderedDict([('iMaxImpactSoundCount', '64')]))]),
    'Sound Card Channels, 8 [Oblivion].ini': OrderedDict(
        [('Audio', OrderedDict([('iMaxImpactSoundCount', '8')]))]),
    'Sound Card Channels, 96 [Oblivion].ini': OrderedDict(
        [('Audio', OrderedDict([('iMaxImpactSoundCount', '96')]))]),
    'Sound Card Channels, ~32 [Oblivion].ini': OrderedDict(
        [('Audio', OrderedDict([('iMaxImpactSoundCount', '32')]))]),
    'Sound, Disabled [Oblivion].ini': OrderedDict(
        [('Audio', OrderedDict([('bSoundEnabled', '0')]))]),
    'Sound, ~Enabled [Oblivion].ini': OrderedDict(
        [('Audio', OrderedDict([('bSoundEnabled', '1')]))])
}
