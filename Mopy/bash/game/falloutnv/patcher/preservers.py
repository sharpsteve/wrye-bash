# -*- coding: utf-8 -*-
#
# GPL License and Copyright Notice ============================================
#  This file is part of Wrye Bash.
#
#  Wrye Bash is free software: you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation, either version 3
#  of the License, or (at your option) any later version.
#
#  Wrye Bash is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with Wrye Bash.  If not, see <https://www.gnu.org/licenses/>.
#
#  Wrye Bash copyright (C) 2005-2009 Wrye, 2010-2020 Wrye Bash Team
#  https://github.com/wrye-bash
#
# =============================================================================
from ....patcher.patchers.preservers import _APreserver

class WeaponModsPatcher(_APreserver):
    """Merge changes to weapon modifications for FalloutNV."""
    patcher_name = _(u'Import Weapon Modifications')
    patcher_text = _(u'Merges changes to weapon modifications.')
    autoKey = {u'WeaponMods'}
    scanOrder = 27
    editOrder = 27
    rec_attrs = {b'WEAP': (
        u'modelWithMods', u'firstPersonModelWithMods', u'weaponMods',
        u'soundMod1Shoot3Ds', u'soundMod1Shoot2D', u'effectMod1',
        u'effectMod2', u'effectMod3', u'valueAMod1', u'valueAMod2',
        u'valueAMod3', u'valueBMod1', u'valueBMod2', u'valueBMod3',
        u'reloadAnimationMod', u'vatsModReqiured', u'scopeModel',
        u'dnamFlags1.hasScope', u'dnamFlags2.scopeFromMod')}
