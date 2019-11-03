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

import re
import time
from ..balt import EnabledLink, AppendableLink, ItemLink, RadioLink, \
    ChoiceLink, MenuLink, CheckLink, Image, UIList_Rename, OneItemLink
from .. import bass, balt, bosh, bush
from .import People_Link, SaveDetails
from ..bolt import GPath

__all__ = ['ColumnsMenu', 'Master_ChangeTo', 'Master_Disable',
           'Screens_NextScreenShot', 'Screen_JpgQuality',
           'Screen_JpgQualityCustom', 'Screen_Rename', 'Screen_ConvertTo',
           'People_AddNew', 'People_Import', 'People_Karma', 'People_Export',
           'Master_AllowEdit', 'Master_ClearRenames']

# Screen Links ----------------------------------------------------------------
#------------------------------------------------------------------------------
class Screens_NextScreenShot(EnabledLink):
    """Sets screenshot base name and number."""
    _text = _('Next Shot...')
    _help = _('Set screenshot base name and number')
    rePattern = re.compile('' r'^(.+?)(\d*)$', re.I | re.U)

    def _enable(self):
        return not bosh.oblivionIni.isCorrupted \
               and bosh.oblivionIni.abs_path.exists()

    @property
    def menu_help(self):
        if not self._enable():
            return self._help + '.  ' + _('%(ini)s must exist') % {
                'ini': bush.game.iniFiles[0]}
        else: return self._help

    def Execute(self):
        oblivionIni = bosh.oblivionIni
        base = oblivionIni.getSetting('Display', 'sScreenShotBaseName',
                                      'ScreenShot')
        next_ = oblivionIni.getSetting('Display', 'iScreenShotIndex', '0')
        pattern = self._askText(
            _("Screenshot base name, optionally with next screenshot number.")
            + '\n' +
            _("E.g. ScreenShot or ScreenShot_101 or Subdir\\ScreenShot_201."),
            default=base + next_)
        if not pattern: return
        maPattern = self.__class__.rePattern.match(pattern)
        newBase,newNext = maPattern.groups()
        settings_screens = {'Display': {
            'SScreenShotBaseName': newBase,
            'iScreenShotIndex': (newNext or next_),
            'bAllowScreenShot': '1', }}
        screensDir = GPath(newBase).head
        if screensDir:
            if not screensDir.isabs(): screensDir = bass.dirs['app'].join(
                screensDir)
            screensDir.makedirs()
        oblivionIni.saveSettings(settings_screens)
        bosh.screensData.refresh()
        self.window.RefreshUI()

#------------------------------------------------------------------------------
class Screen_ConvertTo(EnabledLink):
    """Converts selected images to another type."""
    _help = _('Convert selected images to another format')

    def __init__(self,ext,imageType):
        super(Screen_ConvertTo, self).__init__()
        self.ext = ext.lower()
        self.imageType = imageType
        self._text = _('Convert to %s') % self.ext

    def _enable(self):
        self.convertable = [s for s in self.selected if
                            s.cext != '.' + self.ext]
        return bool(self.convertable)

    def Execute(self):
        try:
            with balt.Progress(_("Converting to %s") % self.ext) as progress:
                progress.setFull(len(self.convertable))
                for index, fileName in enumerate(self.convertable):
                    progress(index,fileName.s)
                    srcPath = bosh.screensData.store_dir.join(fileName)
                    destPath = srcPath.root+'.'+self.ext
                    if srcPath == destPath or destPath.exists(): continue
                    bitmap = Image.Load(srcPath, quality=bass.settings[
                        'bash.screens.jpgQuality'])
                    result = bitmap.SaveFile(destPath.s,self.imageType)
                    if not result: continue
                    srcPath.remove()
        finally:
            bosh.screensData.refresh()
            self.window.RefreshUI()

#------------------------------------------------------------------------------
class Screen_JpgQuality(RadioLink):
    """Sets JPEG quality for saving."""
    _help = _('Sets JPEG quality for saving')

    def __init__(self, quality):
        super(Screen_JpgQuality, self).__init__()
        self.quality = quality
        self._text = '%i' % self.quality

    def _check(self):
        return self.quality == bass.settings['bash.screens.jpgQuality']

    def Execute(self):
        bass.settings['bash.screens.jpgQuality'] = self.quality

