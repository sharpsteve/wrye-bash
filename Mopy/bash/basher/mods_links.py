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

"""Menu items for the _main_ menu of the mods tab - their window attribute
points to BashFrame.modList singleton."""

import re as _re
from .. import bosh, balt, bass, load_order
from .. import bush # for Mods_LoadListData, Mods_LoadList
from ..balt import ItemLink, CheckLink, BoolLink, EnabledLink, ChoiceLink, \
    SeparatorLink, Link
from ..bolt import GPath
from .. import exception

__all__ = ['Mods_EsmsFirst', 'Mods_LoadList', 'Mods_SelectedFirst',
           'Mods_OblivionVersion', 'Mods_CreateBlankBashedPatch',
           'Mods_CreateBlank', 'Mods_ListMods', 'Mods_ListBashTags',
           'Mods_CleanDummyMasters', 'Mods_AutoGhost', 'Mods_LockLoadOrder',
           'Mods_ScanDirty', 'Mods_CrcRefresh']

# "Load" submenu --------------------------------------------------------------
def _getLoadListsDict():
    loadListData = bass.settings['bash.loadLists.data']
    loadListData['Bethesda ESMs'] = [GPath(x) for x in bush.game.bethDataFiles
        if x.endswith('.esm') # but avoid activating modding esms for oblivion
    and (not _re.match(bosh.reOblivion.pattern, x, _re.IGNORECASE)
         or x == 'oblivion.esm')]
    return loadListData

class _Mods_LoadListData(balt.ListEditorData):
    """Data capsule for load list editing dialog."""
    def __init__(self, parent, loadListsDict):
        self.loadListDict = loadListsDict
        #--GUI
        balt.ListEditorData.__init__(self,parent)
        self.showRename = True
        self.showRemove = True

    def getItemList(self):
        """Returns load list keys in alpha order."""
        return sorted(list(self.loadListDict.keys()), key=lambda a: a.lower())

    def rename(self,oldName,newName):
        """Renames oldName to newName."""
        #--Right length?
        if len(newName) == 0 or len(newName) > 64:
            balt.showError(self.parent,
                _('Name must be between 1 and 64 characters long.'))
            return False
        #--Rename
        bass.settings.setChanged('bash.loadLists.data')
        self.loadListDict[newName] = self.loadListDict[oldName]
        del self.loadListDict[oldName]
        return newName

    def remove(self,item):
        """Removes load list."""
        bass.settings.setChanged('bash.loadLists.data')
        del self.loadListDict[item]
        return True

class Mods_LoadList(ChoiceLink):
    """Add active mods list links."""
    loadListsDict = {}

    def __init__(self):
        super(Mods_LoadList, self).__init__()
        Mods_LoadList.loadListsDict = self.loadListsDict or _getLoadListsDict()
        #--Links
        class __Activate(ItemLink):
            """Common methods used by Links de/activating mods."""
            def _refresh(self): self.window.RefreshUI(refreshSaves=True)
            def _selectExact(self, mods):
                errorMessage = bosh.modInfos.lo_activate_exact(mods)
                self._refresh()
                if errorMessage: self._showError(errorMessage, self._text)
        class _All(__Activate):
            _text = _('Activate All')
            _help = _('Activate all mods')
            def Execute(self):
                """Select all mods."""
                try:
                    bosh.modInfos.lo_activate_all()
                except exception.PluginsFullError:
                    self._showError(
                        _("Mod list is full, so some mods were skipped"),
                        _('Select All'))
                except exception.BoltError as e:
                    self._showError('%s' % e, _('Select All'))
                self._refresh()
        class _None(__Activate):
            _text = _('De-activate All')
            _help = _('De-activate all mods')
            def Execute(self): self._selectExact([])
        class _Selected(__Activate):
            _text = _('Activate Selected')
            _help = _('Activate only the mods selected in the UI')
            def Execute(self):
                self._selectExact(self.window.GetSelected())
        class _Edit(ItemLink):
            _text = _('Edit Active Mods Lists...')
            _help = _('Display a dialog to rename/remove active mods lists')
            def Execute(self):
                editorData = _Mods_LoadListData(self.window,
                                                Mods_LoadList.loadListsDict)
                balt.ListEditor.Display(self.window, _('Active Mods Lists'),
                                        editorData)
        class _SaveLink(EnabledLink):
            _text = _('Save Active Mods List')
            _help = _('Save the currently active mods to a new active mods list')
            def _enable(self): return bool(load_order.cached_active_tuple())
            def Execute(self):
                newItem = self._askText(
                    _('Save currently active mods list as:'))
                if not newItem: return
                if len(newItem) > 64:
                    message = _('Active Mods list name must be between '
                                '1 and 64 characters long.')
                    return self._showError(message)
                Mods_LoadList.loadListsDict[newItem] = list(
                    load_order.cached_active_tuple())
                bass.settings.setChanged('bash.loadLists.data')
        self.extraItems = [_All(), _None(), _Selected(), _SaveLink(), _Edit(),
                           SeparatorLink()]
        class _LoListLink(__Activate):
            def Execute(self):
                """Activate mods in list."""
                mods = set(Mods_LoadList.loadListsDict[self._text])
                mods = [m for m in list(self.window.data_store.keys()) if m in mods]
                self._selectExact(mods)
            @property
            def menu_help(self):
                return _('Activate mods in the %(list_name)s list' % {
                    'list_name': self._text})
        self.__class__.choiceLinkType = _LoListLink

    @property
    def _choices(self):
        return sorted(list(self.loadListsDict.keys()), key=lambda a: a.lower())

