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

"""This module contains oblivion multitweak item patcher classes that belong
to the Actors Multitweaker - as well as the TweakActors itself."""

import random
import re
# Internal
from ... import bass # for dirs
from ...bolt import GPath
from ...cint import FormID
from ...exception import AbstractError
from ...patcher.base import AMultiTweakItem
from .base import MultiTweakItem, CBash_MultiTweakItem, MultiTweaker, \
    CBash_MultiTweaker

# Patchers: 30 ----------------------------------------------------------------
class BasalNPCTweaker(MultiTweakItem):
    """Base for all NPC tweakers"""
    tweak_read_classes = 'NPC_',

    #--Patch Phase ------------------------------------------------------------
    def scanModFile(self,modFile,progress,patchFile):
        mapper = modFile.getLongMapper()
        patchRecords = patchFile.NPC_
        for record in modFile.NPC_.getActiveRecords():
            record = record.getTypeCopy(mapper)
            patchRecords.setRecord(record)

    def buildPatch(self,log,progress,patchFile): raise AbstractError

class BasalCreatureTweaker(MultiTweakItem):
    """Base for all Creature tweakers"""
    tweak_read_classes = 'CREA',

    #--Patch Phase ------------------------------------------------------------
    def scanModFile(self,modFile,progress,patchFile):
        mapper = modFile.getLongMapper()
        patchRecords = patchFile.CREA
        for record in modFile.CREA.getActiveRecords():
            record = record.getTypeCopy(mapper)
            patchRecords.setRecord(record)

    def buildPatch(self,log,progress,patchFile): raise AbstractError

class _NpcCTweak(CBash_MultiTweakItem):
    tweak_read_classes = 'NPC_',

class _CreaCTweak(CBash_MultiTweakItem):
    tweak_read_classes = 'CREA',

#------------------------------------------------------------------------------
class AMAONPCSkeletonPatcher(AMultiTweakItem):
    """Changes all NPCs to use the right Mayu's Animation Overhaul Skeleton
    for use with MAO."""

    #--Config Phase -----------------------------------------------------------
    def __init__(self):
        super(AMAONPCSkeletonPatcher, self).__init__(
            _("Mayu's Animation Overhaul Skeleton Tweaker"),
            _('Changes all (modded and vanilla) NPCs to use the MAO '
              'skeletons.  Not compatible with VORB.  Note: ONLY use if '
              'you have MAO installed.'),
            'MAO Skeleton',
            (_('All NPCs'), 0),
            (_('Only Female NPCs'), 1),
            (_('Only Male NPCs'), 2),
            )
        self.logHeader = '=== '+_('MAO Skeleton Setter')
        self.logMsg = '* '+_('Skeletons Tweaked') + ': %d'

class MAONPCSkeletonPatcher(AMAONPCSkeletonPatcher,BasalNPCTweaker):
    def buildPatch(self,log,progress,patchFile):
        """Edits patch file as desired. Will write to log."""
        count = {}
        keep = patchFile.getKeeper()
        for record in patchFile.NPC_.records:
            if self.choiceValues[self.chosen][
                0] == 1 and not record.flags.female:
                continue
            elif self.choiceValues[self.chosen][
                0] == 2 and record.flags.female:
                continue
            if record.fid == (GPath('Oblivion.esm'), 0x000007): continue  #
            # skip player record
            try:
                oldModPath = record.model.modPath
            except AttributeError:  # for freaking weird esps with NPC's
                # with no skeleton assigned to them(!)
                continue
            newModPath = "Mayu's Projects[M]\\Animation " \
                         "Overhaul\\Vanilla\\SkeletonBeast.nif"
            try:
                if oldModPath.lower() == \
                        'characters\\_male\\skeletonsesheogorath.nif':
                    newModPath = "Mayu's Projects[M]\\Animation " \
                                 "Overhaul\\Vanilla\\SkeletonSESheogorath.nif"
            except AttributeError:  # in case modPath was None. Try/Except
                # has no overhead if exception isn't thrown.
                pass
            if newModPath != oldModPath:
                record.model.modPath = newModPath
                keep(record.fid)
                srcMod = record.fid[0]
                count[srcMod] = count.get(srcMod,0) + 1
        self._patchLog(log,count)

