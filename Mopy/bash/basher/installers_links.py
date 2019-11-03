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

"""Menu items for the _main_ menu of the installer tab - their window attribute
points to the InstallersList singleton."""

from . import Installers_Link
from .dialogs import CreateNewProject
from .. import bass, bosh, balt, bush, load_order
from ..balt import BoolLink, AppendableLink, ItemLink, ListBoxes, \
    EnabledLink

__all__ = ['Installers_SortActive', 'Installers_SortProjects',
           'Installers_Refresh', 'Installers_AddMarker',
           'Installers_CreateNewProject', 'Installers_MonitorInstall',
           'Installers_ListPackages', 'Installers_AnnealAll',
           'Installers_UninstallAllPackages',
           'Installers_UninstallAllUnknownFiles', 'Installers_AvoidOnStart',
           'Installers_Enabled', 'Installers_AutoAnneal',
           'Installers_AutoWizard', 'Installers_AutoRefreshProjects',
           'Installers_AutoRefreshBethsoft',
           'Installers_AutoApplyEmbeddedBCFs', 'Installers_BsaRedirection',
           'Installers_RemoveEmptyDirs',
           'Installers_ConflictsReportShowsInactive',
           'Installers_ConflictsReportShowsLower',
           'Installers_ConflictsReportShowBSAConflicts',
           'Installers_WizardOverlay', 'Installers_RenameStrings',
           'Installers_GlobalSkips']

#------------------------------------------------------------------------------
# Installers Links ------------------------------------------------------------
#------------------------------------------------------------------------------
class Installers_AddMarker(ItemLink):
    """Add an installer marker."""
    _text = _('Add Marker...')
    _help = _('Adds a Marker, a special type of package useful for separating'
             ' and labelling your packages.')

    def Execute(self):
        """Add a Marker."""
        self.window.addMarker()