# "Sort by" submenu -----------------------------------------------------------
class Mods_EsmsFirst(CheckLink, EnabledLink):
    """Sort esms to the top."""
    _help = _('Sort masters by type. Always on if current sort is Load Order.')
    _text = _('Type')

    def _enable(self): return not self.window.forceEsmFirst()
    def _check(self): return self.window.esmsFirst

    def Execute(self):
        self.window.esmsFirst = not self.window.esmsFirst
        self.window.SortItems()

class Mods_SelectedFirst(CheckLink):
    """Sort loaded mods to the top."""
    _help = _('Sort loaded mods to the top')
    _text = _('Selection')

    def _check(self): return self.window.selectedFirst

    def Execute(self):
        self.window.selectedFirst = not self.window.selectedFirst
        self.window.SortItems()

# "Oblivion.esm" submenu ------------------------------------------------------
class Mods_OblivionVersion(CheckLink, EnabledLink):
    """Specify/set Oblivion version."""
    _help = _('Specify/set Oblivion version')

    def __init__(self, key, setProfile=False):
        super(Mods_OblivionVersion, self).__init__()
        self.key = self._text = key
        self.setProfile = setProfile

    def _check(self): return bosh.modInfos.voCurrent == self.key

    def _enable(self):
        return bosh.modInfos.voCurrent is not None \
                          and self.key in bosh.modInfos.voAvailable

    def Execute(self):
        """Handle selection."""
        if bosh.modInfos.voCurrent == self.key: return
        bosh.modInfos.setOblivionVersion(self.key)
        self.window.RefreshUI(refreshSaves=True) # True: refresh save's masters
        if self.setProfile:
            bosh.saveInfos.profiles.setItem(bosh.saveInfos.localSave,'vOblivion',self.key)
        Link.Frame.SetTitle()

# "File" submenu --------------------------------------------------------------
class Mods_CreateBlankBashedPatch(ItemLink):
    """Create a new bashed patch."""
    _text, _help = _('New Bashed Patch...'), _('Create a new bashed patch')

    def Execute(self):
        newPatchName = bosh.modInfos.generateNextBashedPatch(
            self.window.GetSelected())
        if newPatchName is not None:
            self.window.ClearSelected(clear_details=True)
            self.window.RefreshUI(redraw=[newPatchName], refreshSaves=False)
        else:
            self._showWarning("Unable to create new bashed patch: "
                              "10 bashed patches already exist!")

class Mods_CreateBlank(ItemLink):
    """Create a new blank mod."""
    _text, _help = _('New Mod...'), _('Create a new blank mod')

    def __init__(self, masterless=False):
        super(Mods_CreateBlank, self).__init__()
        self.masterless = masterless
        if masterless:
            self._text = _('New Mod (masterless)...')
            self._help = _('Create a new blank mod with no masters')

    def Execute(self):
        newName = self.window.new_name(GPath('New Mod.esp'))
        windowSelected = self.window.GetSelected()
        self.window.data_store.create_new_mod(newName, windowSelected,
                                              masterless=self.masterless)
        if windowSelected: # assign it the group of the first selected mod
            mod_group = self.window.data_store.table.getColumn('group')
            mod_group[newName] = mod_group.get(windowSelected[0], '')
        self.window.ClearSelected(clear_details=True)
        self.window.RefreshUI(redraw=[newName], refreshSaves=False)