#------------------------------------------------------------------------------
class Screen_JpgQualityCustom(Screen_JpgQuality):
    """Sets a custom JPG quality."""
    def __init__(self):
        super(Screen_JpgQualityCustom, self).__init__(
            bass.settings['bash.screens.jpgCustomQuality'])
        self._text = _('Custom [%i]') % self.quality

    def Execute(self):
        quality = self._askNumber(_('JPEG Quality'), value=self.quality,
                                  min=0, max=100)
        if quality is None: return
        self.quality = quality
        bass.settings['bash.screens.jpgCustomQuality'] = self.quality
        self._text = _('Custom [%i]') % quality
        super(Screen_JpgQualityCustom, self).Execute()

#------------------------------------------------------------------------------
class Screen_Rename(UIList_Rename):
    """Renames files by pattern."""
    _help = _('Renames files by pattern')

# People Links ----------------------------------------------------------------
#------------------------------------------------------------------------------
class People_AddNew(ItemLink, People_Link):
    """Add a new record."""
    dialogTitle = _('Add New Person')
    _text = _('Add...')
    _help = _('Add a new record')

    def Execute(self):
        name = self._askText(_("Add new person:"), self.dialogTitle)
        if not name: return
        if name in self.pdata: return self._showInfo(
            name + _(" already exists."), title=self.dialogTitle)
        self.pdata[name] = (time.time(),0,'')
        self.window.RefreshUI(redraw=[name])
        self.window.EnsureVisibleItem(name, focus=True)
        self.pdata.setChanged()

#------------------------------------------------------------------------------
class People_Export(ItemLink, People_Link):
    """Export people to text archive."""
    dialogTitle = _("Export People")
    _text = _('Export...')
    _help = _('Export people to text archive')

    def Execute(self):
        textDir = bass.settings.get('bash.workDir', bass.dirs['app'])
        #--File dialog
        export_path = self._askSave(title=_('Export people to text file:'),
                             defaultDir=textDir, defaultFile='People.txt',
                             wildcard='*.txt')
        if not export_path: return
        bass.settings['bash.workDir'] = export_path.head
        self.pdata.dumpText(export_path, self.selected)
        self._showInfo(_('Records exported: %d.') % len(self.selected),
                       title=self.dialogTitle)

#------------------------------------------------------------------------------
class People_Import(ItemLink, People_Link):
    """Import people from text archive."""
    dialogTitle = _("Import People")
    _text = _('Import...')
    _help = _('Import people from text archive')

    def Execute(self):
        textDir = bass.settings.get('bash.workDir', bass.dirs['app'])
        #--File dialog
        import_path = self._askOpen(title=_('Import people from text file:'),
                                    defaultDir=textDir, wildcard='*.txt',
                                    mustExist=True)
        if not import_path: return
        bass.settings['bash.workDir'] = import_path.head
        newNames = self.pdata.loadText(import_path)
        self._showInfo(_("People imported: %d") % len(newNames),
                       title=self.dialogTitle)
        self.window.RefreshUI()

#------------------------------------------------------------------------------
class People_Karma(ChoiceLink, balt.MenuLink, People_Link):
    """Add Karma setting links."""
    _text = _('Karma')
    karma_labels = ['%+d' % x for x in range(5, -6, -1)]

    class _Karma(ItemLink, People_Link):
        def Execute(self):
            karma = int(self._text)
            for item in self.selected:
                self.pdata[item] = (time.time(), karma, self.pdata[item][2])
            self.window.RefreshUI()
            self.pdata.setChanged()

    choiceLinkType = _Karma

    @property
    def _choices(self): return self.__class__.karma_labels

# Masters Links ---------------------------------------------------------------
#------------------------------------------------------------------------------
class Master_AllowEdit(CheckLink, EnabledLink):
    _text, _help = _('Allow edit'), _('Allow editing the masters list')

    def _enable(self): return self.window.panel.detailsPanel.allowDetailsEdit
    def _check(self): return self.window.allowEdit
    def Execute(self): self.window.allowEdit ^= True

class Master_ClearRenames(ItemLink):
    _text = _('Clear Renames')
    _help = _('Clear internal Bash renames dictionary')

    def Execute(self):
        bass.settings['bash.mods.renames'].clear()
        self.window.RefreshUI()