class Installers_MonitorInstall(Installers_Link):
    """Monitors Data folder for external installation."""
    _text = _('Monitor External Installation...')
    _help = _('Monitors the Data folder during installation via manual '
              'install or 3rd party tools.')

    @balt.conversation
    def Execute(self):
        msg = _('Wrye Bash will monitor your data folder for changes when '
                'installing a mod via an external application or manual '
                'install.  This will require two refreshes of the Data folder'
                ' and may take some time.')
        if not self._askOk(msg, _('External Installation')): return
        # Refresh Data
        self.iPanel.ShowPanel(canCancel=False, scan_data_dir=True)
        # Backup CRC data
        data_sizeCrcDate = self.idata.data_sizeCrcDate.copy()
        # Install and wait
        self._showOk(_('You may now install your mod.  When installation is '
                       'complete, press Ok.'), _('External Installation'))
        # Refresh Data
        bosh.bsaInfos.refresh() # TODO: add bsas to BAIN refresh
        with load_order.Unlock():
            mods_changed = bosh.modInfos.refresh()
        inis_changed = bosh.iniInfos.refresh()
        ui_refresh = list(map(bool, [mods_changed, inis_changed]))
        self.iPanel.ShowPanel(canCancel=False, scan_data_dir=True)
        # Determine changes
        curData = self.idata.data_sizeCrcDate
        oldFiles = set(data_sizeCrcDate)
        curFiles = set(curData)
        newFiles = curFiles - oldFiles
        delFiles = oldFiles - curFiles
        sameFiles = curFiles & oldFiles
        changedFiles = set(file_ for file_ in sameFiles if
                           data_sizeCrcDate[file_][1] != curData[file_][1])
        touchedFiles = set(file_ for file_ in sameFiles if
                           data_sizeCrcDate[file_][2] != curData[file_][2])
        touchedFiles -= changedFiles

        if not newFiles and not changedFiles and not touchedFiles:
            self._showOk(_('No changes were detected in the Data directory.'),
                         _('External Installation'))
            return
        newFiles = sorted(newFiles) # sorts case insensitive as those are CIStr
        changedFiles = sorted(changedFiles)
        touchedFiles = sorted(touchedFiles)
        # Show results, select which files to include
        checklists = []
        newFilesKey = _('New Files: %(count)i') % {'count':len(newFiles)}
        changedFilesKey = _('Changed Files: %(count)i') % {'count':len(changedFiles)}
        touchedFilesKey = _('Touched Files: %(count)i') % {'count':len(touchedFiles)}
        delFilesKey = _('Deleted Files')
        if newFiles:
            group = [newFilesKey, _(
                'These files are newly added to the Data directory.'), ]
            group.extend(newFiles)
            checklists.append(group)
        if changedFiles:
            group = [changedFilesKey, _('These files were modified.'), ]
            group.extend(changedFiles)
            checklists.append(group)
        if touchedFiles:
            group = [touchedFilesKey, _(
                'These files were not changed, but had their modification '
                'time altered.  Most likely, these files are included in '
                'the external installation, but were the same version as '
                'already existed.'), ]
            group.extend(touchedFiles)
            checklists.append(group)
        if delFiles:
            group = [delFilesKey, _(
                'These files were deleted.  BAIN does not have the '
                'capability to remove files when installing.'), ]
            group.extend(sorted(delFiles))
        with ListBoxes(self.window, _('External Installation'),
            _('The following changes were detected in the Data directory'),
            checklists, bOk=_('Create Project')) as dialog:
            if not dialog.askOkModal(): return
            include = set()
            for (lst, key) in [(newFiles, newFilesKey),
                               (changedFiles, changedFilesKey),
                               (touchedFiles, touchedFilesKey), ]:
                include |= set(dialog.getChecked(key, lst))
            if not include: return
        # Create Project
        projectName = self._askText(_('Project Name'),
                                    _('External Installation'))
        if not projectName:
            return
        path = self.window.new_name(projectName)
        # Copy Files
        with balt.Progress(_('Creating Project...'), '\n' + ' '*60) as prog:
            self.idata.createFromData(path, include, prog) # will order last
        # createFromData placed the new project last in install order - install
        try:
            self.idata.bain_install([path], ui_refresh, override=False)
        finally:
            self.iPanel.RefreshUIMods(*ui_refresh)
        # Select new installer
        self.window.SelectLast()

class Installers_ListPackages(Installers_Link):
    """Copies list of Bain files to clipboard."""
    _text = _('List Packages...')
    _help = _('Displays a list of all packages.  Also copies that list to '
        'the clipboard.  Useful for posting your package order on forums.')

    @balt.conversation
    def Execute(self):
        #--Get masters list
        message = _('Only show Installed Packages?') + '\n' + _(
            '(Else shows all packages)')
        installed_only = self._askYes(message, _('Only Show Installed?'))
        text = self.idata.getPackageList(showInactive=not installed_only)
        balt.copyToClipboard(text)
        self._showLog(text, title=_('BAIN Packages'), fixedFont=False)

class Installers_AnnealAll(Installers_Link):
    """Anneal all packages."""
    _text = _('Anneal All')
    _help = _('This will install any missing files (for active installers)'
             ' and correct all install order and reconfiguration errors.')

    @balt.conversation
    def Execute(self):
        """Anneal all packages."""
        ui_refresh = [False, False]
        try:
            with balt.Progress(_("Annealing..."),'\n'+' '*60) as progress:
                self.idata.bain_anneal(None, ui_refresh, progress=progress)
        finally:
            self.iPanel.RefreshUIMods(*ui_refresh)

class Installers_UninstallAllPackages(Installers_Link):
    """Uninstall all packages."""
    _text = _('Uninstall All Packages')
    _help = _('This will uninstall all packages.')

    @balt.conversation
    def Execute(self):
        """Uninstall all packages."""
        if not self._askYes(_("Really uninstall All Packages?")): return
        ui_refresh = [False, False]
        try:
            with balt.Progress(_("Uninstalling..."),'\n'+' '*60) as progress:
                self.idata.bain_uninstall('ALL', ui_refresh, progress=progress)
        finally:
            self.iPanel.RefreshUIMods(*ui_refresh)

