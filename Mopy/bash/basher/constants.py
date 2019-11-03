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

"""This module contains some constants ripped out of basher.py"""
from .. import bass, bush
from ..balt import Image, ImageList, defPos

# Color Descriptions ----------------------------------------------------------
colorInfo = {
    'default.text': (_('Default Text'),
        _('This is the text color used for list items when no other is '
        'specified.  For example, an ESP that is not mergeable or ghosted, '
        'and has no other problems.'),
    ),
    'default.bkgd': (_('Default Background'),
        _('This is the text background color used for list items when no '
          'other is specified.  For example, an ESM that is not ghosted.'),
    ),
    'mods.text.esm': (_('ESM'),
        _('Tabs: Mods, Saves') + '\n\n' +
        _('This is the text color used for ESMs in the Mods Tab, and in the '
          'Masters info on both the Mods Tab and Saves Tab.'),),
    'mods.text.esl': (_('ESL'),
        _('Tabs: Mods, Saves') + '\n\n' +
        _('This is the text color used for ESLs in the Mods Tab, and in the '
          'Masters info on both the Mods Tab and Saves Tab.'),),
    'mods.text.eslm': (_('ESLM'),
        _('Tabs: Mods, Saves') + '\n\n' +
        _('This is the text color used for ESLs with a master flag in the '
          'Mods Tab, and in the Masters info on both the Mods Tab and Saves '
          'Tab.'),),
    'mods.text.noMerge': (_("'NoMerge' Plugin"),
        _('Tabs: Mods') + '\n\n' +
        _("This is the text color used for a mergeable plugin that is "
          "tagged 'NoMerge'."),
    ),
    'mods.text.bashedPatch': (_("Bashed Patch"),
        _('Tabs: Mods') + '\n\n' +
        _("This is the text color used for Bashed Patches."),
    ),
    'mods.bkgd.doubleTime.exists': (_('Inactive Time Conflict'),
        _('Tabs: Mods') + '\n\n' +
        _('This is the background color used for a plugin with an inactive '
          'time conflict.  This means that two or more plugins have the same '
          'timestamp, but only one (or none) of them is active.'),
    ),
    'mods.bkgd.doubleTime.load': (_('Active Time Conflict'),
        _('Tabs: Mods') + '\n\n' +
        _('This is the background color used for a plugin with an active '
          'time conflict.  This means that two or more plugins with the same '
          'timestamp are active.'),
    ),
    'mods.bkgd.deactivate': (_("'Deactivate' Plugin"),
        _('Tabs: Mods') + '\n\n' +
        _("This is the background color used for an active plugin that is "
          "tagged 'Deactivate'."),
    ),
    'mods.bkgd.ghosted': (_('Ghosted Plugin'),
        _('Tabs: Mods') + '\n\n' +
        _('This is the background color used for a ghosted plugin.'),
    ),
    'ini.bkgd.invalid': (_('Invalid INI Tweak'),
        _('Tabs: INI Edits') + '\n\n' +
        _('This is the background color used for a tweak file that is invalid'
          ' for the currently selected target INI.'),
    ),
    'tweak.bkgd.invalid': (_('Invalid Tweak Line'),
        _('Tabs: INI Edits') + '\n\n' +
        _('This is the background color used for a line in a tweak file that '
          'is invalid for the currently selected target INI.'),
    ),
    'tweak.bkgd.mismatched': (_('Mismatched Tweak Line'),
        _('Tabs: INI Edits') + '\n\n' +
        _('This is the background color used for a line in a tweak file that '
          'does not match what is set in the target INI.'),
    ),
    'tweak.bkgd.matched': (_('Matched Tweak Line'),
        _('Tabs: INI Edits') + '\n\n' +
        _('This is the background color used for a line in a tweak file that '
          'matches what is set in the target INI.'),
    ),
    'installers.text.complex': (_('Complex Installer'),
        _('Tabs: Installers') + '\n\n' +
        _('This is the text color used for a complex BAIN package.'),
    ),
    'installers.text.invalid': (_('Invalid'),
        _('Tabs: Installers') + '\n\n' +
        _('This is the text color used for invalid packages.'),
    ),
    'installers.text.marker': (_('Marker'),
        _('Tabs: Installers') + '\n\n' +
        _('This is the text color used for Markers.'),
    ),
    'installers.bkgd.skipped': (_('Skipped Files'),
        _('Tabs: Installers') + '\n\n' +
        _('This is the background color used for a package with files that '
          'will not be installed by BAIN.  This means some files are selected'
          ' to be installed, but due to your current Skip settings (for '
          'example, Skip DistantLOD), will not be installed.'),
    ),
    'installers.bkgd.outOfOrder': (_('Installer Out of Order'),
        _('Tabs: Installers') + '\n\n' +
        _('This is the background color used for an installer with files '
          'installed, that should be overridden by a package with a higher '
          'install order.  It can be repaired with an Anneal or Anneal All.'),
    ),
    'installers.bkgd.dirty': (_('Dirty Installer'),
        _('Tabs: Installers') + '\n\n' +
        _('This is the background color used for an installer that is '
          'configured in a "dirty" manner.  This means changes have been made'
          ' to its configuration, and an Anneal or Install needs to be '
          'performed to make the install match what is configured.'),
    ),
    'screens.bkgd.image': (_('Screenshot Background'),
        _('Tabs: Saves, Screens') + '\n\n' +
        _('This is the background color used for images.'),
    ),
}
if bush.game.check_esl:
    colorInfo['mods.text.mergeable'] = (_('ESL Capable plugin'),
            _('Tabs: Mods') + '\n\n' +
            _('This is the text color used for ESL Capable plugins.'),
        )