class CBash_MAONPCSkeletonPatcher(AMAONPCSkeletonPatcher, _NpcCTweak):
    name = _("MAO Skeleton Setter")

    #--Config Phase -----------------------------------------------------------
    def __init__(self):
        super(CBash_MAONPCSkeletonPatcher, self).__init__()
        self.playerFid = FormID(GPath('Oblivion.esm'), 0x000007)

    #--Patch Phase ------------------------------------------------------------
    def apply(self,modFile,record,bashTags):
        """Edits patch file as desired. """
        if record.fid != self.playerFid: #skip player record
            choice = self.choiceValues[self.chosen][0]
            if choice == 1 and record.IsMale: return
            elif choice == 2 and record.IsFemale: return
            oldModPath = record.modPath
            newModPath = "Mayu's Projects[M]\\Animation " \
                         "Overhaul\\Vanilla\\SkeletonBeast.nif"
            try:
                if oldModPath == \
                        'characters\\_male\\skeletonsesheogorath.nif':  #
                    # modPaths do case insensitive comparisons by default
                    newModPath = "Mayu's Projects[M]\\Animation " \
                                 "Overhaul\\Vanilla\\SkeletonSESheogorath.nif"
            except AttributeError:  # in case modPath was None. Try/Except
                # has no overhead if exception isn't thrown.
                pass
            if newModPath != oldModPath:
                override = record.CopyAsOverride(self.patchFile)
                if override:
                    override.modPath = newModPath
                    self.mod_count[modFile.GName] += 1
                    record.UnloadRecord()
                    record._RecordID = override._RecordID

#------------------------------------------------------------------------------
class AVORB_NPCSkeletonPatcher(AMultiTweakItem):
    """Changes all NPCs to use the diverse skeleton for different look."""
    #--Config Phase -----------------------------------------------------------
    def __init__(self):
        super(AVORB_NPCSkeletonPatcher, self).__init__(
            _("VadersApp's Oblivion Real Bodies Skeleton Tweaker"),
            _("Changes all (modded and vanilla) NPCs to use diverse "
              "skeletons for different look.  Not compatible with MAO, "
              "Requires VadersApp's Oblivion Real Bodies."),
            'VORB',
            (_('All NPCs'), 0),
            (_('Only Female NPCs'), 1),
            (_('Only Male NPCs'), 2),
            )
        self.logHeader = '=== '+_("VadersApp's Oblivion Real Bodies")
        self.logMsg = '* '+_('Skeletons Tweaked') + ': %d'

    @staticmethod
    def _initSkeletonCollections():
        """ construct skeleton mesh collections
            skeletonList gets files that match the pattern "skel_*.nif",
            but not "skel_special_*.nif"
            skeletonSetSpecial gets files that match "skel_special_*.nif" """
        # Since bass.dirs hasn't been populated when __init__ executes,
        # we do this here
        skeletonDir = bass.dirs['mods'].join('Meshes', 'Characters',
                                                  '_male')
        list_skel_dir = skeletonDir.list() # empty if dir does not exist
        skel_nifs = [x for x in list_skel_dir if
                     x.cs.startswith('skel_') and x.cext == '.nif']
        skeletonList = [x for x in skel_nifs if
                        not x.cs.startswith('skel_special_')]
        set_skeletonList = set(skeletonList)
        skeletonSetSpecial = set(
            x.s for x in skel_nifs if x not in set_skeletonList)
        return skeletonList, skeletonSetSpecial

class VORB_NPCSkeletonPatcher(AVORB_NPCSkeletonPatcher,BasalNPCTweaker):
    def buildPatch(self,log,progress,patchFile):
        """Edits patch file as desired.  Will write to log."""
        count = {}
        keep = patchFile.getKeeper()
        #--Some setup
        modSkeletonDir = GPath('Characters').join('_male')
        skeletonList, skeletonSetSpecial = \
            AVORB_NPCSkeletonPatcher._initSkeletonCollections()
        if skeletonList:
            femaleOnly = self.choiceValues[self.chosen][0] == 1
            maleOnly = self.choiceValues[self.chosen][0] == 2
            playerFid = (GPath('Oblivion.esm'),0x000007)
            for record in patchFile.NPC_.records:
                # skip records (male only, female only, player)
                if femaleOnly and not record.flags.female: continue
                elif maleOnly and record.flags.female: continue
                if record.fid == playerFid: continue
                try:
                    oldModPath = record.model.modPath
                except AttributeError:  # for freaking weird esps with
                    # NPC's with no skeleton assigned to them(!)
                    continue
                specialSkelMesh = "skel_special_%X.nif" % record.fid[1]
                if specialSkelMesh in skeletonSetSpecial:
                    newModPath = modSkeletonDir.join(specialSkelMesh)
                else:
                    random.seed(record.fid)
                    randomNumber = random.randint(1, len(skeletonList))-1
                    newModPath = modSkeletonDir.join(
                        skeletonList[randomNumber])
                if newModPath != oldModPath:
                    record.model.modPath = newModPath.s
                    keep(record.fid)
                    srcMod = record.fid[0]
                    count[srcMod] = count.get(srcMod,0) + 1
        self._patchLog(log, count)