class Installers_Refresh(AppendableLink, Installers_Link):
    """Refreshes all Installers data."""
    msg = _("Refresh ALL data from scratch? This may take five to ten minutes"
            " (or more) depending on the number of mods you have installed.")

    def __init__(self, full_refresh=False):
        super(Installers_Refresh, self).__init__()
        self.full_refresh = full_refresh
        self._text = _('Full Refresh') if full_refresh else _('Refresh Data')
        self._help = _(
            "Perform a full refresh of all data files, recalculating all "
            "CRCs.  This can take 5-15 minutes.") if self.full_refresh else _(
            "Rescan the Data directory and all project directories.")

    def _append(self, window): return bass.settings['bash.installers.enabled']

    @balt.conversation
    def Execute(self):
        """Refreshes all Installers data"""
        if self.full_refresh and not self._askWarning(self.msg, self._text):
            return
        self.idata.reset_refresh_flag_on_projects()
        self.iPanel.ShowPanel(fullRefresh=self.full_refresh,scan_data_dir=True)

class Installers_UninstallAllUnknownFiles(Installers_Link):
    """Uninstall all files that do not come from a current package/bethesda
    files. For safety just moved to Game Mods\Bash Installers\Bash\Data
    Folder Contents (date/time)\."""
    _text = _('Clean Data')
    _help = _('This will remove all mod files that are not linked to an'
             ' active installer out of the Data folder.')
    fullMessage = _("Clean Data directory?") + "  " + _help + "  " + _(
        'This includes files that were installed manually or by another '
        'program.  Files will be moved to the "%s" directory instead of '
        'being deleted so you can retrieve them later if necessary.  '
        'Note that if you use TES4LODGen, this will also clean out the '
        'DistantLOD folder, so on completion please run TES4LodGen again.'
        ) % bass.dirs['bainData'].join('Data Folder Contents <date>')

    @balt.conversation
    def Execute(self):
        if not self._askYes(self.fullMessage): return
        ui_refresh = [False, False]
        try:
            with balt.Progress(_("Cleaning Data Files..."),'\n' + ' ' * 65):
                self.idata.clean_data_dir(ui_refresh)
        finally:
            self.iPanel.RefreshUIMods(*ui_refresh)

#------------------------------------------------------------------------------
# Installers BoolLinks --------------------------------------------------------
#------------------------------------------------------------------------------
class Installers_AutoAnneal(BoolLink):
    _text, key, _help = _('Auto-Anneal'), 'bash.installers.autoAnneal', _(
        "Enable/Disable automatic annealing of packages.")

class Installers_AutoWizard(BoolLink):
    _text = _('Auto-Anneal/Install Wizards')
    key = 'bash.installers.autoWizard'
    _help = _("Enable/Disable automatic installing or anneal (as applicable)"
             " of packages after running its wizard.")

class _Installers_BoolLink_Refresh(BoolLink):
    def Execute(self):
        super(_Installers_BoolLink_Refresh, self).Execute()
        self.window.RefreshUI()

class Installers_WizardOverlay(_Installers_BoolLink_Refresh):
    """Toggle using the wizard overlay icon"""
    _text  = _('Wizard Icon Overlay')
    key = 'bash.installers.wizardOverlay'
    _help =_("Enable/Disable the magic wand icon overlay for packages with"
            " Wizards.")

class Installers_AutoRefreshProjects(BoolLink):
    """Toggle autoRefreshProjects setting and update."""
    _text = _('Auto-Refresh Projects')
    key = 'bash.installers.autoRefreshProjects'
    _help = _('Toggles whether or not Wrye Bash will automatically detect '
              'changes to projects in the installers directory.')