else:
    colorInfo['mods.text.mergeable'] = (_('Mergeable Plugin'),
            _('Tabs: Mods') + '\n\n' +
            _('This is the text color used for mergeable plugins.'),
        )

#--Load config/defaults
settingDefaults = { ##: (178) belongs to bosh (or better to a settings package)
    #--Basics
    'bash.version': 0,
    'bash.CBashEnabled': True,
    'bash.backupPath': None,
    'bash.frameMax': False, # True if maximized
    'bash.page':1,
    'bash.useAltName':True,
    'bash.pluginEncoding': 'cp1252',    # Western European
    #--Colors
    'bash.colors': {
        #--Common Colors
        'default.text':                 'BLACK',
        'default.bkgd':                 'WHITE',
        #--Mods Tab
        'mods.text.esm':                'BLUE',
        'mods.text.mergeable':          (0x00, 0x99, 0x00),
        'mods.text.noMerge':            (150, 130, 0),
        'mods.bkgd.doubleTime.exists':  (0xFF, 0xDC, 0xDC),
        'mods.bkgd.doubleTime.load':    (0xFF, 0x64, 0x64),
        'mods.bkgd.deactivate':         (0xFF, 0x64, 0x64),
        'mods.bkgd.ghosted':            (0xE8, 0xE8, 0xE8),
        'mods.text.eslm':               (123, 29, 223),
        'mods.text.esl':                (226, 54, 197),
        'mods.text.bashedPatch':        (30, 157, 251),
        #--INI Edits Tab
        'ini.bkgd.invalid':             (0xDF, 0xDF, 0xDF),
        'tweak.bkgd.invalid':           (0xFF, 0xD5, 0xAA),
        'tweak.bkgd.mismatched':        (0xFF, 0xFF, 0xBF),
        'tweak.bkgd.matched':           (0xC1, 0xFF, 0xC1),
        #--Installers Tab
        'installers.text.complex':      'NAVY',
        'installers.text.invalid':      'GREY',
        'installers.text.marker':       (230, 97, 89),
        'installers.bkgd.skipped':      (0xE0, 0xE0, 0xE0),
        'installers.bkgd.outOfOrder':   (0xFF, 0xFF, 0x00),
        'installers.bkgd.dirty':        (0xFF, 0xBB, 0x33),
        #--Screens Tab
        'screens.bkgd.image':           (0x64, 0x64, 0x64),
        },
    #--BSA Redirection
    'bash.bsaRedirection':True,
    #--Wrye Bash: Load Lists
    'bash.loadLists.data': {},
    #--Wrye Bash: StatusBar
    'bash.statusbar.iconSize': 16,
    'bash.statusbar.hide': set(),
    'bash.statusbar.order': [],
    'bash.statusbar.showversion': False,
    #--Wrye Bash: Group and Rating
    'bash.mods.autoGhost': False,
    'bash.mods.groups': [
        'Root',
        'Library',
        'Cosmetic',
        'Clothing',
        'Weapon',
        'Tweak',
        'Overhaul',
        'Misc.',
        'Magic',
        'NPC',
        'Home',
        'Place',
        'Quest',
        'Last',
    ],
    'bash.mods.ratings': ['+','1','2','3','4','5','=','~'],
    #--Wrye Bash: Col (Sort) Names
    'bash.colNames': {
        'Mod Status': _('Mod Status'),
        'Author': _('Author'),
        'Cell': _('Cell'),
        'CRC':_('CRC'),
        'Current Order': _('Current LO'),
        'Date': _('Date'),
        'Day': _('Day'),
        'File': _('File'),
        'Files': _('Files'),
        'Group': _('Group'),
        'Header': _('Header'),
        'Installer':_('Installer'),
        'Karma': _('Karma'),
        'Load Order': _('Load Order'),
        'Modified': _('Modified'),
        'Name': _('Name'),
        'Num': _('MI'),
        'Order': _('Order'),
        'Package': _('Package'),
        'PlayTime':_('Hours'),
        'Player': _('Player'),
        'Rating': _('Rating'),
        'Save Order': _('Save Order'),
        'Size': _('Size'),
        'Status': _('Status'),
        'Subject': _('Subject'),
        },
    #--Wrye Bash: Masters
    'bash.masters.cols': ['File', 'Num', 'Current Order'],
    'bash.masters.esmsFirst': 1,
    'bash.masters.selectedFirst': 0,
    'bash.masters.sort': 'Num',
    'bash.masters.colReverse': {},
    'bash.masters.colWidths': {
        'File':80,
        'Num':30,
        'Current Order':60,
        },
    #--Wrye Bash: Mod Docs
    'bash.modDocs.show': False,
    'bash.modDocs.dir': None,
    #--Installers
    'bash.installers.cols': ['Package','Order','Modified','Size','Files'],
    'bash.installers.colReverse': {},
    'bash.installers.sort': 'Order',
    'bash.installers.colWidths': {
        'Package':230,
        'Order':25,
        'Modified':135,
        'Size':75,
        'Files':55,
        },
    'bash.installers.page':0,
    'bash.installers.enabled': True,
    'bash.installers.autoAnneal': True,
    'bash.installers.autoWizard':True,
    'bash.installers.wizardOverlay':True,
    'bash.installers.fastStart': True,
    'bash.installers.autoRefreshBethsoft': False,
    'bash.installers.autoRefreshProjects': True,
    'bash.installers.removeEmptyDirs':True,
    'bash.installers.skipScreenshots':False,
    'bash.installers.skipScriptSources':False,
    'bash.installers.skipImages':False,
    'bash.installers.skipDocs':False,
    'bash.installers.skipDistantLOD':False,
    'bash.installers.skipLandscapeLODMeshes':False,
    'bash.installers.skipLandscapeLODTextures':False,
    'bash.installers.skipLandscapeLODNormals':False,
    'bash.installers.skipTESVBsl':True,
    'bash.installers.allowOBSEPlugins':True,
    'bash.installers.renameStrings':True,
    'bash.installers.sortProjects':False,
    'bash.installers.sortActive':False,
    'bash.installers.sortStructure':False,
    'bash.installers.conflictsReport.showLower':True,
    'bash.installers.conflictsReport.showInactive':False,
    'bash.installers.conflictsReport.showBSAConflicts':False,
    'bash.installers.goodDlls':{},
    'bash.installers.badDlls':{},
    'bash.installers.onDropFiles.action':None,
    'bash.installers.commentsSplitterSashPos':0,
    #--Wrye Bash: Wizards
    'bash.wizard.size': (600,500),
    'bash.wizard.pos': tuple(defPos),
    #--Wrye Bash: INI Tweaks
    'bash.ini.cols': ['File','Installer'],
    'bash.ini.sort': 'File',
    'bash.ini.colReverse': {},
    'bash.ini.sortValid': True,
    'bash.ini.colWidths': {
        'File':300,
        'Installer':100,
        },
    'bash.ini.choices': {},
    'bash.ini.choice': 0,
    'bash.ini.allowNewLines': bush.game.ini.allowNewLines,
    #--Wrye Bash: Mods
    'bash.mods.cols': ['File', 'Load Order', 'Installer', 'Modified', 'Size',
                       'Author', 'CRC'],
    'bash.mods.esmsFirst': 1,
    'bash.mods.selectedFirst': 0,
    'bash.mods.sort': 'Load Order',
    'bash.mods.colReverse': {},
    'bash.mods.colWidths': {
        'Author':100,
        'File':200,
        'Group':10,
        'Installer':100,
        'Load Order':25,
        'Modified':135,
        'Rating':10,
        'Size':75,
        'CRC':60,
        'Mod Status':50,
        },
    'bash.mods.renames': {},
    'bash.mods.scanDirty': False,
    'bash.mods.export.skip': '',
    'bash.mods.export.deprefix': '',
    'bash.mods.export.skipcomments': False,
    #--Wrye Bash: Saves
    'bash.saves.cols': ['File','Modified','Size','PlayTime','Player','Cell'],
    'bash.saves.sort': 'Modified',
    'bash.saves.colReverse': {
        'Modified':1,
        },
    'bash.saves.colWidths': {
        'File':375,
        'Modified':135,
        'Size':65,
        'PlayTime':50,
        'Player':70,
        'Cell':80,
        },
    #Wrye Bash: BSAs
    'bash.BSAs.cols': ['File', 'Modified', 'Size'],
    'bash.BSAs.colReverse': {
        'Modified':1,
        },
    'bash.BSAs.colWidths': {
        'File':150,
        'Modified':150,
        'Size':75,
        },
    'bash.BSAs.sort': 'File',
    #--Wrye Bash: Screens
    'bash.screens.cols': ['File'],
    'bash.screens.sort': 'File',
    'bash.screens.colReverse': {
        'Modified':1,
        },
    'bash.screens.colWidths': {
        'File':100,
        'Modified':150,
        'Size':75,
        },
    'bash.screens.jpgQuality': 95,
    'bash.screens.jpgCustomQuality': 75,
    #--Wrye Bash: People
    'bash.people.cols': ['Name','Karma','Header'],
    'bash.people.sort': 'Name',
    'bash.people.colReverse': {},
    'bash.people.colWidths': {
        'Name': 80,
        'Karma': 25,
        'Header': 50,
        },
    #--Tes4View/Edit/Trans
    'tes4View.iKnowWhatImDoing':False,
    'tes5View.iKnowWhatImDoing':False,
    'sseView.iKnowWhatImDoing':False,
    'fo4View.iKnowWhatImDoing':False,
    'fo3View.iKnowWhatImDoing':False,
    'fnvView.iKnowWhatImDoing':False,
    'enderalView.iKnowWhatImDoing':False,
    #--BOSS:
    'BOSS.ClearLockTimes':True,
    'BOSS.AlwaysUpdate':True,
    'BOSS.UseGUI':False,
    }