class CBash_VORB_NPCSkeletonPatcher(AVORB_NPCSkeletonPatcher, _NpcCTweak):
    name = _("VORB Skeleton Setter")

    #--Config Phase -----------------------------------------------------------
    def __init__(self):
        super(CBash_VORB_NPCSkeletonPatcher, self).__init__()
        self.modSkeletonDir = GPath('Characters').join('_male')
        self.playerFid = FormID(GPath('Oblivion.esm'), 0x000007)
        self.skeletonList = None
        self.skeletonSetSpecial = None

    #--Patch Phase ------------------------------------------------------------
    def apply(self,modFile,record,bashTags):
        """Edits patch file as desired. """
        recordId = record.fid
        if recordId != self.playerFid: #skip player record
            choice = self.choiceValues[self.chosen][0]
            if choice == 1 and record.IsMale: return
            elif choice == 2 and record.IsFemale: return
            if self.skeletonList is None:
                self.skeletonList, self.skeletonSetSpecial = \
                    AVORB_NPCSkeletonPatcher._initSkeletonCollections()
            if len(self.skeletonList) == 0: return
            try:
                oldModPath = record.modPath.lower()
            except AttributeError:  # for freaking weird esps with NPC's with
                # no skeleton assigned to them(!)
                pass
            specialSkelMesh = "skel_special_%X.nif" % recordId[1]
            if specialSkelMesh in self.skeletonSetSpecial:
                newModPath = self.modSkeletonDir.join(specialSkelMesh)
            else:
                random.seed(recordId)
                randomNumber = random.randint(1, len(self.skeletonList)) - 1
                newModPath = self.modSkeletonDir.join(
                    self.skeletonList[randomNumber])
            if newModPath.cs != oldModPath:
                override = record.CopyAsOverride(self.patchFile)
                if override:
                    override.modPath = newModPath.s
                    self.mod_count[modFile.GName] += 1
                    record.UnloadRecord()
                    record._RecordID = override._RecordID

#------------------------------------------------------------------------------
class AVanillaNPCSkeletonPatcher(AMultiTweakItem):
    """Changes all NPCs to use the vanilla beast race skeleton."""

    #--Config Phase -----------------------------------------------------------
    def __init__(self):
        super(AVanillaNPCSkeletonPatcher, self).__init__(
            _("Vanilla Beast Skeleton Tweaker"),
            _('Avoids visual glitches if an NPC is a beast race but has '
              'the regular skeleton.nif selected, but can cause '
              'performance issues.'),
            'Vanilla Skeleton',
            ('1.0',  '1.0'),
            )
        self.logHeader = '=== '+_('Vanilla Beast Skeleton')
        self.logMsg = '* '+_('Skeletons Tweaked') + ': %d'

class VanillaNPCSkeletonPatcher(AVanillaNPCSkeletonPatcher,BasalNPCTweaker):
    #--Patch Phase ------------------------------------------------------------
    def scanModFile(self,modFile,progress,patchFile):
        mapper = modFile.getLongMapper()
        patchRecords = patchFile.NPC_
        for record in modFile.NPC_.getActiveRecords():
            record = record.getTypeCopy(mapper)
            if not record.model: continue #for freaking weird esps with NPC's
            # with no skeleton assigned to them(!)
            model = record.model.modPath
            if model.lower() == 'characters\\_male\\skeleton.nif':
                patchRecords.setRecord(record)

    def buildPatch(self,log,progress,patchFile):
        """Edits patch file as desired. Will write to log."""
        count = {}
        keep = patchFile.getKeeper()
        newModPath = "Characters\\_Male\\SkeletonBeast.nif"
        for record in patchFile.NPC_.records:
            try:
                oldModPath = record.model.modPath
            except AttributeError: #for freaking weird esps with NPC's with no
                # skeleton assigned to them(!)
                continue
            try:
                if oldModPath.lower() != 'characters\\_male\\skeleton.nif':
                    continue
            except AttributeError: #in case oldModPath was None. Try/Except has
                # no overhead if exception isn't thrown.
                pass
            if newModPath != oldModPath:
                record.model.modPath = newModPath
                keep(record.fid)
                srcMod = record.fid[0]
                count[srcMod] = count.get(srcMod,0) + 1
        self._patchLog(log,count)

