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
"""GameInfo override for TES IV: Oblivion."""

from .. import GameInfo
from ... import brec
from ...brec import MreGlob

class OblivionGameInfo(GameInfo):
    displayName = 'Oblivion'
    fsName = 'Oblivion'
    altName = 'Wrye Bash'
    defaultIniFile = 'Oblivion_default.ini'
    launch_exe = 'Oblivion.exe'
    game_detect_file = ['Oblivion.exe']
    version_detect_file  = ['Oblivion.exe']
    masterFiles = ['Oblivion.esm', 'Nehrim.esm']
    iniFiles = ['Oblivion.ini']
    pklfile = 'bash\\db\\Oblivion_ids.pkl'
    masterlist_dir = 'Oblivion'
    regInstallKeys = ('Bethesda Softworks\\Oblivion', 'Installed Path')
    nexusUrl = 'https://www.nexusmods.com/oblivion/'
    nexusName = 'TES Nexus'
    nexusKey = 'bash.installers.openTesNexus.continue'

    patchURL = 'http://www.elderscrolls.com/downloads/updates_patches.htm'
    patchTip = 'http://www.elderscrolls.com/'

    allow_reset_bsa_timestamps = True
    supports_mod_inis = False

    using_txt_file = False
    has_standalone_pluggy = True

    class cs(GameInfo.cs):
        cs_abbrev = 'TESCS'
        long_name = 'Construction Set'
        exe = 'TESConstructionSet.exe'
        se_args = '-editor'
        image_name = 'tescs%s.png'

    class se(GameInfo.se):
        se_abbrev = 'OBSE'
        long_name = 'Oblivion Script Extender'
        exe = 'obse_loader.exe'
        steam_exe = 'obse_1_2_416.dll'
        plugin_dir = 'OBSE'
        cosave_ext = '.obse'
        url = 'http://obse.silverlock.org/'
        url_tip = 'http://obse.silverlock.org/'

    class ge(GameInfo.ge):
        ge_abbrev = 'OBGE'
        long_name = 'Oblivion Graphics Extender'
        exe = [('obse', 'plugins', 'obge.dll'),
               ('obse', 'plugins', 'obgev2.dll'),
               ('obse', 'plugins', 'oblivionreloaded.dll'),
               ]
        url = 'https://www.nexusmods.com/oblivion/mods/30054'
        url_tip = 'https://www.nexusmods.com/oblivion'

    class ess(GameInfo.ess):
        canEditMore = True

    # BAIN:
    dataDirs = GameInfo.dataDirs | {
        'distantlod',
        'facegen',
        'fonts',
        'menus',
        'shaders',
        'trees',
    }
    dataDirsPlus = {
        '_tejon',
        'ini',
        'obse',
        'pluggy',
        'scripts',
        'streamline',
    }
    SkipBAINRefresh = {
        'tes4edit backups',
        'tes4edit cache',
        'bgsee',
        'conscribe logs',
    }
    wryeBashDataFiles = GameInfo.wryeBashDataFiles | {
        'ArchiveInvalidationInvalidated!.bsa'}
    ignoreDataFiles = {
        'OBSE\\Plugins\\Construction Set Extender.dll',
        'OBSE\\Plugins\\Construction Set Extender.ini'
    }
    ignoreDataFilePrefixes = {
        'Meshes\\Characters\\_Male\\specialanims\\0FemaleVariableWalk_'
    }
    ignoreDataDirs = {
        'OBSE\\Plugins\\ComponentDLLs\\CSE',
        'LSData'
    }

    class esp(GameInfo.esp):
        canBash = True
        canCBash = True
        canEditHeader = True
        validHeaderVersions = (0.8,1.0)
        stringsFiles = []

    allTags = {'Body-F', 'Body-M', 'Body-Size-M', 'Body-Size-F',
               'C.Climate', 'C.Light', 'C.Music', 'C.Name',
               'C.Owner', 'C.RecordFlags', 'C.Regions', 'C.Water',
               'Deactivate', 'Delev', 'Eyes', 'Factions', 'Relations',
               'Filter', 'Graphics', 'Hair', 'IIM', 'Invent', 'Names',
               'NoMerge', 'NpcFaces', 'R.Relations', 'Relev', 'Scripts',
               'ScriptContents', 'Sound', 'SpellStats', 'Stats',
               'Voice-F', 'Voice-M', 'R.Teeth', 'R.Mouth', 'R.Ears',
               'R.Head', 'R.Attributes-F', 'R.Attributes-M', 'R.Skills',
               'R.Description', 'R.AddSpells', 'R.ChangeSpells', 'Roads',
               'Actors.Anims', 'Actors.AIData', 'Actors.DeathItem',
               'Actors.AIPackages', 'Actors.AIPackagesForceAdd',
               'Actors.Stats', 'Actors.ACBS', 'NPC.Class',
               'Actors.CombatStyle', 'Creatures.Blood', 'Actors.Spells',
               'Actors.SpellsForceAdd', 'NPC.Race', 'Actors.Skeleton',
               'NpcFacesForceFullImport', 'MustBeActiveIfImported',
               'Npc.HairOnly', 'Npc.EyesOnly'}  # , 'ForceMerge'

    patchers = (
        'AliasesPatcher', 'AssortedTweaker', 'PatchMerger', 'AlchemicalCatalogs',
        'KFFZPatcher', 'ActorImporter', 'DeathItemPatcher', 'NPCAIPackagePatcher',
        'CoblExhaustion', 'UpdateReferences', 'CellImporter', 'ClothesTweaker',
        'GmstTweaker', 'GraphicsPatcher', 'ImportFactions', 'ImportInventory',
        'SpellsPatcher', 'TweakActors', 'ImportRelations', 'ImportScripts',
        'ImportActorsSpells', 'ListsMerger', 'MFactMarker', 'NamesPatcher',
        'NamesTweaker', 'NpcFacePatcher', 'RacePatcher', 'RoadImporter',
        'SoundPatcher', 'StatsPatcher', 'SEWorldEnforcer', 'ContentsChecker',
        )

    CBash_patchers = (
        'CBash_AliasesPatcher', 'CBash_AssortedTweaker', 'CBash_PatchMerger',
        'CBash_AlchemicalCatalogs', 'CBash_KFFZPatcher', 'CBash_ActorImporter',
        'CBash_DeathItemPatcher', 'CBash_NPCAIPackagePatcher',
        'CBash_CoblExhaustion', 'CBash_UpdateReferences', 'CBash_CellImporter',
        'CBash_ClothesTweaker', 'CBash_GmstTweaker', 'CBash_GraphicsPatcher',
        'CBash_ImportFactions', 'CBash_ImportInventory', 'CBash_SpellsPatcher',
        'CBash_TweakActors', 'CBash_ImportRelations', 'CBash_ImportScripts',
        'CBash_ImportActorsSpells', 'CBash_ListsMerger', 'CBash_MFactMarker',
        'CBash_NamesPatcher', 'CBash_NamesTweaker', 'CBash_NpcFacePatcher',
        'CBash_RacePatcher', 'CBash_RoadImporter', 'CBash_SoundPatcher',
        'CBash_StatsPatcher', 'CBash_SEWorldEnforcer', 'CBash_ContentsChecker',
        )

    weaponTypes = (
        _('Blade (1 Handed)'),
        _('Blade (2 Handed)'),
        _('Blunt (1 Handed)'),
        _('Blunt (2 Handed)'),
        _('Staff'),
        _('Bow'),
        )

    raceNames = {
        0x23fe9 : _('Argonian'),
        0x224fc : _('Breton'),
        0x191c1 : _('Dark Elf'),
        0x19204 : _('High Elf'),
        0x00907 : _('Imperial'),
        0x22c37 : _('Khajiit'),
        0x224fd : _('Nord'),
        0x191c0 : _('Orc'),
        0x00d43 : _('Redguard'),
        0x00019 : _('Vampire'),
        0x223c8 : _('Wood Elf'),
        }
    raceShortNames = {
        0x23fe9 : 'Arg',
        0x224fc : 'Bre',
        0x191c1 : 'Dun',
        0x19204 : 'Alt',
        0x00907 : 'Imp',
        0x22c37 : 'Kha',
        0x224fd : 'Nor',
        0x191c0 : 'Orc',
        0x00d43 : 'Red',
        0x223c8 : 'Bos',
        }
    raceHairMale = {
        0x23fe9 : 0x64f32, #--Arg
        0x224fc : 0x90475, #--Bre
        0x191c1 : 0x64214, #--Dun
        0x19204 : 0x7b792, #--Alt
        0x00907 : 0x90475, #--Imp
        0x22c37 : 0x653d4, #--Kha
        0x224fd : 0x1da82, #--Nor
        0x191c0 : 0x66a27, #--Orc
        0x00d43 : 0x64215, #--Red
        0x223c8 : 0x690bc, #--Bos
        }
    raceHairFemale = {
        0x23fe9 : 0x64f33, #--Arg
        0x224fc : 0x1da83, #--Bre
        0x191c1 : 0x1da83, #--Dun
        0x19204 : 0x690c2, #--Alt
        0x00907 : 0x1da83, #--Imp
        0x22c37 : 0x653d0, #--Kha
        0x224fd : 0x1da83, #--Nor
        0x191c0 : 0x64218, #--Orc
        0x00d43 : 0x64210, #--Red
        0x223c8 : 0x69473, #--Bos
        }

    @classmethod
    def init(cls):
        cls._dynamic_import_modules(__name__)
        from .records import MreActi, MreAlch, MreAmmo, MreAnio, MreAppa, \
            MreArmo, MreBook, MreBsgn, MreClas, MreClot, MreCont, MreCrea, \
            MreDoor, MreEfsh, MreEnch, MreEyes, MreFact, MreFlor, MreFurn, \
            MreGras, MreHair, MreIngr, MreKeym, MreLigh, MreLscr, MreLvlc, \
            MreLvli, MreLvsp, MreMgef, MreMisc, MreNpc, MrePack, MreQust, \
            MreRace, MreScpt, MreSgst, MreSlgm, MreSoun, MreSpel, MreStat, \
            MreTree, MreWatr, MreWeap, MreWthr, MreClmt, MreCsty, MreIdle, \
            MreLtex, MreRegn, MreSbsp, MreSkil, MreAchr, MreAcre, MreCell, \
            MreGmst, MreRefr, MreRoad, MreHeader, MreWrld, MreDial, MreInfo
        cls.mergeClasses = (
            MreActi, MreAlch, MreAmmo, MreAnio, MreAppa, MreArmo, MreBook,
            MreBsgn, MreClas, MreClot, MreCont, MreCrea, MreDoor, MreEfsh,
            MreEnch, MreEyes, MreFact, MreFlor, MreFurn, MreGlob, MreGras,
            MreHair, MreIngr, MreKeym, MreLigh, MreLscr, MreLvlc, MreLvli,
            MreLvsp, MreMgef, MreMisc, MreNpc, MrePack, MreQust, MreRace,
            MreScpt, MreSgst, MreSlgm, MreSoun, MreSpel, MreStat, MreTree,
            MreWatr, MreWeap, MreWthr, MreClmt, MreCsty, MreIdle, MreLtex,
            MreRegn, MreSbsp, MreSkil,
        )
        cls.readClasses = (MreMgef, MreScpt,)
        cls.writeClasses = (MreMgef,)
        # Setting RecordHeader class variables - Oblivion is special
        __rec_type = brec.RecordHeader
        __rec_type.rec_header_size = 20
        __rec_type.rec_pack_format = ['=4s', 'I', 'I', 'I', 'I']
        __rec_type.rec_pack_format_str = ''.join(__rec_type.rec_pack_format)
        __rec_type.pack_formats = {0: '=4sI4s2I'}
        __rec_type.pack_formats.update(
            {x: '=4s4I' for x in {1, 6, 7, 8, 9, 10}})
        __rec_type.pack_formats.update({x: '=4sIi2I' for x in {2, 3}})
        __rec_type.pack_formats.update({x: '=4sIhh2I' for x in {4, 5}})
        # Similar to other games
        __rec_type.topTypes = cls.str_to_bytes([
            'GMST', 'GLOB', 'CLAS', 'FACT', 'HAIR', 'EYES', 'RACE', 'SOUN',
            'SKIL', 'MGEF', 'SCPT', 'LTEX', 'ENCH', 'SPEL', 'BSGN', 'ACTI',
            'APPA', 'ARMO', 'BOOK', 'CLOT', 'CONT', 'DOOR', 'INGR', 'LIGH',
            'MISC', 'STAT', 'GRAS', 'TREE', 'FLOR', 'FURN', 'WEAP', 'AMMO',
            'NPC_', 'CREA', 'LVLC', 'SLGM', 'KEYM', 'ALCH', 'SBSP', 'SGST',
            'LVLI', 'WTHR', 'CLMT', 'REGN', 'CELL', 'WRLD', 'DIAL', 'QUST',
            'IDLE', 'PACK', 'CSTY', 'LSCR', 'LVSP', 'ANIO', 'WATR', 'EFSH'])
        __rec_type.recordTypes = set(
            __rec_type.topTypes + [b'GRUP', b'TES4', b'ROAD', b'REFR',
                                   b'ACHR', b'ACRE', b'PGRD', b'LAND',
                                   b'INFO'])
        brec.MreRecord.type_class = dict((x.classType,x) for x in (
            MreAchr, MreAcre, MreActi, MreAlch, MreAmmo, MreAnio, MreAppa,
            MreArmo, MreBook, MreBsgn, MreCell, MreClas, MreClot, MreCont,
            MreCrea, MreDoor, MreEfsh, MreEnch, MreEyes, MreFact, MreFlor,
            MreFurn, MreGlob, MreGmst, MreGras, MreHair, MreIngr, MreKeym,
            MreLigh, MreLscr, MreLvlc, MreLvli, MreLvsp, MreMgef, MreMisc,
            MreNpc, MrePack, MreQust, MreRace, MreRefr, MreRoad, MreScpt,
            MreSgst, MreSkil, MreSlgm, MreSoun, MreSpel, MreStat, MreTree,
            MreHeader, MreWatr, MreWeap, MreWrld, MreWthr, MreClmt, MreCsty,
            MreIdle, MreLtex, MreRegn, MreSbsp, MreDial, MreInfo,))
        brec.MreRecord.simpleTypes = (
            set(brec.MreRecord.type_class) - {b'TES4', b'ACHR', b'ACRE',
                                              b'REFR', b'CELL', b'PGRD',
                                              b'ROAD', b'LAND', b'WRLD',
                                              b'INFO', b'DIAL'})

GAME_TYPE = OblivionGameInfo