class _Master_EditList(OneItemLink): # one item cause _singleSelect = True

    def _enable(self): return self.window.allowEdit

    @property
    def menu_help(self):
        if not self._enable(): return self.__class__._help + '.  ' + _(
                'You must first allow editing from the column menu')
        else: return self.__class__._help

class Master_ChangeTo(_Master_EditList):
    """Rename/replace master through file dialog."""
    _text = _("Change to...")
    _help = _("Rename/replace master through file dialog")

    @balt.conversation
    def Execute(self):
        masterInfo = self._selected_info
        master_name = masterInfo.name
        #--File Dialog
        wildcard = bosh.modInfos.plugin_wildcard()
        newPath = self._askOpen(title=_('Change master name to:'),
                                defaultDir=bosh.modInfos.store_dir,
                                defaultFile=master_name, wildcard=wildcard,
                                mustExist=True)
        if not newPath: return
        (newDir,newName) = newPath.headTail
        #--Valid directory?
        if newDir != bosh.modInfos.store_dir:
            self._showError(_("File must be selected from "
                "%s Data Files directory." % bush.game.displayName))
            return
        elif newName == master_name:
            return
        #--Save Name
        masterInfo.setName(newName)
        bass.settings.getChanged('bash.mods.renames')[master_name] = newName
        self.window.SetMasterlistEdited(repopulate=True)

#------------------------------------------------------------------------------
class Master_Disable(AppendableLink, _Master_EditList):
    """Rename/replace master through file dialog."""
    _text = _("Disable")
    _help = _("Disable master")

    def _append(self, window): #--Saves only
        return isinstance(window.detailsPanel, SaveDetails)

    def Execute(self):
        masterInfo = self._selected_info
        newName = GPath(re.sub('[mM]$', 'p', 'XX' + masterInfo.name.s))
        #--Save Name
        masterInfo.setName(newName)
        self.window.SetMasterlistEdited(repopulate=True)

# Column menu -----------------------------------------------------------------
#------------------------------------------------------------------------------
class _Column(CheckLink, EnabledLink):

    def __init__(self, _text='COLKEY'):
        """:param _text: not the link _text in this case, the key to the text
        """
        super(_Column, self).__init__()
        self.colName = _text
        self._text = bass.settings['bash.colNames'][_text]
        self._help = _("Show/Hide '%(colname)s' column.") % {
            'colname': self._text}

    def _enable(self):
        return self.colName not in self.window.persistent_columns

    def _check(self): return self.colName in self.window.cols

    def Execute(self):
        if self.colName in self.window.cols:
            self.window.cols.remove(self.colName)
        else:
            #--Ensure the same order each time
            cols = self.window.cols[:]
            del self.window.cols[:]
            self.window.cols.extend([x for x in self.window.allCols if
                                     x in cols or x == self.colName])
        self.window.PopulateColumns()
        self.window.RefreshUI()

class ColumnsMenu(ChoiceLink, MenuLink):
    """Customize visible columns."""
    _text = _("Columns")
    # extraItems
    class _AutoWidth(RadioLink):
        wxFlag = 0
        def _check(self): return self.wxFlag == self.window.autoColWidths
        def Execute(self):
            self.window.autoColWidths = self.wxFlag
            self.window.autosizeColumns()
    class _Manual(_AutoWidth):
        _text = _('Manual')
        _help = _(
            'Allow to manually resize columns. Applies to all Bash lists')
    class _Contents(_AutoWidth):
        _text, wxFlag = _('Fit Contents'), 1 # wx.LIST_AUTOSIZE
        _help = _('Fit columns to their content. Applies to all Bash lists.'
                 ' You can hit Ctrl + Numpad+ to the same effect')
    class _Header(_AutoWidth):
        _text, wxFlag = _('Fit Header'), 2 # wx.LIST_AUTOSIZE_USEHEADER
        _help = _('Fit columns to their content, keep header always visible. '
                 ' Applies to all Bash lists')
    extraItems = [_Manual(), _Contents(), _Header(), balt.SeparatorLink()]
    # choices
    choiceLinkType = _Column
    @property
    def _choices(self): return self.window.allCols