class CBash_VanillaNPCSkeletonPatcher(AVanillaNPCSkeletonPatcher, _NpcCTweak):
    scanOrder = 31 #Run before MAO
    editOrder = 31
    name = _("Vanilla Beast Skeleton")

    #--Patch Phase ------------------------------------------------------------
    def apply(self,modFile,record,bashTags):
        """Edits patch file as desired. """
        oldModPath = record.modPath
        newModPath = "Characters\\_Male\\SkeletonBeast.nif"
        try:
            if oldModPath != 'characters\\_male\\skeleton.nif': #modPaths do
                # case insensitive comparisons by default
                return
        except AttributeError: #in case modPath was None. Try/Except has no
            # overhead if exception isn't thrown.
            pass
        if newModPath != oldModPath:
            override = record.CopyAsOverride(self.patchFile)
            if override:
                override.modPath = newModPath
                self.mod_count[modFile.GName] += 1
                record.UnloadRecord()
                record._RecordID = override._RecordID

#------------------------------------------------------------------------------
class ARedguardNPCPatcher(AMultiTweakItem):
    """Changes all Redguard NPCs texture symmetry for Better Redguard
    Compatibility."""

    #--Config Phase -----------------------------------------------------------
    def __init__(self):
        super(ARedguardNPCPatcher, self).__init__(_("Redguard FGTS Nuller"),
            _('Nulls FGTS of all Redguard NPCs - for compatibility with'
              ' Better Redguards.'),
            'RedguardFGTSPatcher',
            ('1.0',  '1.0'),
            )
        self.logHeader = '=== '+_('Redguard FGTS Patcher')
        self.logMsg = '* '+_('Redguard NPCs Tweaked') + ': %d'

class RedguardNPCPatcher(ARedguardNPCPatcher,BasalNPCTweaker):
    def buildPatch(self,log,progress,patchFile):
        """Edits patch file as desired. Will write to log."""
        count = {}
        keep = patchFile.getKeeper()
        for record in patchFile.NPC_.records:
            if not record.race: continue
            if record.race[1] == 0x00d43:
                record.fgts_p = '\x00'*200
                keep(record.fid)
                srcMod = record.fid[0]
                count[srcMod] = count.get(srcMod,0) + 1
        self._patchLog(log,count)

class CBash_RedguardNPCPatcher(ARedguardNPCPatcher, _NpcCTweak):
    name = _("Redguard FGTS Patcher")
    redguardId = FormID(GPath('Oblivion.esm'),0x00000D43)

    #--Patch Phase ------------------------------------------------------------
    def apply(self,modFile,record,bashTags):
        """Edits patch file as desired. """
        if record.race == self.__class__.redguardId: #Only affect npc's with
            # the Redguard race
            oldFGTS_p = record.fgts_p
            newFGTS_p = [0x00] * 200
            if newFGTS_p != oldFGTS_p:
                override = record.CopyAsOverride(self.patchFile)
                if override:
                    override.fgts_p = newFGTS_p
                    self.mod_count[modFile.GName] += 1
                    record.UnloadRecord()
                    record._RecordID = override._RecordID

#------------------------------------------------------------------------------
class ANoBloodCreaturesPatcher(AMultiTweakItem):
    """Set all creatures to have no blood records."""

    #--Config Phase -----------------------------------------------------------
    def __init__(self):
        super(ANoBloodCreaturesPatcher, self).__init__(
            _("No Bloody Creatures"),
            _("Set all creatures to have no blood records, will have "
              "pretty much no effect when used with MMM since the MMM "
              "blood uses a different system."),
            'No bloody creatures',
            ('1.0',  '1.0'),
            )
        self.logMsg = '* '+_('Creatures Tweaked') + ': %d'

class NoBloodCreaturesPatcher(ANoBloodCreaturesPatcher,BasalCreatureTweaker):
    def buildPatch(self,log,progress,patchFile):
        """Edits patch file as desired. Will write to log."""
        count = {}
        keep = patchFile.getKeeper()
        for record in patchFile.CREA.records:
            if record.bloodDecalPath or record.bloodSprayPath:
                record.bloodDecalPath = None
                record.bloodSprayPath = None
                record.flags.noBloodSpray = True
                record.flags.noBloodDecal = True
                keep(record.fid)
                srcMod = record.fid[0]
                count[srcMod] = count.get(srcMod,0) + 1
        #--Log
        self._patchLog(log, count)

