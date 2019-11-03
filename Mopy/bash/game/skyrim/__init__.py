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
"""GameInfo override for TES V: Skyrim."""

from .. import GameInfo
from ... import brec
from ...brec import MreGlob

class SkyrimGameInfo(GameInfo):
    displayName = 'Skyrim'
    fsName = 'Skyrim'
    altName = 'Wrye Smash'
    defaultIniFile = 'Skyrim_default.ini'
    launch_exe = 'TESV.exe'
    # Set to this because TESV.exe also exists for Enderal
    game_detect_file = ['SkyrimLauncher.exe']
    version_detect_file = ['TESV.exe']
    masterFiles = ['Skyrim.esm', 'Update.esm']
    iniFiles = ['Skyrim.ini', 'SkyrimPrefs.ini']
    pklfile = 'bash\\db\\Skyrim_ids.pkl'
    masterlist_dir = 'Skyrim'
    regInstallKeys = ('Bethesda Softworks\\Skyrim', 'Installed Path')
    nexusUrl = 'https://www.nexusmods.com/skyrim/'
    nexusName = 'Skyrim Nexus'
    nexusKey = 'bash.installers.openSkyrimNexus.continue'

    has_bsl = True
    vanilla_string_bsas = {
        'skyrim.esm': ['Skyrim - Interface.bsa'],
        'update.esm': ['Skyrim - Interface.bsa'],
        'dawnguard.esm': ['Dawnguard.bsa'],
        'hearthfires.esm': ['Hearthfires.bsa'],
        'dragonborn.esm': ['Dragonborn.bsa'],
    }
    resource_archives_keys = ('sResourceArchiveList', 'sResourceArchiveList2')
    script_extensions = {'.psc'}

    class cs(GameInfo.cs):
        cs_abbrev = 'CK'
        long_name = 'Creation Kit'
        exe = 'CreationKit.exe'
        se_args = None  # u'-editor'
        image_name = 'creationkit%s.png'

    class se(GameInfo.se):
        se_abbrev = 'SKSE'
        long_name = 'Skyrim Script Extender'
        exe = 'skse_loader.exe'
        steam_exe = 'skse_loader.exe'
        plugin_dir = 'SKSE'
        cosave_ext = '.skse'
        url = 'http://skse.silverlock.org/'
        url_tip = 'http://skse.silverlock.org/'

    class sd(GameInfo.sd):
        sd_abbrev = 'SD'
        long_name = 'Script Dragon'
        install_dir = 'asi'

    class sp(GameInfo.sp):
        sp_abbrev = 'SP'
        long_name = 'SkyProc'
        install_dir = 'SkyProc Patchers'

    class ini(GameInfo.ini):
        allowNewLines = True
        bsaRedirection = ('', '')

    class pnd(GameInfo.pnd):
        facegen_dir_1 = ['meshes', 'actors', 'character', 'facegendata',
                         'facegeom']
        facegen_dir_2 = ['textures', 'actors', 'character', 'facegendata',
                         'facetint']

    # BAIN:
    dataDirs = GameInfo.dataDirs | {
        'dialogueviews',
        'grass',
        'interface',
        'lodsettings',
        'scripts',
        'seq',
        'shadersfx',
        'strings',
    }
    dataDirsPlus = {
        'asi',
        'calientetools', # bodyslide
        'dyndolod',
        'ini',
        'skse',
        'skyproc patchers',
        'tools', # Bodyslide, FNIS
    }
    dontSkip = (
           # These are all in the Interface folder. Apart from the skyui_ files,
           # they are all present in vanilla.
           'skyui_cfg.txt',
           'skyui_translate.txt',
           'credits.txt',
           'credits_french.txt',
           'fontconfig.txt',
           'controlmap.txt',
           'gamepad.txt',
           'mouse.txt',
           'keyboard_english.txt',
           'keyboard_french.txt',
           'keyboard_german.txt',
           'keyboard_spanish.txt',
           'keyboard_italian.txt',
    )
    dontSkipDirs = {
        # This rule is to allow mods with string translation enabled.
        'interface\\translations':['.txt']
    }
    SkipBAINRefresh = {'tes5edit backups', 'tes5edit cache'}
    ignoreDataDirs = {'LSData'}

    class esp(GameInfo.esp):
        canBash = True
        canEditHeader = True
        validHeaderVersions = (0.94, 1.70,)

    allTags = {'C.Acoustic', 'C.Climate', 'C.Encounter', 'C.ForceHideLand',
               'C.ImageSpace', 'C.Light', 'C.Location', 'C.LockList',
               'C.Music', 'C.Name', 'C.Owner', 'C.RecordFlags',
               'C.Regions', 'C.SkyLighting', 'C.Water', 'Deactivate',
               'Delev', 'Filter', 'Graphics', 'Invent', 'Names',
               'NoMerge', 'Relev', 'Sound', 'Stats'}

    patchers = (
        'CellImporter', 'GmstTweaker', 'GraphicsPatcher',
        'ImportInventory', 'ListsMerger', 'PatchMerger', 'SoundPatcher',
        'StatsPatcher', 'NamesPatcher',
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
        0x13740 : _('Argonian'),
        0x13741 : _('Breton'),
        0x13742 : _('Dark Elf'),
        0x13743 : _('High Elf'),
        0x13744 : _('Imperial'),
        0x13745 : _('Khajiit'),
        0x13746 : _('Nord'),
        0x13747 : _('Orc'),
        0x13748 : _('Redguard'),
        0x13749 : _('Wood Elf'),
        }
    raceShortNames = {
        0x13740 : 'Arg',
        0x13741 : 'Bre',
        0x13742 : 'Dun',
        0x13743 : 'Alt',
        0x13744 : 'Imp',
        0x13745 : 'Kha',
        0x13746 : 'Nor',
        0x13747 : 'Orc',
        0x13748 : 'Red',
        0x13749 : 'Bos',
        }
    raceHairMale = {
        0x13740 : 0x64f32, #--Arg
        0x13741 : 0x90475, #--Bre
        0x13742 : 0x64214, #--Dun
        0x13743 : 0x7b792, #--Alt
        0x13744 : 0x90475, #--Imp
        0x13745 : 0x653d4, #--Kha
        0x13746 : 0x1da82, #--Nor
        0x13747 : 0x66a27, #--Orc
        0x13748 : 0x64215, #--Red
        0x13749 : 0x690bc, #--Bos
        }
    raceHairFemale = {
        0x13740 : 0x64f33, #--Arg
        0x13741 : 0x1da83, #--Bre
        0x13742 : 0x1da83, #--Dun
        0x13743 : 0x690c2, #--Alt
        0x13744 : 0x1da83, #--Imp
        0x13745 : 0x653d0, #--Kha
        0x13746 : 0x1da83, #--Nor
        0x13747 : 0x64218, #--Orc
        0x13748 : 0x64210, #--Red
        0x13749 : 0x69473, #--Bos
        }

    @classmethod
    def init(cls):
        cls._dynamic_import_modules(__name__)
        from .records import MreCell, MreWrld, MreFact, MreAchr, MreDial, \
            MreInfo, MreCams, MreWthr, MreDual, MreMato, MreVtyp, MreMatt, \
            MreLvsp, MreEnch, MreProj, MreDlbr, MreRfct, MreMisc, MreActi, \
            MreEqup, MreCpth, MreDoor, MreAnio, MreHazd, MreIdlm, MreEczn, \
            MreIdle, MreLtex, MreQust, MreMstt, MreNpc, MreFlst, MreIpds, \
            MreGmst, MreRevb, MreClmt, MreDebr, MreSmbn, MreLvli, MreSpel, \
            MreKywd, MreLvln, MreAact, MreSlgm, MreRegn, MreFurn, MreGras, \
            MreAstp, MreWoop, MreMovt, MreCobj, MreShou, MreSmen, MreColl, \
            MreArto, MreAddn, MreSopm, MreCsty, MreAppa, MreArma, MreArmo, \
            MreKeym, MreTxst, MreHdpt, MreHeader, MreAlch, MreBook, MreSpgd, \
            MreSndr, MreImgs, MreScrl, MreMust, MreFstp, MreFsts, MreMgef, \
            MreLgtm, MreMusc, MreClas, MreLctn, MreTact, MreBptd, MreDobj, \
            MreLscr, MreDlvw, MreTree, MreWatr, MreFlor, MreEyes, MreWeap, \
            MreIngr, MreClfm, MreMesg, MreLigh, MreExpl, MreLcrt, MreStat, \
            MreAmmo, MreSmqn, MreImad, MreSoun, MreAvif, MreCont, MreIpct, \
            MreAspc, MreRela, MreEfsh, MreSnct, MreOtft, MrePerk
        # ---------------------------------------------------------------------
        # Unused records, they have empty GRUP in skyrim.esm-------------------
        # CLDC HAIR PWAT RGDL SCOL SCPT
        # ---------------------------------------------------------------------
        # These Are normally not mergeable but added to brec.MreRecord.type_class
        #
        #       MreCell,
        # ---------------------------------------------------------------------
        # These have undefined FormIDs Do not merge them
        #
        #       MreNavi, MreNavm,
        # ---------------------------------------------------------------------
        # These need syntax revision but can be merged once that is corrected
        #
        #       MreAchr, MreDial, MreLctn, MreInfo, MreFact,
        # ---------------------------------------------------------------------
        cls.mergeClasses = (# MreAchr, MreDial, MreInfo, MreFact,
            MreAact, MreActi, MreAddn, MreAlch, MreAmmo, MreAnio, MreAppa,
            MreArma, MreArmo, MreArto, MreAspc, MreAstp, MreAvif, MreBook,
            MreBptd, MreCams, MreClas, MreClfm, MreClmt, MreCobj, MreColl,
            MreCont, MreCpth, MreCsty, MreDebr, MreDlbr, MreDlvw, MreDobj,
            MreDoor, MreDual, MreEczn, MreEfsh, MreEnch, MreEqup, MreExpl,
            MreEyes, MreFlor, MreFlst, MreFstp, MreFsts, MreFurn, MreGlob,
            MreGmst, MreGras, MreHazd, MreHdpt, MreIdle, MreIdlm, MreImad,
            MreImgs, MreIngr, MreIpct, MreIpds, MreKeym, MreKywd, MreLcrt,
            MreLctn, MreLgtm, MreLigh, MreLscr, MreLtex, MreLvli, MreLvln,
            MreLvsp, MreMato, MreMatt, MreMesg, MreMgef, MreMisc, MreMovt,
            MreMstt, MreMusc, MreMust, MreNpc, MreOtft, MrePerk, MreProj,
            MreRegn, MreRela, MreRevb, MreRfct, MreScrl, MreShou, MreSlgm,
            MreSmbn, MreSmen, MreSmqn, MreSnct, MreSndr, MreSopm, MreSoun,
            MreSpel, MreSpgd, MreStat, MreTact, MreTree, MreTxst, MreVtyp,
            MreWatr, MreWeap, MreWoop, MreWthr,
            ####### for debug
            MreQust,)

        # MreScpt is Oblivion/FO3/FNV Only
        # MreMgef, has not been verified to be used here for Skyrim

        # Setting RecordHeader class variables --------------------------------
        brec.RecordHeader.topTypes = cls.str_to_bytes(
           ['GMST', 'KYWD', 'LCRT', 'AACT', 'TXST',
            'GLOB', 'CLAS', 'FACT', 'HDPT', 'HAIR', 'EYES', 'RACE', 'SOUN',
            'ASPC', 'MGEF', 'SCPT', 'LTEX', 'ENCH', 'SPEL', 'SCRL', 'ACTI',
            'TACT', 'ARMO', 'BOOK', 'CONT', 'DOOR', 'INGR', 'LIGH', 'MISC',
            'APPA', 'STAT', 'SCOL', 'MSTT', 'PWAT', 'GRAS', 'TREE', 'CLDC',
            'FLOR', 'FURN', 'WEAP', 'AMMO', 'NPC_', 'LVLN', 'KEYM', 'ALCH',
            'IDLM', 'COBJ', 'PROJ', 'HAZD', 'SLGM', 'LVLI', 'WTHR', 'CLMT',
            'SPGD', 'RFCT', 'REGN', 'NAVI', 'CELL', 'WRLD', 'DIAL', 'QUST',
            'IDLE', 'PACK', 'CSTY', 'LSCR', 'LVSP', 'ANIO', 'WATR', 'EFSH',
            'EXPL', 'DEBR', 'IMGS', 'IMAD', 'FLST', 'PERK', 'BPTD', 'ADDN',
            'AVIF', 'CAMS', 'CPTH', 'VTYP', 'MATT', 'IPCT', 'IPDS', 'ARMA',
            'ECZN', 'LCTN', 'MESG', 'RGDL', 'DOBJ', 'LGTM', 'MUSC', 'FSTP',
            'FSTS', 'SMBN', 'SMQN', 'SMEN', 'DLBR', 'MUST', 'DLVW', 'WOOP',
            'SHOU', 'EQUP', 'RELA', 'SCEN', 'ASTP', 'OTFT', 'ARTO', 'MATO',
            'MOVT', 'SNDR', 'DUAL', 'SNCT', 'SOPM', 'COLL', 'CLFM', 'REVB'])
        #-> this needs updating for Skyrim
        brec.RecordHeader.recordTypes = set(
            brec.RecordHeader.topTypes + [b'GRUP', b'TES4', b'REFR', b'ACHR',
                                          b'ACRE', b'LAND', b'INFO', b'NAVM',
                                          b'PHZD', b'PGRE'])
        brec.RecordHeader.plugin_form_version = 43
        brec.MreRecord.type_class = dict((x.classType,x) for x in (
            MreAchr, MreDial, MreInfo, MreAact, MreActi, MreAddn, MreAlch,
            MreAmmo, MreAnio, MreAppa, MreArma, MreArmo, MreArto, MreAspc,
            MreAstp, MreAvif, MreBook, MreBptd, MreCams, MreClas, MreClfm,
            MreClmt, MreCobj, MreColl, MreCont, MreCpth, MreCsty, MreDebr,
            MreDlbr, MreDlvw, MreDobj, MreDoor, MreDual, MreEczn, MreEfsh,
            MreEnch, MreEqup, MreExpl, MreEyes, MreFact, MreFlor, MreFlst,
            MreFstp, MreFsts, MreFurn, MreGlob, MreGmst, MreGras, MreHazd,
            MreHdpt, MreIdle, MreIdlm, MreImad, MreImgs, MreIngr, MreIpct,
            MreIpds, MreKeym, MreKywd, MreLcrt, MreLctn, MreLgtm, MreLigh,
            MreLscr, MreLtex, MreLvli, MreLvln, MreLvsp, MreMato, MreMatt,
            MreMesg, MreMgef, MreMisc, MreMovt, MreMstt, MreMusc, MreMust,
            MreNpc, MreOtft, MrePerk, MreProj, MreRegn, MreRela, MreRevb,
            MreRfct, MreScrl, MreShou, MreSlgm, MreSmbn, MreSmen, MreSmqn,
            MreSnct, MreSndr, MreSopm, MreSoun, MreSpel, MreSpgd, MreStat,
            MreTact, MreTree, MreTxst, MreVtyp, MreWatr, MreWeap, MreWoop,
            MreWthr, MreCell, MreWrld,  # MreNavm, MreNavi
            ####### for debug
            MreQust, MreHeader,
        ))
        brec.MreRecord.simpleTypes = (
            set(brec.MreRecord.type_class) - {b'TES4', b'ACHR', b'CELL',
                                              b'DIAL', b'INFO', b'WRLD', })

GAME_TYPE = SkyrimGameInfo