# Images ----------------------------------------------------------------------
#------------------------------------------------------------------------------
imDirJn = bass.dirs['images'].join
def _png(name): return Image(imDirJn(name)) ##: not png necessarily, rename!

#--Image lists
karmacons = ImageList(16,16)
karmacons.images.extend(list({
    'karma+5': _png('checkbox_purple_inc.png'),
    'karma+4': _png('checkbox_blue_inc.png'),
    'karma+3': _png('checkbox_blue_inc.png'),
    'karma+2': _png('checkbox_green_inc.png'),
    'karma+1': _png('checkbox_green_inc.png'),
    'karma+0': _png('checkbox_white_off.png'),
    'karma-1': _png('checkbox_yellow_off.png'),
    'karma-2': _png('checkbox_yellow_off.png'),
    'karma-3': _png('checkbox_orange_off.png'),
    'karma-4': _png('checkbox_orange_off.png'),
    'karma-5': _png('checkbox_red_off.png'),
    }.items()))
installercons = ImageList(16,16)
installercons.images.extend(list({
    #--Off/Archive
    'off.green':  _png('checkbox_green_off.png'),
    'off.grey':   _png('checkbox_grey_off.png'),
    'off.red':    _png('checkbox_red_off.png'),
    'off.white':  _png('checkbox_white_off.png'),
    'off.orange': _png('checkbox_orange_off.png'),
    'off.yellow': _png('checkbox_yellow_off.png'),
    #--Off/Archive - Wizard
    'off.green.wiz':    _png('checkbox_green_off_wiz.png'),
    #grey
    'off.red.wiz':      _png('checkbox_red_off_wiz.png'),
    'off.white.wiz':    _png('checkbox_white_off_wiz.png'),
    'off.orange.wiz':   _png('checkbox_orange_off_wiz.png'),
    'off.yellow.wiz':   _png('checkbox_yellow_off_wiz.png'),
    #--On/Archive
    'on.green':  _png('checkbox_green_inc.png'),
    'on.grey':   _png('checkbox_grey_inc.png'),
    'on.red':    _png('checkbox_red_inc.png'),
    'on.white':  _png('checkbox_white_inc.png'),
    'on.orange': _png('checkbox_orange_inc.png'),
    'on.yellow': _png('checkbox_yellow_inc.png'),
    #--On/Archive - Wizard
    'on.green.wiz':  _png('checkbox_green_inc_wiz.png'),
    #grey
    'on.red.wiz':    _png('checkbox_red_inc_wiz.png'),
    'on.white.wiz':  _png('checkbox_white_inc_wiz.png'),
    'on.orange.wiz': _png('checkbox_orange_inc_wiz.png'),
    'on.yellow.wiz': _png('checkbox_yellow_inc_wiz.png'),
    #--Off/Directory
    'off.green.dir':  _png('diamond_green_off.png'),
    'off.grey.dir':   _png('diamond_grey_off.png'),
    'off.red.dir':    _png('diamond_red_off.png'),
    'off.white.dir':  _png('diamond_white_off.png'),
    'off.orange.dir': _png('diamond_orange_off.png'),
    'off.yellow.dir': _png('diamond_yellow_off.png'),
    #--Off/Directory - Wizard
    'off.green.dir.wiz':  _png('diamond_green_off_wiz.png'),
    #grey
    'off.red.dir.wiz':    _png('diamond_red_off_wiz.png'),
    'off.white.dir.wiz':  _png('diamond_white_off_wiz.png'),
    'off.orange.dir.wiz': _png('diamond_orange_off_wiz.png'),
    'off.yellow.dir.wiz': _png('diamond_yellow_off_wiz.png'),
    #--On/Directory
    'on.green.dir':  _png('diamond_green_inc.png'),
    'on.grey.dir':   _png('diamond_grey_inc.png'),
    'on.red.dir':    _png('diamond_red_inc.png'),
    'on.white.dir':  _png('diamond_white_inc.png'),
    'on.orange.dir': _png('diamond_orange_inc.png'),
    'on.yellow.dir': _png('diamond_yellow_inc.png'),
    #--On/Directory - Wizard
    'on.green.dir.wiz':  _png('diamond_green_inc_wiz.png'),
    #grey
    'on.red.dir.wiz':    _png('diamond_red_inc_wiz.png'),
    'on.white.dir.wiz':  _png('diamond_white_off_wiz.png'),
    'on.orange.dir.wiz': _png('diamond_orange_inc_wiz.png'),
    'on.yellow.dir.wiz': _png('diamond_yellow_inc_wiz.png'),
    #--Broken
    'corrupt':   _png('red_x.png'),
    }.items()))