class CBash_NoBloodCreaturesPatcher(ANoBloodCreaturesPatcher, _CreaCTweak):
    name = _("No Bloody Creatures")

    #--Patch Phase ------------------------------------------------------------
    def apply(self,modFile,record,bashTags):
        """Edits patch file as desired. """
        if record.bloodDecalPath or record.bloodSprayPath:
            override = record.CopyAsOverride(self.patchFile)
            if override:
                override.bloodDecalPath = None
                override.bloodSprayPath = None
                override.IsNoBloodSpray = True
                override.IsNoBloodDecal = True
                self.mod_count[modFile.GName] += 1
                record.UnloadRecord()
                record._RecordID = override._RecordID

#------------------------------------------------------------------------------
class AAsIntendedImpsPatcher(AMultiTweakItem):
    """Set all imps to have the Bethesda imp spells that were never assigned
    (discovered by the UOP team, made into a mod by Tejon)."""
    reImpModPath = re.compile('' r'(imp(?!erial)|gargoyle)\\.', re.I | re.U)
    reImp  = re.compile('(imp(?!erial)|gargoyle)',re.I|re.U)

    #--Config Phase -----------------------------------------------------------
    def __init__(self):
        super(AAsIntendedImpsPatcher, self).__init__(_('As Intended: Imps'),
            _("Set imps to have the unassigned Bethesda Imp Spells as"
              " discovered by the UOP team and made into a mod by Tejon."),
            'vicious imps!',
            (_('All imps'), 'all'),
            (_('Only fullsize imps'), 'big'),
            (_('Only implings'), 'small'),
            )
        self.logMsg = '* '+_('Imps Tweaked') + ': %d'

class AsIntendedImpsPatcher(AAsIntendedImpsPatcher,BasalCreatureTweaker):
    def buildPatch(self,log,progress,patchFile):
        """Edits patch file as desired. Will write to log."""
        count = {}
        keep = patchFile.getKeeper()
        spell = (GPath('Oblivion.esm'), 0x02B53F)
        reImp  = self.reImp
        reImpModPath = self.reImpModPath
        for record in patchFile.CREA.records:
            try:
                oldModPath = record.model.modPath
            except AttributeError:
                continue
            if not reImpModPath.search(oldModPath or ''): continue

            for bodyPart in record.bodyParts:
                if reImp.search(bodyPart):
                    break
            else:
                continue
            if record.baseScale < 0.4:
                if 'big' in self.choiceValues[self.chosen]:
                    continue
            elif 'small' in self.choiceValues[self.chosen]:
                continue
            if spell not in record.spells:
                record.spells.append(spell)
                keep(record.fid)
                srcMod = record.fid[0]
                count[srcMod] = count.get(srcMod,0) + 1
        self._patchLog(log,count)

class CBash_AsIntendedImpsPatcher(AAsIntendedImpsPatcher, _CreaCTweak):
    name = _("As Intended: Imps")
    spell = FormID(GPath('Oblivion.esm'), 0x02B53F)

    #--Patch Phase ------------------------------------------------------------
    def apply(self,modFile,record,bashTags):
        """Edits patch file as desired. """
        if not self.reImpModPath.search(record.modPath or ''): return
        reImp  = self.reImp
        for bodyPart in record.bodyParts:
            if reImp.search(bodyPart):
                break
        else:
            return
        if record.baseScale < 0.4:
            if 'big' in self.choiceValues[self.chosen]:
                return
        elif 'small' in self.choiceValues[self.chosen]:
            return
        spells = record.spells
        newSpell = self.spell
        if newSpell not in spells:
            override = record.CopyAsOverride(self.patchFile)
            if override:
                spells.append(newSpell)
                override.spells = spells
                self.mod_count[modFile.GName] += 1
                record.UnloadRecord()
                record._RecordID = override._RecordID

#------------------------------------------------------------------------------
class AAsIntendedBoarsPatcher(AMultiTweakItem):
    """Set all boars to have the Bethesda boar spells that were never
    assigned (discovered by the UOP team, made into a mod by Tejon)."""
    reBoarModPath = re.compile('' r'(boar)\\.', re.I | re.U)
    reBoar  = re.compile('(boar)', re.I|re.U)

    #--Config Phase -----------------------------------------------------------
    def __init__(self):
        super(AAsIntendedBoarsPatcher, self).__init__(_('As Intended: Boars'),
            _("Set boars to have the unassigned Bethesda Boar Spells as"
              " discovered by the UOP team and made into a mod by Tejon."),
            'vicious boars!',
            ('1.0',  '1.0'),
            )
        self.logMsg = '* '+_('Boars Tweaked') + ': %d'