class Installers_AutoApplyEmbeddedBCFs(ItemLink):
    """Automatically apply Embedded BCFs to archives that have one."""
    _text = _('Auto-Apply Embedded BCFs')
    key = 'bash.installers.autoApplyEmbeddedBCFs'
    _help = _(
        'Automatically apply Embedded BCFs to their containing archives.')

    @balt.conversation
    def Execute(self):
        with balt.Progress(_('Auto-Applying Embedded BCFs...'),
                           message='\n' + ' ' * 60) as progress:
            destinations, converted = self.window.data_store.applyEmbeddedBCFs(
                progress=progress)
            if not destinations: return
        self.window.RefreshUI()
        self.window.ClearSelected(clear_details=True)
        self.window.SelectItemsNoCallback(destinations + converted)

class Installers_AutoRefreshBethsoft(BoolLink, Installers_Link):
    """Toggle refreshVanilla setting and update."""
    _text = _('Skip Bethsoft Content')
    key = 'bash.installers.autoRefreshBethsoft'
    _help = _('Skip installing Bethesda ESMs, ESPs, and BSAs')
    opposite = True
    message = _("Enable installation of Bethsoft Content?") + '\n\n' + _(
        "In order to support this, Bethesda ESPs, ESMs, and BSAs need to "
        "have their CRCs calculated.  Moreover Bethesda ESPs, ESMs will have "
        "their crc recalculated every time on booting BAIN.  Are you sure "
        "you want to continue?")

    @balt.conversation
    def Execute(self):
        if not bass.settings[self.key] and not self._askYes(self.message):
            return
        super(Installers_AutoRefreshBethsoft, self).Execute()
        if bass.settings[self.key]:
            # Refresh Data - only if we are now including Bethsoft files
            with balt.Progress(title=_('Refreshing Bethsoft Content'),
                               message='\n' + ' ' * 60) as progress:
                self.idata.update_for_overridden_skips(bush.game.bethDataFiles,
                                                       progress)
        # Refresh Installers
        toRefresh = set(name for name, installer in self.idata.items() if
                        installer.hasBethFiles)
        self.window.rescanInstallers(toRefresh, abort=False,
                                     update_from_data=False, shallow=True)

class Installers_Enabled(BoolLink):
    """Flips installer state."""
    _text, key, _help = _('Enabled'), 'bash.installers.enabled', _(
        'Enable/Disable the Installers tab.')
    dialogTitle = _('Enable Installers')
    message = _("Do you want to enable Installers?") + '\n\n\t' + _(
        "If you do, Bash will first need to initialize some data. This can "
        "take on the order of five minutes if there are many mods installed.")

    @balt.conversation
    def Execute(self):
        """Enable/Disable the installers tab."""
        enabled = bass.settings[self.key]
        if not enabled and not self._askYes(self.message,
                                            title=self.dialogTitle): return
        enabled = bass.settings[self.key] = not enabled
        if enabled:
            self.window.panel.ShowPanel(scan_data_dir=True)
        else:
            self.window.DeleteAll()
            self.window.panel.ClearDetails()

class Installers_BsaRedirection(AppendableLink, BoolLink, EnabledLink):
    """Toggle BSA Redirection."""
    _text, key = _('BSA Redirection'), 'bash.bsaRedirection'
    _help = _("Use Quarn's BSA redirection technique.")

    @property
    def menu_help(self):
        if not self._enable():
            return self._help + '  ' + _('%(ini)s must exist') % {
                'ini': bush.game.iniFiles[0]}
        else: return self._help

    def _append(self, window):
        section,key = bush.game.ini.bsaRedirection
        return bool(section) and bool(key)

    def _enable(self): return bosh.oblivionIni.abs_path.exists()

    def Execute(self):
        super(Installers_BsaRedirection, self).Execute()
        if bass.settings[self.key]:
            # Undo any alterations done to the textures BSA
            bsaPath = bosh.modInfos.store_dir.join(
                    bass.inisettings['OblivionTexturesBSAName'])
            bsaFile = bosh.bsa_files.OblivionBsa(bsaPath, load_cache=True,
                                                 names_only=False)
            with balt.Progress(_('Enabling BSA Redirection...'),
                               message='\n' + ' ' * 60) as progress:
                bsaFile.undo_alterations(progress)
            # Reset modification time(s) and delete AI.txt, if it exists
            bosh.bsaInfos.reset_oblivion_mtimes()
            bosh.bsaInfos.remove_invalidation_file()
            #balt.showOk(self,_(u"BSA Hashes reset: %d") % (resetCount,))
        bosh.oblivionIni.setBsaRedirection(bass.settings[self.key])