#--Buttons
def imageList(template):
    return [Image(imDirJn(template % x)) for x in (16,24,32)]

# TODO(65): game handling refactoring - some of the buttons are game specific
toolbar_buttons = (
        ('ISOBL', imageList('tools/isobl%s.png'),
        _("Launch InsanitySorrow's Oblivion Launcher")),
        ('ISRMG', imageList("tools/insanity'sreadmegenerator%s.png"),
        _("Launch InsanitySorrow's Readme Generator")),
        ('ISRNG', imageList("tools/insanity'srng%s.png"),
        _("Launch InsanitySorrow's Random Name Generator")),
        ('ISRNPCG', imageList('tools/randomnpc%s.png'),
        _("Launch InsanitySorrow's Random NPC Generator")),
        ('OBFEL', imageList('tools/oblivionfaceexchangerlite%s.png'),
        _("Oblivion Face Exchange Lite")),
        ('OBMLG', imageList('tools/modlistgenerator%s.png'),
        _("Oblivion Mod List Generator")),
        ('BSACMD', imageList('tools/bsacommander%s.png'),
        _("Launch BSA Commander")),
        ('Tabula', imageList('tools/tabula%s.png'),
         _("Launch Tabula")),
        ('Tes4FilesPath', imageList('tools/tes4files%s.png'),
        _("Launch TES4Files")),
)