class AsIntendedBoarsPatcher(AAsIntendedBoarsPatcher,BasalCreatureTweaker):
    def buildPatch(self,log,progress,patchFile):
        """Edits patch file as desired. Will write to log."""
        count = {}
        spell = (GPath('Oblivion.esm'), 0x02B54E)
        keep = patchFile.getKeeper()
        reBoar  = self.reBoar
        reBoarModPath = self.reBoarModPath
        for record in patchFile.CREA.records:
            try:
                oldModPath = record.model.modPath
            except AttributeError:
                continue
            if not reBoarModPath.search(oldModPath or ''): continue

            for bodyPart in record.bodyParts:
                if reBoar.search(bodyPart):
                    break
            else:
                continue
            if spell not in record.spells:
                record.spells.append(spell)
                keep(record.fid)
                srcMod = record.fid[0]
                count[srcMod] = count.get(srcMod,0) + 1
        self._patchLog(log,count)

class CBash_AsIntendedBoarsPatcher(AAsIntendedBoarsPatcher, _CreaCTweak):
    name = _("As Intended: Boars")
    spell = FormID(GPath('Oblivion.esm'), 0x02B54E)

    #--Patch Phase ------------------------------------------------------------
    def apply(self,modFile,record,bashTags):
        """Edits patch file as desired. """
        if not self.reBoarModPath.search(record.modPath or ''): return
        reBoar  = self.reBoar
        for bodyPart in record.bodyParts:
            if reBoar.search(bodyPart):
                break
        else:
            return
        spells = record.spells
        newSpell = self.spell
        if newSpell not in spells:
            override = record.CopyAsOverride(self.patchFile)
            if override:
                spells.append(newSpell)
                override.spells = spells
                self.mod_count[modFile.GName] += 1
                record.UnloadRecord()
                record._RecordID = override._RecordID

#------------------------------------------------------------------------------
class ASWALKNPCAnimationPatcher(AMultiTweakItem):
    """Changes all female NPCs to use Mur Zuk's Sexy Walk."""

    #--Config Phase -----------------------------------------------------------
    def __init__(self):
        super(ASWALKNPCAnimationPatcher, self).__init__(
            _("Sexy Walk for female NPCs"),
            _("Changes all female NPCs to use Mur Zuk's Sexy Walk - "
              "Requires Mur Zuk's Sexy Walk animation file."),
            'Mur Zuk SWalk',
            ('1.0',  '1.0'),
            )
        self.logMsg = '* '+_('NPCs Tweaked') + ' :%d'

class SWALKNPCAnimationPatcher(ASWALKNPCAnimationPatcher,BasalNPCTweaker):
    def buildPatch(self,log,progress,patchFile):
        """Edits patch file as desired. Will write to log."""
        count = {}
        keep = patchFile.getKeeper()
        for record in patchFile.NPC_.records:
            if record.flags.female == 1:
                record.animations += ['0sexywalk01.kf']
                keep(record.fid)
                srcMod = record.fid[0]
                count[srcMod] = count.get(srcMod,0) + 1
        self._patchLog(log,count)

class CBash_SWALKNPCAnimationPatcher(ASWALKNPCAnimationPatcher, _NpcCTweak):
    name = _("Sexy Walk for female NPCs")
    playerFid = FormID(GPath('Oblivion.esm'), 0x000007)

    #--Patch Phase ------------------------------------------------------------
    def apply(self,modFile,record,bashTags):
        """Edits patch file as desired. """
        if record.fid != self.playerFid: #skip player record
            if record.IsFemale:
                override = record.CopyAsOverride(self.patchFile)
                if override:
                    override.animations += ['0sexywalk01.kf']
                    self.mod_count[modFile.GName] += 1
                    record.UnloadRecord()
                    record._RecordID = override._RecordID

#------------------------------------------------------------------------------
class ARWALKNPCAnimationPatcher(AMultiTweakItem):
    """Changes all female NPCs to use Mur Zuk's Real Walk."""

    #--Config Phase -----------------------------------------------------------
    def __init__(self):
        super(ARWALKNPCAnimationPatcher, self).__init__(
            _("Real Walk for female NPCs"),
            _("Changes all female NPCs to use Mur Zuk's Real Walk - "
              "Requires Mur Zuk's Real Walk animation file."),
            'Mur Zuk RWalk',
            ('1.0',  '1.0'),
            )
        self.logMsg = '* '+_('NPCs Tweaked') + ': %d'

