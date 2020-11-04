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
"""Temp module, contains the Race Records patcher."""
import random
import re
from collections import defaultdict
# Internal
from .base import Patcher
from ... import bush
from ...bolt import GPath

# Utilities & Constants -------------------------------------------------------

_main_master = GPath(bush.game.master_file)
_dremora_race = (_main_master, 0x038010)

#------------------------------------------------------------------------------
# Race Patcher ----------------------------------------------------------------
#------------------------------------------------------------------------------
class RacePatcher(Patcher):
    """Race patcher."""
    group = _(u'Special')
    scanOrder = 40
    editOrder = 40
    _read_write_records = ('RACE', 'HAIR', 'NPC_',)

    def __init__(self, p_name, p_file):
        super(RacePatcher, self).__init__(p_name, p_file)
        self.isActive = True #--Always enabled to support hair filtering
        self.scanTypes = {'RACE', 'HAIR', 'NPC_'}

    def scanModFile(self, modFile, progress):
        """Add appropriate records from modFile."""
        if not (set(modFile.tops) & self.scanTypes): return
        #--Hair
        for type in ('HAIR',):
            patchBlock = getattr(self.patchFile,type)
            id_records = patchBlock.id_records
            for record in getattr(modFile,type).getActiveRecords():
                if record.fid not in id_records:
                    patchBlock.setRecord(record.getTypeCopy())
        #--Npcs with missing hair
        patchBlock = self.patchFile.NPC_
        id_records = patchBlock.id_records
        for record in modFile.NPC_.getActiveRecords():
            if record.fid not in id_records: ##: hair conditions
                patchBlock.setRecord(record.getTypeCopy())

    def buildPatch(self,log,progress):
        """Updates races as needed."""
        if not self.isActive: return
        patchFile = self.patchFile
        keep = patchFile.getKeeper()
        if 'RACE' not in patchFile.tops: return
        racesSorted = []
        mod_npcsFixed = defaultdict(set)
        reProcess = re.compile(
            u'(?:dremora)|(?:akaos)|(?:lathulet)|(?:orthe)|(?:ranyu)',
            re.I | re.U)
        #--Sort Hair
        defaultMaleHair = {}
        defaultFemaleHair = {}
        hairNames = dict((x.fid,x.full) for x in patchFile.HAIR.records)
        maleHairs = set(
            x.fid for x in patchFile.HAIR.records if not x.flags.notMale)
        femaleHairs = set(
            x.fid for x in patchFile.HAIR.records if not x.flags.notFemale)
        for race in patchFile.RACE.records:
            if race.flags.playable or race.fid == _dremora_race:
                defaultMaleHair[race.fid] = [x for x in race.hairs if
                                             x in maleHairs]
                defaultFemaleHair[race.fid] = [x for x in race.hairs if
                                               x in femaleHairs]
                race.hairs.sort(key=lambda x: hairNames.get(x))
                racesSorted.append(race.eid)
                keep(race.fid)
        #--Npcs with unassigned hair
        for npc in patchFile.NPC_.records:
            if npc.fid == (_main_master, 0x000007): continue  #
            # skip player
            if npc.full is not None and npc.race == (
                    _main_master, 0x038010) and not reProcess.search(
                    npc.full): continue
            random.seed(npc.fid[1]) # make it deterministic
            raceHair = (
                (defaultMaleHair, defaultFemaleHair)[npc.flags.female]).get(
                npc.race)
            if not npc.hair and raceHair:
                npc.hair = random.choice(raceHair)
                mod_npcsFixed[npc.fid[0]].add(npc.fid)
                keep(npc.fid)
            if not npc.hairLength:
                npc.hairLength = random.random()
                mod_npcsFixed[npc.fid[0]].add(npc.fid)
                keep(npc.fid)
        #--Done
        log.setHeader(u'= ' + self._patcher_name)
        log(u'\n=== ' + _(u'Hair Sorted'))
        if not racesSorted:
            log(u'. ~~%s~~' % _(u'None'))
        else:
            for eid in sorted(racesSorted):
                log(u'* ' + eid)
        if mod_npcsFixed:
            log(u'\n=== ' + _(u'Hair Assigned for NPCs'))
            for srcMod in sorted(mod_npcsFixed):
                log(u'* %s: %d' % (srcMod.s,len(mod_npcsFixed[srcMod])))