class Installers_ConflictsReportShowsInactive(_Installers_BoolLink_Refresh):
    """Toggles option to show inactive on conflicts report."""
    _text = _('Show Inactive Conflicts')
    _help = _('In the conflicts tab also display conflicts with inactive '
              '(not installed) installers')
    key = 'bash.installers.conflictsReport.showInactive'

class Installers_ConflictsReportShowsLower(_Installers_BoolLink_Refresh):
    """Toggles option to show lower on conflicts report."""
    _text = _('Show Lower Conflicts')
    _help = _('In the conflicts tab also display conflicts with lower order '
             'installers (or lower loading active bsas)')
    key = 'bash.installers.conflictsReport.showLower'

class Installers_ConflictsReportShowBSAConflicts(_Installers_BoolLink_Refresh):
    """Toggles option to show files inside BSAs on conflicts report."""
    _text = _('Show Active BSA Conflicts')
    _help = _('In the conflicts tab also display same-name resources inside '
             'installed *and* active bsas')
    key = 'bash.installers.conflictsReport.showBSAConflicts'

class Installers_AvoidOnStart(BoolLink):
    """Ensures faster bash startup by preventing Installers from being startup tab."""
    _text, key, _help = _('Avoid at Startup'), 'bash.installers.fastStart', _(
        "Toggles Wrye Bash to avoid the Installers tab on startup,"
        " avoiding unnecessary data scanning.")

class Installers_RemoveEmptyDirs(BoolLink):
    """Toggles option to remove empty directories on file scan."""
    _text = _('Remove Empty Directories')
    _help = _('Toggles whether or not Wrye Bash will remove empty '
              'directories when scanning the Data folder.')
    key = 'bash.installers.removeEmptyDirs'

# Sorting Links
class _Installer_Sort(ItemLink):
    def Execute(self):
        super(_Installer_Sort, self).Execute()
        self.window.SortItems()

class Installers_SortActive(_Installer_Sort, BoolLink):
    """Sort by type."""
    _text, key, _help = _('Sort by Active'), 'bash.installers.sortActive', _(
        'If selected, active installers will be sorted to the top of the '
        'list.')

class Installers_SortProjects(_Installer_Sort, BoolLink):
    """Sort dirs to the top."""
    _text, key, _help = _('Projects First'), 'bash.installers.sortProjects', \
        _('If selected, projects will be sorted to the top of the list.')

class Installers_SortStructure(_Installer_Sort, BoolLink):
    """Sort by type."""
    _text, key = _('Sort by Structure'), 'bash.installers.sortStructure'

#------------------------------------------------------------------------------
# Installers_Skip Links -------------------------------------------------------
#------------------------------------------------------------------------------
class _Installers_Skip(Installers_Link, BoolLink):
    """Toggle global skip settings and update."""

    @property
    def menu_help(self):
        # Slice off the starting 'Skip '
        return _('Skips the installation of %(files)s.') % {
            'files': self._text[5:]}

    @balt.conversation
    def Execute(self):
        super(_Installers_Skip, self).Execute()
        bosh.bain.Installer.init_global_skips()
        self._refreshInstallers()

    def _refreshInstallers(self):
        self.window.rescanInstallers(list(self.idata.keys()), abort=False,
            update_from_data=False,##:update data too when turning skips off ??
            shallow=True)

class _Installers_SkipScreenshots(_Installers_Skip):
    """Toggle skipScreenshots setting and update."""
    _text, key = _('Skip Screenshots'), 'bash.installers.skipScreenshots'

class _Installers_SkipScriptSources(AppendableLink, _Installers_Skip):
    """Toggle skipScriptSources setting and update."""
    _text, key = _('Skip Script Sources'), 'bash.installers.skipScriptSources'
    def _append(self, window): return bool(bush.game.script_extensions)

