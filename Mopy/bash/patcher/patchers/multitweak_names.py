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
to the Names Multitweaker - as well as the NamesTweaker itself."""

import re
# Internal
from ... import load_order
from ...patcher.base import AMultiTweakItem, AMultiTweaker
from ...patcher.patchers.base import MultiTweakItem, CBash_MultiTweakItem
from ...patcher.patchers.base import MultiTweaker, CBash_MultiTweaker

class _AMultiTweakItem_Names(MultiTweakItem):

    def _patchLog(self, log, count):
        # --Log - Notice self.logMsg is not used - so (apart from
        # NamesTweak_BodyTags and NamesTweak_Body where it is not defined in
        # the ANamesTweak_XX common superclass) the
        # CBash implementations which _do_ use it produce different logs. TODO:
        # unify C/P logs by using self.logMsg (mind the classes mentioned)
        log('* %s: %d' % (self.label,sum(count.values())))
        for srcMod in load_order.get_ordered(list(count.keys())):
            log('  * %s: %d' % (srcMod.s,count[srcMod]))

# Patchers: 30 ----------------------------------------------------------------
class ANamesTweak_BodyTags(AMultiTweakItem):
    #--Config Phase -----------------------------------------------------------
    def __init__(self):
        super(ANamesTweak_BodyTags, self).__init__(
            _("Body Part Codes"),
            _('Sets body part codes used by Armor/Clothes name tweaks. A: '
            'Amulet, R: Ring, etc.'),
            'bodyTags',
            ('ARGHTCCPBS','ARGHTCCPBS'),
            ('ABGHINOPSL','ABGHINOPSL'),)

class NamesTweak_BodyTags(ANamesTweak_BodyTags,MultiTweakItem):

    def buildPatch(self,log,progress,patchFile):
        """Edits patch file as desired. Will write to log."""
        patchFile.bodyTags = self.choiceValues[self.chosen][0]

class CBash_NamesTweak_BodyTags(ANamesTweak_BodyTags,CBash_MultiTweakItem):

    def buildPatchLog(self,log):
        """Will write to log."""
        pass

#------------------------------------------------------------------------------
class NamesTweak_Body(_AMultiTweakItem_Names):
    """Names tweaker for armor and clothes."""
    #--Patch Phase ------------------------------------------------------------
    def getReadClasses(self):
        """Returns load factory classes needed for reading."""
        return self.key,

    def getWriteClasses(self):
        """Returns load factory classes needed for writing."""
        return self.key,

    def scanModFile(self,modFile,progress,patchFile):
        mapper = modFile.getLongMapper()
        patchBlock = getattr(patchFile,self.key)
        id_records = patchBlock.id_records
        for record in getattr(modFile,self.key).getActiveRecords():
            if record.full and mapper(record.fid) not in id_records:
                record = record.getTypeCopy(mapper)
                patchBlock.setRecord(record)

    def buildPatch(self,log,progress,patchFile):
        """Edits patch file as desired. Will write to log."""
        count = {}
        format_ = self.choiceValues[self.chosen][0]
        showStat = '%02d' in format_
        keep = patchFile.getKeeper()
        codes = getattr(patchFile,'bodyTags','ARGHTCCPBS')
        amulet,ring,gloves,head,tail,robe,chest,pants,shoes,shield = [
            x for x in codes]
        for record in getattr(patchFile,self.key).records:
            if not record.full: continue
            if record.full[0] in '+-=.()[]': continue
            rec_flgs = record.flags
            if rec_flgs.head or rec_flgs.hair: type_ = head
            elif rec_flgs.rightRing or rec_flgs.leftRing: type_ = ring
            elif rec_flgs.amulet: type_ = amulet
            elif rec_flgs.upperBody and rec_flgs.lowerBody: type_ = robe
            elif rec_flgs.upperBody: type_ = chest
            elif rec_flgs.lowerBody: type_ = pants
            elif rec_flgs.hand: type_ = gloves
            elif rec_flgs.foot: type_ = shoes
            elif rec_flgs.tail: type_ = tail
            elif rec_flgs.shield: type_ = shield
            else: continue
            if record.recType == 'ARMO':
                type_ += 'LH'[record.flags.heavyArmor]
            if showStat:
                record.full = format_ % (
                    type_, record.strength / 100) + record.full
            else:
                record.full = format_ % type_ + record.full
            keep(record.fid)
            srcMod = record.fid[0]
            count[srcMod] = count.get(srcMod,0) + 1
        self._patchLog(log, count)

class CBash_NamesTweak_Body(CBash_MultiTweakItem):
    """Names tweaker for armor and clothes."""

    #--Config Phase -----------------------------------------------------------
    def __init__(self, label, tip, key, *choices, **kwargs):
        super(CBash_NamesTweak_Body, self).__init__(label, tip, key, *choices,
                                                    **kwargs)
        self.logMsg = '* ' + _('%(record_type)s Renamed') % {
            'record_type': ('%s ' % self.key)} + ': %d'

    def getTypes(self):
        return [self.key]

    #--Patch Phase ------------------------------------------------------------
    def apply(self,modFile,record,bashTags):
        """Edits patch file as desired. """
        if record.IsNonPlayable: return
        newFull = record.full
        if newFull:
            if record.IsHead or record.IsHair: type_ = self.head
            elif record.IsRightRing or record.IsLeftRing: type_ = self.ring
            elif record.IsAmulet: type_ = self.amulet
            elif record.IsUpperBody and record.IsLowerBody: type_ = self.robe
            elif record.IsUpperBody: type_ = self.chest
            elif record.IsLowerBody: type_ = self.pants
            elif record.IsHand: type_ = self.gloves
            elif record.IsFoot: type_ = self.shoes
            elif record.IsTail: type_ = self.tail
            elif record.IsShield: type_ = self.shield
            else: return
            if record._Type == 'ARMO':
                type_ += 'LH'[record.IsHeavyArmor]
            if self.showStat:
                newFull = self.format % (
                    type_, record.strength / 100) + newFull
            else:
                newFull = self.format % type_ + newFull
            if record.full != newFull:
                override = record.CopyAsOverride(self.patchFile)
                if override:
                    override.full = newFull
                    self.mod_count[modFile.GName] += 1
                    record.UnloadRecord()
                    record._RecordID = override._RecordID

#------------------------------------------------------------------------------
class ANamesTweak_Potions(AMultiTweakItem):
    """Names tweaker for potions."""
    reOldLabel = re.compile('^(-|X) ',re.U)
    reOldEnd = re.compile(' -$',re.U)
    tweak_read_classes = 'ALCH',

    #--Config Phase -----------------------------------------------------------
    def __init__(self):
        super(ANamesTweak_Potions, self).__init__(_("Potions"),
            _('Label potions to sort by type and effect.'),
            'ALCH',
            (_('XD Illness'),  '%s '),
            (_('XD. Illness'), '%s. '),
            (_('XD - Illness'),'%s - '),
            (_('(XD) Illness'),'(%s) '),
            )
        self.logMsg = '* ' + _('%(record_type)s Renamed') % {
            'record_type': ('%s ' % self.key)} + ': %d'

class NamesTweak_Potions(ANamesTweak_Potions, _AMultiTweakItem_Names):

    #--Patch Phase ------------------------------------------------------------
    def scanModFile(self,modFile,progress,patchFile):
        mapper = modFile.getLongMapper()
        patchBlock = patchFile.ALCH
        id_records = patchBlock.id_records
        for record in modFile.ALCH.getActiveRecords():
            if mapper(record.fid) in id_records: continue
            record = record.getTypeCopy(mapper)
            patchBlock.setRecord(record)

    def buildPatch(self,log,progress,patchFile):
        """Edits patch file as desired. Will write to log."""
        count = {}
        format_ = self.choiceValues[self.chosen][0]
        hostileEffects = patchFile.getMgefHostiles()
        keep = patchFile.getKeeper()
        reOldLabel = self.__class__.reOldLabel
        reOldEnd = self.__class__.reOldEnd
        mgef_school = patchFile.getMgefSchool()
        for record in patchFile.ALCH.records:
            if not record.full: continue
            school = 6 #--Default to 6 (U: unknown)
            for index,effect in enumerate(record.effects):
                effectId = effect.name
                if index == 0:
                    if effect.scriptEffect:
                        school = effect.scriptEffect.school
                    else:
                        school = mgef_school.get(effectId,6)
                #--Non-hostile effect?
                if effect.scriptEffect:
                    if not effect.scriptEffect.flags.hostile:
                        isPoison = False
                        break
                elif effectId not in hostileEffects:
                    isPoison = False
                    break
            else:
                isPoison = True
            full = reOldLabel.sub('',record.full) #--Remove existing label
            full = reOldEnd.sub('',full)
            if record.flags.isFood:
                record.full = '.'+full
            else:
                label = ('X' if isPoison else '') + 'ACDIMRU'[school]
                record.full = format_ % label + full
            keep(record.fid)
            srcMod = record.fid[0]
            count[srcMod] = count.get(srcMod,0) + 1
        self._patchLog(log, count)

class CBash_NamesTweak_Potions(ANamesTweak_Potions, CBash_MultiTweakItem):

    #--Patch Phase ------------------------------------------------------------
    def apply(self,modFile,record,bashTags):
        """Edits patch file as desired. """
        newFull = record.full
        if newFull:
            mgef_school = self.patchFile.mgef_school
            hostileEffects = self.patchFile.hostileEffects
            schoolType = 6 #--Default to 6 (U: unknown)
            for index,effect in enumerate(record.effects):
                effectId = effect.name
                if index == 0:
                    if effect.script:
                        schoolType = effect.schoolType
                    else:
                        schoolType = mgef_school.get(effectId,6)
                #--Non-hostile effect?
                if effect.script:
                    if not effect.IsHostile:
                        isPoison = False
                        break
                elif effectId not in hostileEffects:
                    isPoison = False
                    break
            else:
                isPoison = True
            newFull = self.reOldLabel.sub('',newFull) #--Remove existing label
            newFull = self.reOldEnd.sub('',newFull)
            if record.IsFood:
                newFull = '.' + newFull
            else:
                label = ('X' if isPoison else '') + 'ACDIMRU'[schoolType]
                newFull = self.format % label + newFull
            if record.full != newFull:
                override = record.CopyAsOverride(self.patchFile)
                if override:
                    override.full = newFull
                    self.mod_count[modFile.GName] += 1
                    record.UnloadRecord()
                    record._RecordID = override._RecordID

#------------------------------------------------------------------------------
reSpell = re.compile('^(\([ACDIMR]\d\)|\w{3,6}:) ',re.U) # compile once

class ANamesTweak_Scrolls(AMultiTweakItem):
    reOldLabel = reSpell
    #--Config Phase -----------------------------------------------------------
    def __init__(self):
        super(ANamesTweak_Scrolls,self).__init__(_("Notes and Scrolls"),
            _('Mark notes and scrolls to sort separately from books'),
            'scrolls',
            (_('~Fire Ball'),    '~'),
            (_('~D Fire Ball'),  '~%s '),
            (_('~D. Fire Ball'), '~%s. '),
            (_('~D - Fire Ball'),'~%s - '),
            (_('~(D) Fire Ball'),'~(%s) '),
            ('----','----'),
            (_('.Fire Ball'),    '.'),
            (_('.D Fire Ball'),  '.%s '),
            (_('.D. Fire Ball'), '.%s. '),
            (_('.D - Fire Ball'),'.%s - '),
            (_('.(D) Fire Ball'),'.(%s) '),
            )
        self.logMsg = '* '+_('Items Renamed') + ': %d'

    def save_tweak_config(self, configs):
        """Save config to configs dictionary."""
        super(ANamesTweak_Scrolls,self).save_tweak_config(configs)
        rawFormat = self.choiceValues[self.chosen][0]
        self.orderFormat = ('~.','.~')[rawFormat[0] == '~']
        self.magicFormat = rawFormat[1:]

class NamesTweak_Scrolls(ANamesTweak_Scrolls,_AMultiTweakItem_Names):
    tweak_read_classes = 'BOOK','ENCH',

    #--Patch Phase ------------------------------------------------------------
    def scanModFile(self,modFile,progress,patchFile):
        mapper = modFile.getLongMapper()
        #--Scroll Enchantments
        if self.magicFormat:
            patchBlock = patchFile.ENCH
            id_records = patchBlock.id_records
            for record in modFile.ENCH.getActiveRecords():
                if mapper(record.fid) in id_records: continue
                if record.itemType == 0:
                    record = record.getTypeCopy(mapper)
                    patchBlock.setRecord(record)
        #--Books
        patchBlock = patchFile.BOOK
        id_records = patchBlock.id_records
        for record in modFile.BOOK.getActiveRecords():
            if mapper(record.fid) in id_records: continue
            if record.flags.isScroll and not record.flags.isFixed:
                record = record.getTypeCopy(mapper)
                patchBlock.setRecord(record)

    def buildPatch(self,log,progress,patchFile):
        """Edits patch file as desired. Will write to log."""
        count = {}
        reOldLabel = self.__class__.reOldLabel
        orderFormat, magicFormat = self.orderFormat, self.magicFormat
        keep = patchFile.getKeeper()
        id_ench = patchFile.ENCH.id_records
        mgef_school = patchFile.getMgefSchool()
        for record in patchFile.BOOK.records:
            if not record.full or not record.flags.isScroll or \
                    record.flags.isFixed: continue
            #--Magic label
            isEnchanted = bool(record.enchantment)
            if magicFormat and isEnchanted:
                school = 6 #--Default to 6 (U: unknown)
                enchantment = id_ench.get(record.enchantment)
                if enchantment and enchantment.effects:
                    effect = enchantment.effects[0]
                    effectId = effect.name
                    if effect.scriptEffect:
                        school = effect.scriptEffect.school
                    else:
                        school = mgef_school.get(effectId,6)
                record.full = reOldLabel.sub('',record.full) #--Remove
                # existing label
                record.full = magicFormat % 'ACDIMRU'[school] + record.full
            #--Ordering
            record.full = orderFormat[isEnchanted] + record.full
            keep(record.fid)
            srcMod = record.fid[0]
            count[srcMod] = count.get(srcMod,0) + 1
        self._patchLog(log, count)

class CBash_NamesTweak_Scrolls(ANamesTweak_Scrolls,CBash_MultiTweakItem):
    """Names tweaker for scrolls."""
    tweak_read_classes = 'BOOK',

    #--Patch Phase ------------------------------------------------------------
    def apply(self,modFile,record,bashTags):
        """Edits patch file as desired. """
        newFull = record.full
        if newFull and record.IsScroll and not record.IsFixed:
            #--Magic label
            isEnchanted = bool(record.enchantment)
            magicFormat = self.magicFormat
            if magicFormat and isEnchanted:
                schoolType = 6 #--Default to 6 (U: unknown)
                enchantment = record.enchantment
                if enchantment:
                    enchantment = self.patchFile.Current.LookupRecords(
                        enchantment)
                    if enchantment:
                        #Get the winning record
                        enchantment = enchantment[0]
                        Effects = enchantment.effects
                    else:
                        Effects = None
                    if Effects:
                        effect = Effects[0]
                        if effect.script:
                            schoolType = effect.schoolType
                        else:
                            schoolType = self.patchFile.mgef_school.get(
                                effect.name, 6)
                newFull = self.__class__.reOldLabel.sub('',newFull) #--Remove
                # existing label
                newFull = magicFormat % 'ACDIMRU'[schoolType] + newFull
            #--Ordering
            newFull = self.orderFormat[isEnchanted] + newFull
            if record.full != newFull:
                override = record.CopyAsOverride(self.patchFile)
                if override:
                    override.full = newFull
                    self.mod_count[modFile.GName] += 1
                    record.UnloadRecord()
                    record._RecordID = override._RecordID

#------------------------------------------------------------------------------
class ANamesTweak_Spells(AMultiTweakItem):
    """Names tweaker for spells."""
    tweak_read_classes = 'SPEL',

    #--Config Phase -----------------------------------------------------------
    reOldLabel = reSpell
    def __init__(self):
        super(ANamesTweak_Spells, self).__init__(_("Spells"),
            _('Label spells to sort by school and level.'),
            'SPEL',
            (_('Fire Ball'),  'NOTAGS'),
            ('----','----'),
            (_('D Fire Ball'),  '%s '),
            (_('D. Fire Ball'), '%s. '),
            (_('D - Fire Ball'),'%s - '),
            (_('(D) Fire Ball'),'(%s) '),
            ('----','----'),
            (_('D2 Fire Ball'),  '%s%d '),
            (_('D2. Fire Ball'), '%s%d. '),
            (_('D2 - Fire Ball'),'%s%d - '),
            (_('(D2) Fire Ball'),'(%s%d) '),
            )
        self.logMsg = '* '+_('Spells Renamed') + ': %d'

class NamesTweak_Spells(ANamesTweak_Spells,_AMultiTweakItem_Names):

    #--Patch Phase ------------------------------------------------------------
    def scanModFile(self,modFile,progress,patchFile):
        mapper = modFile.getLongMapper()
        patchBlock = patchFile.SPEL
        id_records = patchBlock.id_records
        for record in modFile.SPEL.getActiveRecords():
            if mapper(record.fid) in id_records: continue
            if record.spellType == 0:
                record = record.getTypeCopy(mapper)
                patchBlock.setRecord(record)

    def buildPatch(self,log,progress,patchFile):
        """Edits patch file as desired. Will write to log."""
        count = {}
        format_ = self.choiceValues[self.chosen][0]
        removeTags = '%s' not in format_
        showLevel = '%d' in format_
        keep = patchFile.getKeeper()
        reOldLabel = self.__class__.reOldLabel
        mgef_school = patchFile.getMgefSchool()
        for record in patchFile.SPEL.records:
            if record.spellType != 0 or not record.full: continue
            school = 6 #--Default to 6 (U: unknown)
            if record.effects:
                effect = record.effects[0]
                effectId = effect.name
                if effect.scriptEffect:
                    school = effect.scriptEffect.school
                else:
                    school = mgef_school.get(effectId,6)
            newFull = reOldLabel.sub('',record.full) #--Remove existing label
            if not removeTags:
                if showLevel:
                    newFull = format_ % (
                        'ACDIMRU'[school], record.level) + newFull
                else:
                    newFull = format_ % 'ACDIMRU'[school] + newFull
            if newFull != record.full:
                record.full = newFull
                keep(record.fid)
                srcMod = record.fid[0]
                count[srcMod] = count.get(srcMod,0) + 1
        self._patchLog(log, count)

class CBash_NamesTweak_Spells(ANamesTweak_Spells,CBash_MultiTweakItem):

    #--Config Phase -----------------------------------------------------------
    def save_tweak_config(self, configs):
        """Save config to configs dictionary."""
        super(CBash_NamesTweak_Spells, self).save_tweak_config(configs)
        self.format = self.choiceValues[self.chosen][0]
        self.removeTags = '%s' not in self.format
        self.showLevel = '%d' in self.format

    #--Patch Phase ------------------------------------------------------------
    def apply(self,modFile,record,bashTags):
        """Edits patch file as desired. """
        newFull = record.full
        if newFull and record.IsSpell:
            #--Magic label
            schoolType = 6 #--Default to 6 (U: unknown)
            Effects = record.effects
            if Effects:
                effect = Effects[0]
                if effect.script:
                    schoolType = effect.schoolType
                else:
                    schoolType = self.patchFile.mgef_school.get(effect.name,6)
            newFull = self.__class__.reOldLabel.sub('',newFull) #--Remove
            # existing label
            if not self.removeTags:
                if self.showLevel:
                    newFull = self.format % (
                        'ACDIMRU'[schoolType], record.levelType) + newFull
                else:
                    newFull = self.format % 'ACDIMRU'[schoolType] + newFull

            if record.full != newFull:
                override = record.CopyAsOverride(self.patchFile)
                if override:
                    override.full = newFull
                    self.mod_count[modFile.GName] += 1
                    record.UnloadRecord()
                    record._RecordID = override._RecordID

#------------------------------------------------------------------------------
class ANamesTweak_Weapons(AMultiTweakItem):
    """Names tweaker for weapons and ammo."""
    tweak_read_classes = 'AMMO','WEAP',

    #--Config Phase -----------------------------------------------------------
    def __init__(self):
        super(ANamesTweak_Weapons, self).__init__(_("Weapons"),
            _('Label ammo and weapons to sort by type and damage.'),
            'WEAP',
            (_('B Iron Bow'),  '%s '),
            (_('B. Iron Bow'), '%s. '),
            (_('B - Iron Bow'),'%s - '),
            (_('(B) Iron Bow'),'(%s) '),
            ('----','----'),
            (_('B08 Iron Bow'),  '%s%02d '),
            (_('B08. Iron Bow'), '%s%02d. '),
            (_('B08 - Iron Bow'),'%s%02d - '),
            (_('(B08) Iron Bow'),'(%s%02d) '),
            )
        self.logMsg = '* '+_('Items Renamed') + ': %d'

class NamesTweak_Weapons(ANamesTweak_Weapons,_AMultiTweakItem_Names):

    #--Patch Phase ------------------------------------------------------------
    def scanModFile(self,modFile,progress,patchFile):
        mapper = modFile.getLongMapper()
        for blockType in ('AMMO','WEAP'):
            modBlock = getattr(modFile,blockType)
            patchBlock = getattr(patchFile,blockType)
            id_records = patchBlock.id_records
            for record in modBlock.getActiveRecords():
                if mapper(record.fid) not in id_records:
                    record = record.getTypeCopy(mapper)
                    patchBlock.setRecord(record)

    def buildPatch(self,log,progress,patchFile):
        """Edits patch file as desired. Will write to log."""
        count = {}
        format_ = self.choiceValues[self.chosen][0]
        showStat = '%02d' in format_
        keep = patchFile.getKeeper()
        for record in patchFile.AMMO.records:
            if not record.full: continue
            if record.full[0] in '+-=.()[]': continue
            if showStat:
                record.full = format_ % ('A',record.damage) + record.full
            else:
                record.full = format_ % 'A' + record.full
            keep(record.fid)
            srcMod = record.fid[0]
            count[srcMod] = count.get(srcMod,0) + 1
        for record in patchFile.WEAP.records:
            if not record.full: continue
            if showStat:
                record.full = format_ % (
                    'CDEFGB'[record.weaponType], record.damage) + record.full
            else:
                record.full = format_ % 'CDEFGB'[
                    record.weaponType] + record.full
            keep(record.fid)
            srcMod = record.fid[0]
            count[srcMod] = count.get(srcMod,0) + 1
        self._patchLog(log, count)

class CBash_NamesTweak_Weapons(ANamesTweak_Weapons,CBash_MultiTweakItem):

    #--Config Phase -----------------------------------------------------------
    def save_tweak_config(self, configs):
        """Save config to configs dictionary."""
        super(CBash_NamesTweak_Weapons, self).save_tweak_config(configs)
        self.format = self.choiceValues[self.chosen][0]
        self.showStat = '%02d' in self.format

    #--Patch Phase ------------------------------------------------------------
    def apply(self,modFile,record,bashTags):
        """Edits patch file as desired. """
        newFull = record.full
        if newFull:
            if record._Type == 'AMMO':
                if newFull[0] in '+-=.()[]': return
                type_ = 6
            else:
                type_ = record.weaponType
            if self.showStat:
                newFull = self.format % (
                    'CDEFGBA'[type_], record.damage) + newFull
            else:
                newFull = self.format % 'CDEFGBA'[type_] + newFull
            if record.full != newFull:
                override = record.CopyAsOverride(self.patchFile)
                if override:
                    override.full = newFull
                    self.mod_count[modFile.GName] += 1
                    record.UnloadRecord()
                    record._RecordID = override._RecordID

#------------------------------------------------------------------------------
class ATextReplacer(AMultiTweakItem):
    """Base class for replacing any text via regular expressions."""
    #--Config Phase -----------------------------------------------------------
    def __init__(self, reMatch, reReplace, label, tip, key, choices):
        super(ATextReplacer, self).__init__(label, tip, key, choices)
        self.reMatch = reMatch
        self.reReplace = reReplace
        self.logMsg = '* '+_('Items Renamed') + ': %d'

class TextReplacer(ATextReplacer,_AMultiTweakItem_Names):
    #--Config Phase -----------------------------------------------------------
    def __init__(self, reMatch, reReplace, label, tip, key, choices):
        super(TextReplacer, self).__init__(reMatch, reReplace, label, tip, key,
                                           choices)
        self.activeTypes = ['ALCH','AMMO','APPA','ARMO','BOOK','BSGN',
                            'CLAS','CLOT','CONT','CREA','DOOR',
                            'ENCH','EYES','FACT','FLOR','FURN','GMST',
                            'HAIR','INGR','KEYM','LIGH','LSCR','MGEF',
                            'MISC','NPC_','QUST','RACE','SCPT','SGST',
                            'SKIL','SLGM','SPEL','WEAP']

    #--Patch Phase ------------------------------------------------------------
    def getReadClasses(self):
        """Returns load factory classes needed for reading."""
        return tuple(self.activeTypes)

    def getWriteClasses(self):
        """Returns load factory classes needed for writing."""
        return tuple(self.activeTypes)

    def scanModFile(self,modFile,progress,patchFile):
        mapper = modFile.getLongMapper()
        for blockType in self.activeTypes:
            if blockType not in modFile.tops: continue
            modBlock = getattr(modFile,blockType)
            patchBlock = getattr(patchFile,blockType)
            id_records = patchBlock.id_records
            for record in modBlock.getActiveRecords():
                if mapper(record.fid) not in id_records:
                    record = record.getTypeCopy(mapper)
                    patchBlock.setRecord(record)

    def buildPatch(self,log,progress,patchFile):
        count = {}
        keep = patchFile.getKeeper()
        reMatch = re.compile(self.reMatch)
        reReplace = self.reReplace
        for type_ in self.activeTypes:
            if type_ not in patchFile.tops: continue
            for record in patchFile.tops[type_].records:
                changed = False
                if hasattr(record, 'full'):
                    changed = reMatch.search(record.full or '')
                if not changed:
                    if hasattr(record, 'effects'):
                        Effects = record.effects
                        for effect in Effects:
                            try:
                                changed = reMatch.search(
                                    effect.scriptEffect.full or '')
                            except AttributeError:
                                continue
                            if changed: break
                if not changed:
                    if hasattr(record, 'text'):
                        changed = reMatch.search(record.text or '')
                if not changed:
                    if hasattr(record, 'description'):
                        changed = reMatch.search(record.description or '')
                if not changed:
                    if type_ == 'GMST' and record.eid[0] == 's':
                        changed = reMatch.search(record.value or '')
                if not changed:
                    if hasattr(record, 'stages'):
                        Stages = record.stages
                        for stage in Stages:
                            for entry in stage.entries:
                                changed = reMatch.search(entry.text or '')
                                if changed: break
                if not changed:
                    if type_ == 'SKIL':
                        changed = reMatch.search(record.apprentice or '')
                        if not changed:
                            changed = reMatch.search(record.journeyman or '')
                        if not changed:
                            changed = reMatch.search(record.expert or '')
                        if not changed:
                            changed = reMatch.search(record.master or '')
                if changed:
                    if hasattr(record, 'full'):
                        newString = record.full
                        if record:
                            record.full = reMatch.sub(reReplace, newString)
                    if hasattr(record, 'effects'):
                        Effects = record.effects
                        for effect in Effects:
                            try:
                                newString = effect.scriptEffect.full
                            except AttributeError:
                                continue
                            if newString:
                                effect.scriptEffect.full = reMatch.sub(
                                    reReplace, newString)
                    if hasattr(record, 'text'):
                        newString = record.text
                        if newString:
                            record.text = reMatch.sub(reReplace, newString)
                    if hasattr(record, 'description'):
                        newString = record.description
                        if newString:
                            record.description = reMatch.sub(reReplace,
                                                             newString)
                    if type_ == 'GMST' and record.eid[0] == 's':
                        newString = record.value
                        if newString:
                            record.value = reMatch.sub(reReplace, newString)
                    if hasattr(record, 'stages'):
                        Stages = record.stages
                        for stage in Stages:
                            for entry in stage.entries:
                                newString = entry.text
                                if newString:
                                    entry.text = reMatch.sub(reReplace,
                                                             newString)
                    if type_ == 'SKIL':
                        newString = record.apprentice
                        if newString:
                            record.apprentice = reMatch.sub(reReplace,
                                                            newString)
                        newString = record.journeyman
                        if newString:
                            record.journeyman = reMatch.sub(reReplace,
                                                            newString)
                        newString = record.expert
                        if newString:
                            record.expert = reMatch.sub(reReplace, newString)
                        newString = record.master
                        if newString:
                            record.master = reMatch.sub(reReplace, newString)
                    keep(record.fid)
                    srcMod = record.fid[0]
                    count[srcMod] = count.get(srcMod,0) + 1
        self._patchLog(log, count)

class CBash_TextReplacer(ATextReplacer,CBash_MultiTweakItem):
    #--Config Phase -----------------------------------------------------------
    def getTypes(self):
        ##: note it differs only in 'CELLS' from TextReplacer.activeTypes
        return ['ALCH','AMMO','APPA','ARMO','BOOK','BSGN',
                'CELLS','CLAS','CLOT','CONT','CREA','DOOR',
                'ENCH','EYES','FACT','FLOR','FURN','GMST',
                'HAIR','INGR','KEYM','LIGH','LSCR','MGEF',
                'MISC','NPC_','QUST','RACE','SCPT','SGST',
                'SKIL','SLGM','SPEL','WEAP']

    def save_tweak_config(self, configs):
        """Save config to configs dictionary."""
        super(CBash_TextReplacer, self).save_tweak_config(configs)
        self.format = self.choiceValues[self.chosen][0]
        self.showStat = '%02d' in self.format

    #--Patch Phase ------------------------------------------------------------
    def apply(self,modFile,record,bashTags):
        """Edits patch file as desired. """
        reMatch = re.compile(self.reMatch)
        changed = False
        if hasattr(record, 'full'):
            changed = reMatch.search(record.full or '')
        if not changed:
            if hasattr(record, 'effects'):
                Effects = record.effects
                for effect in Effects:
                    changed = reMatch.search(effect.full or '')
                    if changed: break
        if not changed:
            if hasattr(record, 'text'):
                changed = reMatch.search(record.text or '')
        if not changed:
            if hasattr(record, 'description'):
                changed = reMatch.search(record.description or '')
        if not changed:
            if record._Type == 'GMST' and record.eid[0] == 's':
                changed = reMatch.search(record.value or '')
        if not changed:
            if hasattr(record, 'stages'):
                Stages = record.stages
                for stage in Stages:
                    for entry in stage.entries:
                        changed = reMatch.search(entry.text or '')
                        if changed: break
##### CRUFT: is this code needed ?
##                        compiled = entry.compiled_p
##                        if compiled:
##                            changed = reMatch.search(struct.pack('B' * len(compiled), *compiled) or '')
##                            if changed: break
##                        changed = reMatch.search(entry.scriptText or '')
##                        if changed: break
##        if not changed:
##            if hasattr(record, 'scriptText'):
##                changed = reMatch.search(record.scriptText or '')
##                if not changed:
##                    compiled = record.compiled_p
##                    changed = reMatch.search(struct.pack('B' * len(compiled), *compiled) or '')
        if not changed:
            if record._Type == 'SKIL':
                changed = reMatch.search(record.apprentice or '')
                if not changed:
                    changed = reMatch.search(record.journeyman or '')
                if not changed:
                    changed = reMatch.search(record.expert or '')
                if not changed:
                    changed = reMatch.search(record.master or '')

        # Could support DIAL/INFO as well, but skipping since they're often
        # voiced as well
        if changed:
            override = record.CopyAsOverride(self.patchFile)
            if override:
                if hasattr(override, 'full'):
                    newString = override.full
                    if newString:
                        override.full = reMatch.sub(self.reReplace, newString)
                if hasattr(override, 'effects'):
                    Effects = override.effects
                    for effect in Effects:
                        newString = effect.full
                        if newString:
                            effect.full = reMatch.sub(self.reReplace, newString)
                if hasattr(override, 'text'):
                    newString = override.text
                    if newString:
                        override.text = reMatch.sub(self.reReplace, newString)
                if hasattr(override, 'description'):
                    newString = override.description
                    if newString:
                        override.description = reMatch.sub(self.reReplace,
                                                           newString)
                if override._Type == 'GMST' and override.eid[0] == 's':
                    newString = override.value
                    if newString:
                        override.value = reMatch.sub(self.reReplace, newString)
                if hasattr(override, 'stages'):
                    Stages = override.stages
                    for stage in Stages:
                        for entry in stage.entries:
                            newString = entry.text
                            if newString:
                                entry.text = reMatch.sub(self.reReplace, newString)
##### CRUFT: is this code needed ?
##                            newString = entry.compiled_p
##                            if newString:
##                                nSize = len(newString)
##                                newString = reMatch.sub(self.reReplace, struct.pack('B' * nSize, *newString))
##                                nSize = len(newString)
##                                entry.compiled_p = struct.unpack('B' * nSize, newString)
##                                entry.compiledSize = nSize
##                            newString = entry.scriptText
##                            if newString:
##                                entry.scriptText = reMatch.sub(self.reReplace, newString)
##
##                if hasattr(override, 'scriptText'):
##                    newString = override.compiled_p
##                    if newString:
##                        nSize = len(newString)
##                        newString = reMatch.sub(self.reReplace, struct.pack('B' * nSize, *newString))
##                        nSize = len(newString)
##                        override.compiled_p = struct.unpack('B' * nSize, newString)
##                        override.compiledSize = nSize
##                    newString = override.scriptText
##                    if newString:
##                        override.scriptText = reMatch.sub(self.reReplace, newString)
                if override._Type == 'SKIL':
                    newString = override.apprentice
                    if newString:
                        override.apprentice = reMatch.sub(self.reReplace,
                                                          newString)
                    newString = override.journeyman
                    if newString:
                        override.journeyman = reMatch.sub(self.reReplace,
                                                          newString)
                    newString = override.expert
                    if newString:
                        override.expert = reMatch.sub(self.reReplace,
                                                      newString)
                    newString = override.master
                    if newString:
                        override.master = reMatch.sub(self.reReplace,
                                                      newString)
                self.mod_count[modFile.GName] += 1
                record.UnloadRecord()
                record._RecordID = override._RecordID

#------------------------------------------------------------------------------
class _ANamesTweaker(AMultiTweaker):
    """Tweaks record full names in various ways."""
    scanOrder = 32
    editOrder = 32
    name = _('Tweak Names')
    text = _("Tweak object names in various ways such as lore friendliness or"
             " show type/quality.")
    _namesTweaksBody = ((_("Armor"),
                         _("Rename armor to sort by type."),
                         'ARMO',
                         (_('BL Leather Boots'), '%s '),
                         (_('BL. Leather Boots'), '%s. '),
                         (_('BL - Leather Boots'), '%s - '),
                         (_('(BL) Leather Boots'), '(%s) '),
                         ('----', '----'),
                         (_('BL02 Leather Boots'), '%s%02d '),
                         (_('BL02. Leather Boots'), '%s%02d. '),
                         (_('BL02 - Leather Boots'), '%s%02d - '),
                         (_('(BL02) Leather Boots'), '(%s%02d) '),),
                        (_("Clothes"),
                         _("Rename clothes to sort by type."),
                         'CLOT',
                         (_('P Grey Trousers'),  '%s '),
                         (_('P. Grey Trousers'), '%s. '),
                         (_('P - Grey Trousers'),'%s - '),
                         (_('(P) Grey Trousers'),'(%s) '),),)
    _txtReplacer = (('' r'\b(d|D)(?:warven|warf)\b', '' r'\1wemer',
                     _("Lore Friendly Text: Dwarven -> Dwemer"),
                     _('Replace any occurrences of the words "Dwarf" or'
                       ' "Dwarven" with "Dwemer" to better follow lore.'),
                     'Dwemer',
                     ('Lore Friendly Text: Dwarven -> Dwemer', 'Dwemer'),),
                    ('' r'\b(d|D)(?:warfs)\b', '' r'\1warves',
                     _("Proper English Text: Dwarfs -> Dwarves"),
                     _('Replace any occurrences of the words "Dwarfs" with '
                       '"Dwarves" to better follow proper English.'),
                     'Dwarfs',
                     ('Proper English Text: Dwarfs -> Dwarves', 'Dwarves'),),
                    ('' r'\b(s|S)(?:taffs)\b', '' r'\1taves',
                     _("Proper English Text: Staffs -> Staves"),
                     _('Replace any occurrences of the words "Staffs" with'
                       ' "Staves" to better follow proper English.'),
                     'Staffs',
                    ('Proper English Text: Staffs -> Staves', 'Staves'),),)

class NamesTweaker(_ANamesTweaker,MultiTweaker):
    tweaks = sorted(
        [NamesTweak_Body(*x) for x in _ANamesTweaker._namesTweaksBody] + [
            TextReplacer(*x) for x in _ANamesTweaker._txtReplacer] + [
            NamesTweak_Potions(), NamesTweak_Scrolls(), NamesTweak_Spells(),
            NamesTweak_Weapons()], key=lambda a: a.label.lower())
    tweaks.insert(0, NamesTweak_BodyTags())

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

class CBash_NamesTweaker(_ANamesTweaker,CBash_MultiTweaker):
    tweaks = sorted(
        [CBash_NamesTweak_Body(*x) for x in _ANamesTweaker._namesTweaksBody] +
        [CBash_TextReplacer(*x) for x in _ANamesTweaker._txtReplacer] + [
            CBash_NamesTweak_Potions(), CBash_NamesTweak_Scrolls(),
            CBash_NamesTweak_Spells(), CBash_NamesTweak_Weapons()],
        key=lambda a: a.label.lower())
    tweaks.insert(0,CBash_NamesTweak_BodyTags())

    #--Config Phase -----------------------------------------------------------
    def initPatchFile(self, patchFile):
        self.patchFile = patchFile
        for tweak in self.tweaks[1:]:
            tweak.patchFile = patchFile
        bodyTagPatcher = self.tweaks[0]
        patchFile.bodyTags = \
            bodyTagPatcher.choiceValues[bodyTagPatcher.chosen][0]
        patchFile.indexMGEFs = True

    def initData(self,group_patchers,progress):
        if not self.isActive: return
        for tweak in self.enabledTweaks:
            for type_ in tweak.getTypes():
                group_patchers.setdefault(type_,[]).append(tweak)
            tweak.format = tweak.choiceValues[tweak.chosen][0]
            if isinstance(tweak, CBash_NamesTweak_Body):
                tweak.showStat = '%02d' in tweak.format
                tweak.codes = getattr(self.patchFile,'bodyTags','ARGHTCCPBS')
                tweak.amulet, tweak.ring, tweak.gloves, tweak.head, \
                tweak.tail, tweak.robe, tweak.chest, tweak.pants, \
                tweak.shoes, tweak.shield = [
                    x for x in tweak.codes]