class RWALKNPCAnimationPatcher(ARWALKNPCAnimationPatcher,BasalNPCTweaker):
    def buildPatch(self,log,progress,patchFile):
        """Edits patch file as desired. Will write to log."""
        count = {}
        keep = patchFile.getKeeper()
        for record in patchFile.NPC_.records:
            if record.flags.female == 1:
                record.animations += ['0realwalk01.kf']
                keep(record.fid)
                srcMod = record.fid[0]
                count[srcMod] = count.get(srcMod,0) + 1
        self._patchLog(log,count)

class CBash_RWALKNPCAnimationPatcher(ARWALKNPCAnimationPatcher, _NpcCTweak):
    name = _("Real Walk for female NPCs")
    playerFid = FormID(GPath('Oblivion.esm'), 0x000007)

    #--Patch Phase ------------------------------------------------------------
    def apply(self,modFile,record,bashTags):
        """Edits patch file as desired. """
        if record.fid != self.playerFid: #skip player record
            if record.IsFemale:
                override = record.CopyAsOverride(self.patchFile)
                if override:
                    override.animations += ['0realwalk01.kf']
                    self.mod_count[modFile.GName] += 1
                    record.UnloadRecord()
                    record._RecordID = override._RecordID

#------------------------------------------------------------------------------
class AQuietFeetPatcher(AMultiTweakItem):
    """Removes 'foot' sounds from all/specified creatures - like the mod by
    the same name but works on all modded creatures."""

    #--Config Phase -----------------------------------------------------------
    def __init__(self):
        super(AQuietFeetPatcher, self).__init__(_('Quiet Feet'),
            _("Removes all/some 'foot' sounds from creatures; on some"
              " computers can have a significant performance boost."),
            'silent n sneaky!',
            (_('All Creature Foot Sounds'), 'all'),
            (_('Only 4 Legged Creature Foot Sounds'), 'partial'),
            (_('Only Mount Foot Sounds'), 'mounts'),
            )
        self.logMsg = '* '+_('Creatures Tweaked') + ': %d'

class QuietFeetPatcher(AQuietFeetPatcher,BasalCreatureTweaker):
    def buildPatch(self,log,progress,patchFile):
        """Edits patch file as desired. Will write to log."""
        count = {}
        keep = patchFile.getKeeper()
        chosen = self.choiceValues[self.chosen][0]
        for record in patchFile.CREA.records:
            sounds = record.sounds
            if chosen == 'all':
                sounds = [sound for sound in sounds if
                          sound.type not in [0, 1, 2, 3]]
            elif chosen == 'partial':
                for sound in record.sounds:
                    if sound.type in [2,3]:
                        sounds = [sound for sound in sounds if
                                  sound.type not in [0, 1, 2, 3]]
                        break
            else: # really is: "if chosen == 'mounts':", but less cpu to do it
                # as else.
                if record.creatureType == 4:
                    sounds = [sound for sound in sounds if
                              sound.type not in [0, 1, 2, 3]]
            if sounds != record.sounds:
                record.sounds = sounds
                keep(record.fid)
                srcMod = record.fid[0]
                count[srcMod] = count.get(srcMod,0) + 1
        self._patchLog(log,count)

class CBash_QuietFeetPatcher(AQuietFeetPatcher, _CreaCTweak):
    name = _("Quiet Feet")

    #--Patch Phase ------------------------------------------------------------
    def apply(self,modFile,record,bashTags):
        """Edits patch file as desired. """
        chosen = self.choiceValues[self.chosen][0]
        if chosen == 'partial':
            for sound in record.sounds:
                if sound.IsLeftBackFoot or sound.IsRightBackFoot:
                    break
            else:
                return
        elif chosen == 'mounts' and not record.IsHorse:
            return
        # equality operator not implemented for ObCREARecord.Sound class,
        # so use the list version instead
        # 0 = IsLeftFoot, 1 = IsRightFoot, 2 = IsLeftBackFoot,
        # 3 = IsRightBackFoot
        sounds_list = [(soundType, sound, chance) for soundType, sound, chance
                       in record.sounds_list if soundType not in [0, 1, 2, 3]]
        if sounds_list != record.sounds_list:
            override = record.CopyAsOverride(self.patchFile)
            if override:
                override.sounds_list = sounds_list
                self.mod_count[modFile.GName] += 1
                record.UnloadRecord()
                record._RecordID = override._RecordID