#------------------------------------------------------------------------------
class Mods_ListMods(ItemLink):
    """Copies list of mod files to clipboard."""
    _text = _("List Mods...")
    _help = _("Copies list of active mod files to clipboard.")

    def Execute(self):
        #--Get masters list
        list_txt = bosh.modInfos.getModList(showCRC=balt.getKeyState(67))
        balt.copyToClipboard(list_txt)
        self._showLog(list_txt, title=_("Active Mod Files"), fixedFont=False)

#------------------------------------------------------------------------------
class Mods_ListBashTags(ItemLink): # duplicate of mod_links.Mod_ListBashTags
    """Copies list of bash tags to clipboard."""
    _text = _("List Bash Tags...")
    _help = _("Copies list of bash tags to clipboard.")

    def Execute(self):
        tags_text = bosh.modInfos.getTagList()
        balt.copyToClipboard(tags_text)
        self._showLog(tags_text, title=_("Bash Tags"), fixedFont=False)

#------------------------------------------------------------------------------
class Mods_CleanDummyMasters(EnabledLink):
    """Clean up after using a 'Create Dummy Masters...' command."""
    _text = _('Remove Dummy Masters...')
    _help = _("Clean up after using a 'Create Dummy Masters...' command")

    def _enable(self):
        for fileInfo in list(bosh.modInfos.values()):
            if fileInfo.header.author == 'BASHED DUMMY':
                return True
        return False

    def Execute(self):
        remove = []
        for fileName, fileInfo in bosh.modInfos.items():
            if fileInfo.header.author == 'BASHED DUMMY':
                remove.append(fileName)
        remove = load_order.get_ordered(remove)
        self.window.DeleteItems(items=remove, order=False,
                                dialogTitle=_('Delete Dummy Masters'))

#------------------------------------------------------------------------------
class Mods_AutoGhost(BoolLink):
    """Toggle Auto-ghosting."""
    _text, key = _('Auto-Ghost'), 'bash.mods.autoGhost'
    _help = _('Toggles whether or not to automatically ghost all disabled '
              'mods.')

    def Execute(self):
        super(Mods_AutoGhost, self).Execute()
        self.window.RefreshUI(redraw=bosh.modInfos.autoGhost(force=True),
                              refreshSaves=False)

#------------------------------------------------------------------------------
class Mods_ScanDirty(BoolLink):
    """Read mod CRC's to check for dirty mods."""
    _text = _("Check mods against LOOT's dirty mod list")
    _help = _("Display a tooltip if mod is dirty and underline dirty mods - "
             "checks are performed using bundled LOOT")
    key = 'bash.mods.scanDirty'

    def Execute(self):
        super(Mods_ScanDirty, self).Execute()
        self.window.RefreshUI(refreshSaves=False) # update all mouse tips

class Mods_LockLoadOrder(CheckLink):
    """Turn on Lock Load Order feature."""
    _text = _('Lock Load Order')
    _help = _("Will reset mod Load Order to whatever Wrye Bash has saved for"
             " them whenever Wrye Bash refreshes data/starts up.")

    def _check(self): return load_order.locked

    def Execute(self): load_order.toggle_lock_load_order()

class Mods_CrcRefresh(ItemLink):
    """Recalculate crcs for all mods"""
    _text = _('Recalculate CRCs')
    _help = _('Clean stale CRCs from cache')

    @balt.conversation
    def Execute(self):
        message = '== %s' % _('Mismatched CRCs') + '\n\n'
        with balt.BusyCursor(): pairs = bosh.modInfos.refresh_crcs()
        mismatched = dict((k, v) for k, v in pairs.items() if v[0] != v[1])
        if mismatched:
            message += '  * ' + '\n  * '.join(
                ['%s: cached %08X real %08X' % (k.s, v[1], v[0]) for k, v in
                 mismatched.items()])
            self.window.RefreshUI(redraw=list(mismatched.keys()), refreshSaves=False)
        else: message += _('No stale cached CRC values detected')
        self._showWryeLog(message)
