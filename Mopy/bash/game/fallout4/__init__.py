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
"""GameInfo override for Fallout 4."""

from .. import GameInfo
from ... import brec

class Fallout4GameInfo(GameInfo):
    displayName = 'Fallout 4'
    fsName = 'Fallout4'
    altName = 'Wrye Flash'
    defaultIniFile = 'Fallout4_default.ini'
    launch_exe = 'Fallout4.exe'
    game_detect_file = ['Fallout4.exe']
    version_detect_file = ['Fallout4.exe']
    masterFiles = ['Fallout4.esm']
    iniFiles = ['Fallout4.ini', 'Fallout4Prefs.ini', 'Fallout4Custom.ini', ]
    pklfile = 'bash\\db\\Fallout4_ids.pkl'
    masterlist_dir = 'Fallout4'
    regInstallKeys = ('Bethesda Softworks\\Fallout4', 'Installed Path')
    nexusUrl = 'https://www.nexusmods.com/fallout4/'
    nexusName = 'Fallout 4 Nexus'
    nexusKey = 'bash.installers.openFallout4Nexus.continue'

    bsa_extension = 'ba2'
    vanilla_string_bsas = {
        'fallout4.esm': ['Fallout4 - Interface.ba2'],
        'dlcrobot.esm': ['DLCRobot - Main.ba2'],
        'dlcworkshop01.esm': ['DLCworkshop01 - Main.ba2'],
        'dlcworkshop02.esm': ['DLCworkshop02 - Main.ba2'],
        'dlcworkshop03.esm': ['DLCworkshop03 - Main.ba2'],
        'dlccoast.esm': ['DLCCoast - Main.ba2'],
        'dlcnukaworld.esm':  ['DLCNukaWorld - Main.ba2'],
    }
    resource_archives_keys = (
        'sResourceIndexFileList', 'sResourceStartUpArchiveList',
        'sResourceArchiveList', 'sResourceArchiveList2',
        'sResourceArchiveListBeta'
    )

    espm_extensions = {'.esp', '.esm', '.esl'}
    script_extensions = {'.psc'}
    has_achlist = True
    check_esl = True

    class cs(GameInfo.cs):
        # TODO:  When the Fallout 4 Creation Kit is actually released,
        # double check that the filename is correct, and create an actual icon
        cs_abbrev = 'FO4CK'
        long_name = 'Creation Kit'
        exe = 'CreationKit.exe'
        se_args = None
        image_name = 'creationkit%s.png'

    class se(GameInfo.se):
        se_abbrev = 'F4SE'
        long_name = 'Fallout 4 Script Extender'
        exe = 'f4se_loader.exe'
        steam_exe = 'f4se_steam_loader.dll'
        plugin_dir = 'F4SE'
        cosave_ext = '.f4se'
        url = 'http://f4se.silverlock.org/'
        url_tip = 'http://f4se.silverlock.org/'

    class ini(GameInfo.ini):
        allowNewLines = True
        bsaRedirection = ('','')

    class ess(GameInfo.ess):
        ext = '.fos'

    class pnd(GameInfo.pnd):
        facegen_dir_1 = ['meshes', 'actors', 'character', 'facegendata',
                         'facegeom']
        facegen_dir_2 = ['meshes', 'actors', 'character',
                         'facecustomization']

    # BAIN:
    dataDirs = GameInfo.dataDirs | {
        'interface',
        'lodsettings',
        'materials',
        'misc',
        'programs',
        'scripts',
        'seq',
        'shadersfx',
        'strings',
        'vis',
    }
    dataDirsPlus = {
        'f4se',
        'ini',
        'mcm',   # FO4 MCM
        'tools', # bodyslide
    }
    dontSkipDirs = {
        # This rule is to allow mods with string translation enabled.
        'interface\\translations':['.txt']
    }
    SkipBAINRefresh = {'fo4edit backups', 'fo4edit cache'}

    class esp(GameInfo.esp):
        canBash = True
        canEditHeader = True
        validHeaderVersions = (0.95,)

    allTags = {'Delev', 'Relev'}

    patchers = ('ListsMerger',)

    # ---------------------------------------------------------------------
    # --Imported - MreGlob is special import, not in records.py
    # ---------------------------------------------------------------------
    @classmethod
    def init(cls):
        cls._dynamic_import_modules(__name__)
        # First import from fallout4.records file, so MelModel is set correctly
        from .records import MreHeader, MreLvli, MreLvln
        # ---------------------------------------------------------------------
        # These Are normally not mergable but added to brec.MreRecord.type_class
        #
        #       MreCell,
        # ---------------------------------------------------------------------
        # These have undefined FormIDs Do not merge them
        #
        #       MreNavi, MreNavm,
        # ---------------------------------------------------------------------
        # These need syntax revision but can be merged once that is corrected
        #
        #       MreAchr, MreDial, MreLctn, MreInfo, MreFact, MrePerk,
        # ---------------------------------------------------------------------
        cls.mergeClasses = (
            # -- Imported from Skyrim/SkyrimSE
            # Added to records.py
            MreLvli, MreLvln
        )
        # Setting RecordHeader class variables --------------------------------
        brec.RecordHeader.topTypes = cls.str_to_bytes([
            'GMST', 'KYWD', 'LCRT', 'AACT', 'TRNS', 'CMPO', 'TXST', 'GLOB',
            'DMGT', 'CLAS', 'FACT', 'HDPT', 'RACE', 'SOUN', 'ASPC', 'MGEF',
            'LTEX', 'ENCH', 'SPEL', 'ACTI', 'TACT', 'ARMO', 'BOOK', 'CONT',
            'DOOR', 'INGR', 'LIGH', 'MISC', 'STAT', 'SCOL', 'MSTT', 'GRAS',
            'TREE', 'FLOR', 'FURN', 'WEAP', 'AMMO', 'NPC_', 'PLYR', 'LVLN',
            'KEYM', 'ALCH', 'IDLM', 'NOTE', 'PROJ', 'HAZD', 'BNDS', 'TERM',
            'LVLI', 'WTHR', 'CLMT', 'SPGD', 'RFCT', 'REGN', 'NAVI', 'CELL',
            'WRLD', 'QUST', 'IDLE', 'PACK', 'CSTY', 'LSCR', 'LVSP', 'ANIO',
            'WATR', 'EFSH', 'EXPL', 'DEBR', 'IMGS', 'IMAD', 'FLST', 'PERK',
            'BPTD', 'ADDN', 'AVIF', 'CAMS', 'CPTH', 'VTYP', 'MATT', 'IPCT',
            'IPDS', 'ARMA', 'ECZN', 'LCTN', 'MESG', 'DOBJ', 'DFOB', 'LGTM',
            'MUSC', 'FSTP', 'FSTS', 'SMBN', 'SMQN', 'SMEN', 'DLBR', 'MUST',
            'DLVW', 'EQUP', 'RELA', 'SCEN', 'ASTP', 'OTFT', 'ARTO', 'MATO',
            'MOVT', 'SNDR', 'SNCT', 'SOPM', 'COLL', 'CLFM', 'REVB', 'PKIN',
            'RFGP', 'AMDL', 'LAYR', 'COBJ', 'OMOD', 'MSWP', 'ZOOM', 'INNR',
            'KSSM', 'AECH', 'SCCO', 'AORU', 'SCSN', 'STAG', 'NOCM', 'LENS',
            'GDRY', 'OVIS'])
        brec.RecordHeader.recordTypes = (set(brec.RecordHeader.topTypes) |
            {b'GRUP', b'TES4', b'REFR', b'ACHR', b'PMIS', b'PARW', b'PGRE',
             b'PBEA', b'PFLA', b'PCON', b'PBAR', b'PHZD', b'LAND', b'NAVM',
             b'DIAL', b'INFO'})
        brec.RecordHeader.plugin_form_version = 131
        brec.MreRecord.type_class = dict((x.classType,x) for x in (
            #--Always present
            MreHeader, MreLvli, MreLvln,
            # Imported from Skyrim or SkyrimSE
            # Added to records.py
            ))
        brec.MreRecord.simpleTypes = (
            set(brec.MreRecord.type_class) - {b'TES4',})

GAME_TYPE = Fallout4GameInfo