#------------------------------------------------------------------------------
class AIrresponsibleCreaturesPatcher(AMultiTweakItem):
    """Sets responsibility to 0 for all/specified creatures - like the mod
    by the name of Irresponsible Horses but works on all modded creatures."""

    #--Config Phase -----------------------------------------------------------
    def __init__(self):
        super(AIrresponsibleCreaturesPatcher, self).__init__(
            _('Irresponsible Creatures'),
            _("Sets responsibility to 0 for all/specified creatures - so "
              "they can't report you for crimes."),
            'whatbadguarddogs',
            (_('All Creatures'), 'all'),
            (_('Only Horses'), 'mounts'),
            )
        self.logMsg = '* '+_('Creatures Tweaked') + ': %d'

class IrresponsibleCreaturesPatcher(AIrresponsibleCreaturesPatcher,
                                    BasalCreatureTweaker):
    def buildPatch(self,log,progress,patchFile):
        """Edits patch file as desired. Will write to log."""
        count = {}
        keep = patchFile.getKeeper()
        chosen = self.choiceValues[self.chosen][0]
        for record in patchFile.CREA.records:
            if record.responsibility == 0: continue
            if chosen == 'all':
                record.responsibility = 0
                keep(record.fid)
                srcMod = record.fid[0]
                count[srcMod] = count.get(srcMod,0) + 1
            else: # really is: "if chosen == 'mounts':", but less cpu to do it
                # as else.
                if record.creatureType == 4:
                    record.responsibility = 0
                    keep(record.fid)
                    srcMod = record.fid[0]
                    count[srcMod] = count.get(srcMod,0) + 1
        self._patchLog(log,count)

class CBash_IrresponsibleCreaturesPatcher(AIrresponsibleCreaturesPatcher,
                                          _CreaCTweak):
    name = _("Irresponsible Creatures")

    #--Patch Phase ------------------------------------------------------------
    def apply(self,modFile,record,bashTags):
        """Edits patch file as desired. """
        if record.responsibility == 0: return
        if self.choiceValues[self.chosen][
            0] == 'mounts' and not record.IsHorse: return
        override = record.CopyAsOverride(self.patchFile)
        if override:
            override.responsibility = 0
            self.mod_count[modFile.GName] += 1
            record.UnloadRecord()
            record._RecordID = override._RecordID

#------------------------------------------------------------------------------
class TweakActors(MultiTweaker):
    """Sets Creature stuff or NPC Skeletons, Animations or other settings to
    better work with mods or avoid bugs."""
    name = _('Tweak Actors')
    text = _("Tweak NPC and Creatures records in specified ways.")
    tweaks = sorted([
        VORB_NPCSkeletonPatcher(),
        MAONPCSkeletonPatcher(),
        VanillaNPCSkeletonPatcher(),
        RedguardNPCPatcher(),
        NoBloodCreaturesPatcher(),
        AsIntendedImpsPatcher(),
        AsIntendedBoarsPatcher(),
        QuietFeetPatcher(),
        IrresponsibleCreaturesPatcher(),
        RWALKNPCAnimationPatcher(),
        SWALKNPCAnimationPatcher(),
        ],key=lambda a: a.label.lower())

    #--Patch Phase ------------------------------------------------------------
    def getReadClasses(self):
        """Returns load factory classes needed for reading."""
        if not self.isActive: return tuple()
        classTuples = [tweak.getReadClasses() for tweak in self.enabledTweaks]
        return sum(classTuples,tuple())

    def getWriteClasses(self):
        """Returns load factory classes needed for writing."""
        if not self.isActive: return tuple()
        classTuples = [tweak.getWriteClasses() for tweak in self.enabledTweaks]
        return sum(classTuples,tuple())

    def scanModFile(self,modFile,progress):
        if not self.isActive: return
        for tweak in self.enabledTweaks:
            tweak.scanModFile(modFile,progress,self.patchFile)

class CBash_TweakActors(CBash_MultiTweaker):
    """Sets Creature stuff or NPC Skeletons, Animations or other settings to
    better work with mods or avoid bugs."""
    name = _('Tweak Actors')
    text = _("Tweak NPC and Creatures records in specified ways.")
    tweaks = sorted([
        CBash_VORB_NPCSkeletonPatcher(),
        CBash_MAONPCSkeletonPatcher(),
        CBash_VanillaNPCSkeletonPatcher(),
        CBash_RedguardNPCPatcher(),
        CBash_NoBloodCreaturesPatcher(),
        CBash_AsIntendedImpsPatcher(),
        CBash_AsIntendedBoarsPatcher(),
        CBash_QuietFeetPatcher(),
        CBash_IrresponsibleCreaturesPatcher(),
        CBash_RWALKNPCAnimationPatcher(),
        CBash_SWALKNPCAnimationPatcher(),
        ],key=lambda a: a.label.lower())