modeling_tools_buttons = (
    ('AutoCad', imageList('tools/autocad%s.png'), _("Launch AutoCad")),
    ('BlenderPath', imageList('tools/blender%s.png'), _("Launch Blender")),
    ('Dogwaffle', imageList('tools/dogwaffle%s.png'), _("Launch Dogwaffle")),
    ('GmaxPath', imageList('tools/gmax%s.png'), _("Launch Gmax")),
    ('MayaPath', imageList('tools/maya%s.png'), _("Launch Maya")),
    ('MaxPath', imageList('tools/3dsmax%s.png'), _("Launch 3dsMax")),
    ('Milkshape3D', imageList('tools/milkshape3d%s.png'),
     _("Launch Milkshape 3D")),
    ('Mudbox', imageList('tools/mudbox%s.png'), _("Launch Mudbox")),
    ('Sculptris', imageList('tools/sculptris%s.png'), _("Launch Sculptris")),
    ('SpeedTree', imageList('tools/speedtree%s.png'), _("Launch SpeedTree")),
    ('Treed', imageList('tools/treed%s.png'), _("Launch Tree\[d\]")),
    ('Wings3D', imageList('tools/wings3d%s.png'), _("Launch Wings 3D")),
)

texture_tool_buttons = (
    ('AniFX', imageList('tools/anifx%s.png'), _("Launch AniFX")),
    ('ArtOfIllusion', imageList('tools/artofillusion%s.png'),
     _("Launch Art Of Illusion")),
    ('Artweaver', imageList('tools/artweaver%s.png'), _("Launch Artweaver")),
    ('CrazyBump', imageList('tools/crazybump%s.png'), _("Launch CrazyBump")),
    ('DDSConverter', imageList('tools/ddsconverter%s.png'),
     _("Launch DDSConverter")),
    ('DeepPaint', imageList('tools/deeppaint%s.png'), _("Launch DeepPaint")),
    ('FastStone', imageList('tools/faststoneimageviewer%s.png'),
     _("Launch FastStone Image Viewer")),
    ('Genetica', imageList('tools/genetica%s.png'), _("Launch Genetica")),
    ('GeneticaViewer', imageList('tools/geneticaviewer%s.png'),
     _("Launch Genetica Viewer")),
    ('GIMP', imageList('tools/gimp%s.png'), _("Launch GIMP")),
    ('IcoFX', imageList('tools/icofx%s.png'), _("Launch IcoFX")),
    ('Inkscape', imageList('tools/inkscape%s.png'), _("Launch Inkscape")),
    ('IrfanView', imageList('tools/irfanview%s.png'), _("Launch IrfanView")),
    ('Krita', imageList('tools/krita%s.png'), _("Launch Krita")),
    ('MaPZone', imageList('tools/mapzone%s.png'), _("Launch MaPZone")),
    ('MyPaint', imageList('tools/mypaint%s.png'), _("Launch MyPaint")),
    ('NVIDIAMelody', imageList('tools/nvidiamelody%s.png'),
     _("Launch Nvidia Melody")),
    ('PaintNET', imageList('tools/paint.net%s.png'), _("Launch Paint.NET")),
    ('PaintShopPhotoPro', imageList('tools/paintshopprox3%s.png'),
     _("Launch PaintShop Photo Pro")),
    ('PhotoshopPath', imageList('tools/photoshop%s.png'),
     _("Launch Photoshop")),
    ('PhotoScape', imageList('tools/photoscape%s.png'),
     _("Launch PhotoScape")),
    ('PhotoSEAM', imageList('tools/photoseam%s.png'), _("Launch PhotoSEAM")),
    ('Photobie', imageList('tools/photobie%s.png'), _("Launch Photobie")),
    ('PhotoFiltre', imageList('tools/photofiltre%s.png'),
     _("Launch PhotoFiltre")),
    ('PixelStudio', imageList('tools/pixelstudiopro%s.png'),
     _("Launch Pixel Studio Pro")),
    ('Pixia', imageList('tools/pixia%s.png'), _("Launch Pixia")),
    ('TextureMaker', imageList('tools/texturemaker%s.png'),
     _("Launch TextureMaker")),
    ('TwistedBrush', imageList('tools/twistedbrush%s.png'),
     _("Launch TwistedBrush")),
    ('WTV', imageList('tools/wtv%s.png'),
     _("Launch Windows Texture Viewer")),
    ('xNormal', imageList('tools/xnormal%s.png'), _("Launch xNormal")),
    ('XnView', imageList('tools/xnview%s.png'), _("Launch XnView")),
)