class _Installers_SkipImages(_Installers_Skip):
    """Toggle skipImages setting and update."""
    _text, key = _('Skip Images'), 'bash.installers.skipImages'

class _Installers_SkipDistantLOD(_Installers_Skip):
    """Toggle skipDistantLOD setting and update."""
    _text, key = _('Skip DistantLOD'), 'bash.installers.skipDistantLOD'

class _Installers_SkipLandscapeLODMeshes(_Installers_Skip):
    """Toggle skipLandscapeLODMeshes setting and update."""
    _text = _('Skip LOD Meshes')
    key = 'bash.installers.skipLandscapeLODMeshes'

class _Installers_SkipLandscapeLODTextures(_Installers_Skip):
    """Toggle skipLandscapeLODTextures setting and update."""
    _text = _('Skip LOD Textures')
    key = 'bash.installers.skipLandscapeLODTextures'

class _Installers_SkipLandscapeLODNormals(_Installers_Skip):
    """Toggle skipLandscapeLODNormals setting and update."""
    _text = _('Skip LOD Normals')
    key = 'bash.installers.skipLandscapeLODNormals'

class _Installers_SkipBsl(AppendableLink, _Installers_Skip):
    """Toggle skipTESVBsl setting and update."""
    _text, key = _('Skip BSL Files'), 'bash.installers.skipTESVBsl'
    def _append(self, window): return bush.game.has_bsl

class Installers_GlobalSkips(balt.MenuLink):
    """Global Skips submenu."""
    _text = _('Global Skips')

    def __init__(self):
        super(Installers_GlobalSkips, self).__init__()
        self.append(_Installers_SkipOBSEPlugins())
        self.append(_Installers_SkipScreenshots())
        self.append(_Installers_SkipScriptSources())
        self.append(_Installers_SkipImages())
        self.append(_Installers_SkipDocs())
        self.append(_Installers_SkipDistantLOD())
        self.append(_Installers_SkipLandscapeLODMeshes())
        self.append(_Installers_SkipLandscapeLODTextures())
        self.append(_Installers_SkipLandscapeLODNormals())
        self.append(_Installers_SkipBsl())

# Complex skips
class _Installers_Process_Skip(_Installers_Skip):
    """Toggle global skip settings and update - those skips however have to
    be processed before skipped and are not set in init_global_skips."""

    def Execute(self):
        super(Installers_Link, self).Execute() # note Installers_Link !
        self._refreshInstallers()

class _Installers_SkipDocs(_Installers_Process_Skip):
    """Toggle skipDocs setting and update."""
    _text, key = _('Skip Docs'), 'bash.installers.skipDocs'

class _Installers_SkipOBSEPlugins(AppendableLink, _Installers_Skip):
    """Toggle allowOBSEPlugins setting and update."""
    _se_sd = bush.game.se.se_abbrev + (
            '/' + bush.game.sd.long_name) if bush.game.sd.sd_abbrev else ''
    _text = _('Skip %s Plugins') % _se_sd
    key = 'bash.installers.allowOBSEPlugins'
    def _append(self, window): return bool(self._se_sd)
    def _check(self): return not bass.settings[self.key]

class Installers_RenameStrings(AppendableLink, _Installers_Process_Skip):
    """Toggle auto-renaming of .STRINGS files"""
    _text = _('Auto-name String Translation Files')
    key = 'bash.installers.renameStrings'
    def _append(self, window): return bool(bush.game.esp.stringsFiles)

    @property
    def menu_help(self):
        return _('If checked, Wrye Bash will rename all installed string '
                 'files so they match your current language.')

#--New project dialog ---------------------------------------------------------
class Installers_CreateNewProject(ItemLink):
    """Open the Create New Project Dialog"""
    _text = _('Create New Project...')
    _help = _('Create a new project...')

    @balt.conversation
    def Execute(self): CreateNewProject.Display()
