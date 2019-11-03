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

# Import all constants from skyrim then edit them as needed

from ..skyrim.constants import *

bethDataFiles = {
    'skyrim.esm',
    'update.esm',
    'dawnguard.esm',
    'dragonborn.esm',
    'hearthfires.esm',
    'skyrim - animations.bsa',
    'skyrim - interface.bsa',
    'skyrim - meshes0.bsa',
    'skyrim - meshes1.bsa',
    'skyrim - misc.bsa',
    'skyrim - patch.bsa',
    'skyrim - shaders.bsa',
    'skyrim - sounds.bsa',
    'skyrim - textures0.bsa',
    'skyrim - textures1.bsa',
    'skyrim - textures2.bsa',
    'skyrim - textures3.bsa',
    'skyrim - textures4.bsa',
    'skyrim - textures5.bsa',
    'skyrim - textures6.bsa',
    'skyrim - textures7.bsa',
    'skyrim - textures8.bsa',
    'skyrim - voices_en0.bsa',
}

# xEdit menu string and key for expert setting
xEdit_expert = (_('SSEEdit Expert'), 'sseView.iKnowWhatImDoing')