audio_tools = (
    ('Audacity', imageList('tools/audacity%s.png'), _("Launch Audacity")),
    ('ABCAmberAudioConverter',
     imageList('tools/abcamberaudioconverter%s.png'),
    _("Launch ABC Amber Audio Converter")),
    ('Switch', imageList('tools/switch%s.png'), _("Launch Switch")),
)

misc_tools = (
    ('Fraps', imageList('tools/fraps%s.png'), _("Launch Fraps")),
    ('MAP', imageList('tools/interactivemapofcyrodiil%s.png'),
        _("Interactive Map of Cyrodiil and Shivering Isles")),
    ('LogitechKeyboard', imageList('tools/logitechkeyboard%s.png'),
        _("Launch LogitechKeyboard")),
    ('MediaMonkey', imageList('tools/mediamonkey%s.png'),
        _("Launch MediaMonkey")),
    ('NPP', imageList('tools/notepad++%s.png'), _("Launch Notepad++")),
    ('Steam', imageList('steam%s.png'), _("Launch Steam")),
    ('EVGAPrecision', imageList('tools/evgaprecision%s.png'),
        _("Launch EVGA Precision")),
    ('WinMerge', imageList('tools/winmerge%s.png'), _("Launch WinMerge")),
    ('FreeMind', imageList('tools/freemind%s.png'), _("Launch FreeMind")),
    ('Freeplane', imageList('tools/freeplane%s.png'), _("Launch Freeplane")),
    ('FileZilla', imageList('tools/filezilla%s.png'), _("Launch FileZilla")),
    ('EggTranslator', imageList('tools/eggtranslator%s.png'),
        _("Launch Egg Translator")),
    ('RADVideo', imageList('tools/radvideotools%s.png'),
        _("Launch RAD Video Tools")),
    ('WinSnap', imageList('tools/winsnap%s.png'), _("Launch WinSnap")),
)
